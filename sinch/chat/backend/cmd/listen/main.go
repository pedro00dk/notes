package main

import (
	"context"
	"encoding/json"
	"example/chat/pkg"
	"fmt"
	"log"
	"net/http"
	"os"
	"strconv"
	"strings"
	"time"

	"github.com/segmentio/kafka-go"
)

type ListenRequest struct {
	App_id           string    `json:"app_id"`
	Accepted_time    time.Time `json:"accepted_time"`
	Event_time       time.Time `json:"event_time"`
	Message_metadata string    `json:"message_metadata"`
	Message          *struct {
		Id               string             `json:"id"`
		Sender_id        string             `json:"sender_id"`
		Contact_id       string             `json:"contact_id"`
		Conversation_id  string             `json:"conversation_id"`
		Accept_time      time.Time          `json:"accept_time"`
		Direction        pkg.Direction      `json:"direction"`
		Processing_mode  pkg.ProcessingMode `json:"processing_mode"`
		Metadata         string             `json:"metadata"`
		Channel_identity struct {
			App_id   string      `json:"app_id"`
			Identity string      `json:"identity"`
			Channel  pkg.Channel `json:"channel"`
		} `json:"channel_identity"`
		Contact_message pkg.ContactMessage `json:"contact_message"`
	} `json:"message,omitempty"`
	Message_delivery_report *struct {
		Message_id       string             `json:"message_id"`
		Contact_id       string             `json:"contact_id"`
		Conversation_id  string             `json:"conversation_id"`
		Processing_mode  pkg.ProcessingMode `json:"processing_mode"`
		Status           pkg.Status         `json:"status"`
		Metadata         string             `json:"metadata"`
		Channel_identity struct {
			App_id   string      `json:"app_id"`
			Identity string      `json:"identity"`
			Channel  pkg.Channel `json:"channel"`
		} `json:"channel_identity"`
	} `json:"message_delivery_report,omitempty"`
}

type handler struct {
	onRequest func(message ListenRequest)
}

func (h *handler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	var message ListenRequest
	json.NewDecoder(r.Body).Decode(&message)
	w.WriteHeader(http.StatusOK)
	h.onRequest(message)
}

func listen(port int, onRequest func(message ListenRequest)) {
	server := http.Server{Addr: ":" + strconv.Itoa(port), Handler: &handler{onRequest}}
	log.Fatal(server.ListenAndServe())
}

func kafkaWriter(brokers []string, topic string, create bool) *kafka.Writer {
	if len(brokers) == 0 {
		log.Fatal("KAFKA_BROKERS is not set")
	}
	return &kafka.Writer{
		Addr:     kafka.TCP(brokers[0]),
		Topic:    topic,
		Balancer: &kafka.LeastBytes{},
	}
}

func main() {
	webhookPort, _ := strconv.Atoi(os.Getenv("WEBHOOK_PORT"))
	kafkaBrokers := strings.Split(os.Getenv("KAFKA_BROKERS"), ",")
	kafkaTopic := os.Getenv("KAFKA_TOPIC")
	kafkaCreate := os.Getenv("KAFKA_CREATE") == "true"
	writer := kafkaWriter(kafkaBrokers, kafkaTopic, kafkaCreate)
	defer writer.Close()
	listen(webhookPort, func(request ListenRequest) {
		fmt.Println(request)
		data, err := json.Marshal(request)
		if err != nil {
			data = []byte(err.Error())
		}
		err = writer.WriteMessages(context.Background(),
			kafka.Message{Value: data},
		)
		if err != nil {
			log.Fatal("failed to write message:", err)
		}
	})
}
