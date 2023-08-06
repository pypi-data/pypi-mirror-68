import OUtils.configurations
import OUtils.Kafka.metrics as metrics
import OUtils.Kafka.checks as checks

import confluent_kafka.admin
import re


def get_nodes(port=False):
    result = []
    nodes = OUtils.configurations.get(module="kafka", key="nodes")

    for node in nodes:
        if port is False:
            result.append(node["host"])

        elif port not in node["ports"]:
            raise KeyError("Port '%s' not supported" % port)

        else:
            result.append("%s:%d" % (node["host"], node["ports"][port]))

    assert len(result) >= 3, "Too few nodes (%s) loaded. Please check configuration file." % len(result)

    return result


def get_configuration_files():
    result = OUtils.configurations.get(module="kafka", key="configuration_files")

    assert len(result) > 0, "Too few (%d) configuration files loaded. Please check configurations file." % len(result)

    return result


def get_check_configurations(check_name):
    result = OUtils.configurations.get(module="kafka", key="checks")

    assert check_name in result.keys(), "No configurations found for check (%s)." % check_name

    return result[check_name]


def get_base_properties():
    nodes = OUtils.Kafka.get_nodes(port="kafka")

    properties = OUtils.configurations.get(module="kafka", key="base_properties")
    properties = {**properties, **{"bootstrap.servers": ",".join(nodes)}}

    return properties


def __get_admin_client():
    properties = OUtils.Kafka.get_base_properties()

    return confluent_kafka.admin.AdminClient(properties)


def get_topics_metadata(topic_name_pattern=".*"):
    return [topic_metadata for topic_metadata in __get_admin_client().list_topics().topics.values()
            if re.match(topic_name_pattern, topic_metadata.topic)]


def get_brokers_metadata():
    return __get_admin_client().list_topics().brokers
