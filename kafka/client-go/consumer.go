package main

import (
	"fmt"

	"github.com/confluentinc/confluent-kafka-go/kafka"
)

func main() {
	consumer, err := kafka.NewConsumer(&kafka.ConfigMap{
		"client.id":         "consumer-go",
		"group.id":          "consumer-foo",
		"bootstrap.servers": "localhost:9080,localhost:9081,localhost:9082",
	})
	if err != nil {
		panic(err)
	}
	consumer.Subscribe("foo", nil)
	defer consumer.Close()

	for {
		message, err := consumer.ReadMessage(-1)
		if err != nil {
			fmt.Printf("Consumer error: %v (%v)\n", err, message)
			continue
		}
		fmt.Printf("%v-%v key: %v value: %v\n",
			*message.TopicPartition.Topic,
			message.TopicPartition.Partition,
			string(message.Key), string(message.Value),
		)
	}
}
