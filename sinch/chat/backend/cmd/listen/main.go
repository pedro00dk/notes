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
	App_id           string
	Accepted_time    time.Time
	Event_time       time.Time
	Message_metadata string
	Message          struct {
		Id               string
		Sender_id        string
		Contact_id       string
		Conversation_id  string
		Accept_time      time.Time
		Direction        pkg.Direction
		Processing_mode  pkg.ProcessingMode
		Metadata         string
		Channel_identity struct {
			App_id   int
			Identity string
			Channel  pkg.Channel
		}
		Contact_message pkg.ContactMessage
	}
	Message_delivery_report struct {
		Message_id       string
		Contact_id       string
		Conversation_id  string
		Processing_mode  pkg.ProcessingMode
		Status           pkg.Status
		Metadata         string
		Channel_identity struct {
			App_id   int
			Identity string
			Channel  pkg.Channel
		}
	}
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
