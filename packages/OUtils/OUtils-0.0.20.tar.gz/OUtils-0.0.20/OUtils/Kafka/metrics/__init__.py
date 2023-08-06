import OUtils.Kafka

import subprocess
import jmxquery
import sys
import os


def __execute_jmx_query(node, query_string):
    assert ":" in node, "Missing port information on provided argument '%s'" % node

    try:
        # This is suppress visualization of jar stderr errors (e.g. connection failed)
        # Ref. https://stackoverflow.com/questions/2125702/how-to-suppress-console-output-in-python
        # Ref. https://stackoverflow.com/questions/1956142/how-to-redirect-stderr-in-python
        sys.stderr = open(os.devnull, "w")

        jmx_connection = jmxquery.JMXConnection(connection_uri="service:jmx:rmi:///jndi/rmi://%s/jmxrmi" % node)
        jmx_results = jmx_connection.query([jmxquery.JMXQuery(mBeanName=query_string)])

    except subprocess.SubprocessError as error:
        if "ConnectException" in error.output.decode("utf-8"):
            raise ConnectionError(error.output.decode("utf-8"))

        else:
            raise error

    finally:
        # Conclusion of the trick above
        sys.stderr = sys.__stderr__

    return jmx_results


def get_under_replicated_replicas_per_node(node):
    results = __execute_jmx_query(node, "kafka.server:type=ReplicaManager,name=UnderReplicatedPartitions")

    if len(results) == 0:
        raise ConnectionError("Unable to load JMX Query results (timeout?)")

    return results[0].value


def get_total_under_replicated_replicas():
    result = 0

    for node in OUtils.Kafka.get_nodes(port="jmx"):
        result = get_under_replicated_replicas_per_node(node=node)

    return result
