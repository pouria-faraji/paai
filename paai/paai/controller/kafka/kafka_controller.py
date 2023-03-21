from confluent_kafka import KafkaException
from confluent_kafka.admin import AdminClient, NewTopic


class KafkaController:
    """
    Class for methods related to kafka operations
    """
    def __init__(self, configs) -> None:
        self._admin_client = AdminClient(configs)

    def create_topic(self, topic:str):
        """
        Function to create topics
        """
        topics = [topic]
        new_topics = [NewTopic(topic, num_partitions=1, replication_factor=1) for topic in topics]
        futures = self._admin_client.create_topics(new_topics)
        # Wait for each operation to finish.
        for topic, future in futures.items():
            try:
                future.result()  # The result itself is None
                print("Topic {} created".format(topic))
            except KafkaException as ex:
                print("Failed to create topic {}: {}".format(topic, ex))
