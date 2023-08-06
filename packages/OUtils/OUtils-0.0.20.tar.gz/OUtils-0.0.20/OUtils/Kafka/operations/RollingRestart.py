import OUtils.Kafka

import subprocess
import time


class RollingRestart:

    def __init__(self):
        pass

    def __verify_cluster_clean_state(self):
        assert OUtils.Kafka.checks.are_configuration_files_aligned() is True, "Configuration files not aligned"
        assert OUtils.Kafka.metrics.get_total_under_replicated_replicas() == 0, "There are under-replicated replicas"

        return True

    def __get_confirmation(self, string):
        confirmation = input(string)

        if confirmation.lower() in ["yes", "y"]:
            return True

        return False

    def __execute_kafka_service_restart(self, node):
        subprocess.run("bash -c \"ssh root@%s 'systemctl restart kafka'\"" % node, shell=True, check=True)

        return True

    def execute(self, skip_files_check=False):
        try:
            # Step 1
            if self.__get_confirmation("Please confirm restarting '%s': " % OUtils.Kafka.get_nodes()) is False:
                print("Rolling restart aborted")
                return

            # Step 2
            print("Verifying clean cluster status before restart ...")

            if (skip_files_check is False) and (self.__verify_cluster_clean_state() is True):
                print("\tOK")
            else:
                print("\tSkipped")

            # Step 3
            print("Executing rolling restart ...")

            for node in OUtils.Kafka.get_nodes():

                # Step 3a: restart service
                print("\tOn node %s: Restarting Kafka service ..." % node)
                if self.__execute_kafka_service_restart(node) is True:
                    print("\t\tOK")

                # Step 3b: check that cluster status returns to clean
                print("\tOn node %s: Checking under-replication ..." % node)

                for attempt in range(10):
                    time.sleep(5)

                    try:
                        under_replicated_replicas = OUtils.Kafka.metrics.get_total_under_replicated_replicas()

                    except ConnectionError:
                        print("\t\tFailed to connect. Will re-try.")
                        continue

                    if under_replicated_replicas == 0:
                        print("\t\tOK: No under-replicated replicas found: system stabilized back.\n")
                        break

                    print("\t\tFound %d under-replicated partitions." % under_replicated_replicas)
                    continue

                if under_replicated_replicas != 0:
                    raise Exception("System did not stabilize back after several attempts")

            print("Rolling restart completed.")
            return True

        except Exception as err:
            print("An exception occurred and the rolling restart was interrupted. Please verify cluster status.")
            print(str(err))
            return False
