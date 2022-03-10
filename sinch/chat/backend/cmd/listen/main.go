package main

import (
	"encoding/json"
	"example/chat/pkg"
	"fmt"
	"log"
	"net/http"
	"strconv"
	"time"
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

func Listen(port int, onRequest func(message ListenRequest)) {
	server := http.Server{Addr: ":" + strconv.Itoa(port), Handler: &handler{onRequest}}
	log.Fatal(server.ListenAndServe())
}

func main() {
	Listen(3000, func(request ListenRequest) {
		x := request.Message.Contact_message
		fmt.Printf("%T\n", x)
		fmt.Println(x)
	})
}
