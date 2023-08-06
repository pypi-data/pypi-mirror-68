import OUtils.Kafka

import confluent_kafka
import uuid
import time
import re


class Heartbeat:

    @staticmethod
    def are_topics_skewed():
        # [1] https://docs.confluent.io/current/clients/confluent-kafka-python/#confluent_kafka.admin.PartitionMetadata
        configs = OUtils.Kafka.get_check_configurations("heartbeat")

        heartbeat_topics = OUtils.Kafka.get_topics_metadata(configs["topic_pattern"])

        # Ensure that something is being checked
        assert len(heartbeat_topics) > 0, \
            "No metadata loaded/found for provided topic_pattern '%s'" % configs["topic_pattern"]

        # Ensure quantity of brokers and heartbeat topics matches
        qty_of_heartbeat_topics = len(heartbeat_topics)
        qty_of_brokers = len(OUtils.Kafka.get_brokers_metadata())
        assert qty_of_heartbeat_topics >= qty_of_brokers, \
            "Quantity of heartbeat topics (%d) and brokers (%d) differ" % (qty_of_heartbeat_topics, qty_of_brokers)

        # Ensure the heartbeat topics are not partitioned and not replicated
        for heartbeat_topic in heartbeat_topics:

            assert len(heartbeat_topic.partitions) == 1, \
                "Heartbeat topic '%s' has multiple partitions" % heartbeat_topic

            assert len(heartbeat_topic.partitions[0].replicas) == 1, \
                "Heartbeat topic '%s' is replicated" % heartbeat_topic

        # If all assertions succeeded
        return False

    @staticmethod
    def is_topic_on_homonym_node(topic):
        heartbeat_topics = OUtils.Kafka.get_topics_metadata(topic)

        return heartbeat_topics[0].topic.endswith(str(heartbeat_topics[0].partitions[0].leader))

    @staticmethod
    def run_on_topic(topic):
        # Ensure heartbeat topics are at the right places
        assert OUtils.Kafka.checks.Heartbeat.are_topics_skewed() is False, \
            "Heartbeat topics not ready for check execution (skewed situation)"

        assert OUtils.Kafka.checks.Heartbeat.is_topic_on_homonym_node(topic) is True, \
            "Heartbeat topic '%s' is not hosted on the homonym broker" % topic

        configs = OUtils.Kafka.get_check_configurations("heartbeat")

        # Ensure heartbeat is executed on topics dedicated to heartbeats
        assert re.match(configs["topic_pattern"], topic), \
            "The topic specified '%s' does not match the required pattern '%s'" % (topic, configs["topic_pattern"])

        # Actors
        consumer = Heartbeat.__get_consumer(topic, configs["timeout_assignment"])
        producer = Heartbeat.__get_producer(topic)

        # Generate token
        injected_token = str(uuid.uuid4())

        time_0 = time.clock()

        # Produce a message
        producer.produce(topic=topic, value=injected_token.encode("utf-8"))

        # Consume messages
        messages = consumer.consume(num_messages=1, timeout=configs["timeout_consumption"])

        time_1 = time.clock()

        # Close consumer handler to release partition assignments more quickly (and help the next check execution)
        consumer.close()

        # Check 1: quantity of messages
        assert len(messages) == 1, \
            "Unexpected quantity of messages received (%d)" % len(messages)

        # Check 2: verify content
        loaded_token = str(messages[0].value().decode("utf-8"))
        assert loaded_token == injected_token, \
            "The consumed message (%s) is not consistent with injected token (%s)" % (loaded_token, injected_token)

        # If all good, return heartbeat elapsed time
        return time_1 - time_0

    @staticmethod
    def __get_consumer(topic, timeout):
        properties = OUtils.Kafka.get_base_properties()

        properties["group.id"] = properties["client.id"] = topic  # Use topic name as group.id, so to avoid offset commit overlaps

        consumer = confluent_kafka.Consumer(properties)
        consumer.subscribe([topic])

        for attempt in range(timeout):
            consumer.poll(1)
            if len(consumer.assignment()) > 0:
                break

        assignments = consumer.assignment()

        assert len(assignments) == 1, \
            "Partitions assignment (%d) inconsistent after timeout." % len(assignments)

        # Move offsets to the latest point for each partition
        # assignments[0].offset = confluent_kafka.OFFSET_END

        # consumer.assign(assignments)

        return consumer

    @staticmethod
    def __get_producer(topic):
        properties = OUtils.Kafka.get_base_properties()

        properties["client.id"] = topic

        return confluent_kafka.Producer(properties)
