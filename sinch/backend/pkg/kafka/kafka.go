package kafka

import (
	"context"
	"encoding/json"

	kfk "github.com/segmentio/kafka-go"
)

type Client struct {
	Producer *kfk.Writer
	Consumer *kfk.Reader
	closed   bool
}

func NewClient(id string, group string, topic string, brokers []string) *Client {
	if len(brokers) == 0 {
		panic(1)
	}
	return &Client{
		Producer: kfk.NewWriter(kfk.WriterConfig{Brokers: brokers}),
		Consumer: kfk.NewReader(kfk.ReaderConfig{Brokers: brokers, Topic: topic}),
	}
}

func (client *Client) Produce(topic string, key string, value interface{}) error {
	data, err := json.Marshal(value)
	if err != nil {
		return err
	}
	return client.Producer.WriteMessages(context.Background(), kfk.Message{
		Topic: topic,
		Key:   []byte(key),
		Value: data,
	})
}

type Message = *kfk.Message

func (client *Client) Consume(topic string, offset int64, handler func(message *kfk.Message)) {
	client.Consumer.SetOffset(offset)
	for {
		message, err := client.Consumer.ReadMessage(context.Background())
		if err != nil {
			break
		}
		go handler(&message)
	}
}

func (client *Client) Close() {
	client.Producer.Close()
	client.Consumer.Close()
}
