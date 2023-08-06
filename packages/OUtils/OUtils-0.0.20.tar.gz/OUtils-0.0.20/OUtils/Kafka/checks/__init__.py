import OUtils.Kafka

from OUtils.Kafka.checks.Heartbeat import *

import subprocess
import re


def __is_file_aligned_across_nodes(file_path, whitelisted_patterns):
    assert file_path.startswith("/"), "The value of filePath (%s) appears invalid. Please check." % file_path

    nodes = OUtils.Kafka.get_nodes()

    # Compare each file against the copy on another's node (there is 1x overlap!)
    for i in range(len(nodes)):
        node_a = nodes[i - 1]
        node_b = nodes[i]

        cmd = "bash -c \"diff <(ssh %s 'cat %s') <(ssh %s 'cat %s') | grep -E '< .|> .' | cut -c 3-\""
        cmd = cmd % (node_a, file_path, node_b, file_path)

        output = subprocess.run(cmd, shell=True, capture_output=True)

        if len(output.stderr.decode("utf-8")) > 0:
            raise Exception("Got error '%s' while executing '%s'" % (output.stderr.decode("utf-8"), cmd))

        differences = output.stdout.decode("utf-8").splitlines()

        # Each difference found must be accepted by any of the whitelisting rules provided for this file
        for difference in differences:
            if __validate_difference(difference, whitelisted_patterns) is True:
                continue

            raise Exception("Difference '%s' found on [%s, %s] for file '%s'" % (difference, node_a, node_b, file_path))

    return True


def __validate_difference(difference, whitelisted_patterns):
    for pattern in whitelisted_patterns:
        if re.fullmatch(pattern, difference) is not None:
            return True

    return False


def are_configuration_files_aligned():
    files_to_check = OUtils.Kafka.get_configuration_files()

    for file in files_to_check:
        file_path = file["file_path"]
        whitelisted_patterns = file["whitelisted_patterns"]

        if __is_file_aligned_across_nodes(file_path=file_path, whitelisted_patterns=whitelisted_patterns) is False:
            return False

    return True


def leaders_even_distribution(topic):
    partitions_metadata = OUtils.Kafka.get_partitions_metadata(topic)

    leaders_list = [partition_metadata.leader for partition_metadata in partitions_metadata.values()]

    return len(set(leaders_list)) == len(leaders_list)
