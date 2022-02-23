package main

import (
	"fmt"
	"math/rand"
	"time"

	"github.com/confluentinc/confluent-kafka-go/kafka"
)

func main() {
	producer, err := kafka.NewProducer(&kafka.ConfigMap{
		"client.id":         "producer-go",
		"bootstrap.servers": "localhost:9080,localhost:9081,localhost:9082",
	})
	if err != nil {
		panic(err)
	}

	defer producer.Close()
	defer producer.Flush(5000)

	for {
		topic := "foo"
		nextMessage := time.Now().Format(time.UnixDate)[11:19]
		fmt.Println("producing: key: golang, value:", nextMessage)
		producer.Produce(
			&kafka.Message{
				TopicPartition: kafka.TopicPartition{Topic: &topic, Partition: kafka.PartitionAny},
				Key:            []byte("golang"), Value: []byte(nextMessage)},
			nil,
		)
		time.Sleep(time.Duration(1+9*rand.Float64()) * time.Second)
	}
}
