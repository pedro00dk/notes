kafka-topics.sh --bootstrap-server localhost:9090 --create --topic dcp

kafka-topics.sh --bootstrap-server localhost:9093 --list

kafka-console-producer.sh --broker-list localhost:9092 --topic dcp

kafka-console-consumer.sh --bootstrap-server kafka-0:9090 --topic dcp --from-beginning
