package webhook

import (
	"encoding/json"
	"example/chat/pkg"
	"log"
	"net/http"
	"strconv"
	"sync"
	"time"
)

// Sinch Conversation API incoming requests struct.
//
// This struct is used for the unmarshal of user message requests (Message field) and also for message delivery
// notifications (Message_delivery_report field).
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

// Http server handler used as webhook for the Sinch Conversation API.
type Endpoint struct {
	OnRequest func(message ListenRequest) // Callback function used to handle incoming requests.
	Server    *http.Server                // Http server used to listen requests, populated when `Listen` is called.
	Waiter    *sync.WaitGroup             // Wait group for the shutdown, populated when `Listen` is called.
}

// Set up the endpoint server and start listening request on `port`.
//
// - `port`: Port number to listen requests on.
// - `wait`: Block the current thread until the server is shutdown.
func (endpoint *Endpoint) Listen(port int, wait bool) {
	endpoint.Server = &http.Server{Addr: ":" + strconv.Itoa(port), Handler: endpoint}
	endpoint.Waiter = &sync.WaitGroup{}
	log.Printf("server listening at %v\n", port)
	endpoint.Waiter.Add(1)
	go func() {
		endpoint.Server.ListenAndServe()
		log.Println("server stopped")
		endpoint.Waiter.Done()
	}()
	if wait {
		endpoint.Waiter.Wait()
	}
}

func (endpoint *Endpoint) ServeHTTP(response http.ResponseWriter, request *http.Request) {
	var message ListenRequest
	json.NewDecoder(request.Body).Decode(&message)
	response.WriteHeader(http.StatusOK)
	endpoint.OnRequest(message)
}
