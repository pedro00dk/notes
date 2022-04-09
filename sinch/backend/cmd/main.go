package main

import (
	"encoding/json"
	"example/chat/pkg/kafka"
	"example/chat/pkg/webhook"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	serverPort, _ := strconv.Atoi(os.Getenv("SERVER_PORT"))
	kafkaBrokers := strings.Split(os.Getenv("KAFKA_BROKERS"), ",")
	kafkaTopic := os.Getenv("KAFKA_TOPIC")

	endpoint := &webhook.Endpoint{}
	client := kafka.NewClient("backend", "", kafkaTopic, kafkaBrokers)

	endpoint.OnRequest = func(request webhook.ListenRequest) {
		fmt.Println(request)
		client.Produce(kafkaTopic, "", request)
	}
	endpoint.Listen(serverPort, false)

	client.Consume(kafkaTopic, 0, func(message kafka.Message) {
		key := string(message.Key)
		var value interface{}
		json.Unmarshal(message.Value, &value)

		fmt.Printf("CONSUMMING: %v: %v\n", key, value)
	})

	endpoint.Waiter.Wait()
	client.Close()
}
