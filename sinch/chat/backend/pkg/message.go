package pkg

// This module contains struct definitions that compose the message interface used by Sinch Conversation API.
// Extensive message documentation can be found at https://developers.sinch.com/docs/conversation/message-types/

type TextMessage struct {
	Text_message struct {
		Text string `json:"text"`
	} `json:"text_message"`
}

type MediaMessage struct {
	Media_message struct {
		Url           string `json:"url"`
		Thumbnail_url string `json:"thumbnail_url"`
	} `json:"media_message"`
}

type LocationMessage struct {
	Location_message struct {
		Title       string `json:"title"`
		Label       string `json:"label"`
		Coordinates struct {
			Latitude  float64 `json:"latitude"`
			Longitude float64 `json:"longitude"`
		} `json:"coordinates"`
	} `json:"location_message"`
}

type CallMessage struct {
	Call_message struct {
		Title        string `json:"title"`
		Phone_number string `json:"phone_number"`
	} `json:"call_message"`
}

type URLMessage struct {
	Url_message struct {
		Title string `json:"title"`
		Url   string `json:"url"`
	} `json:"url_message"`
}

type Choice struct {
	*TextMessage
	*MediaMessage
	*LocationMessage
	*CallMessage
	*URLMessage
}

type ChoiceMessage struct {
	Choice_message struct {
		Text_message TextMessage `json:"text_message"`
		Choices      [3]Choice   `json:"choices"`
	} `json:"choice_message"`
}

type CardMessage struct {
	Card_message struct {
		Title         string    `json:"title"`
		Description   string    `json:"description"`
		Height        string    `json:"height"`
		Choices       [3]Choice `json:"choices"`
		*MediaMessage `json:"mediamessage"`
	} `json:"card_message"`
}

type CarrouselMessage struct {
	Carrousel_message struct {
		Cards   [10]*CardMessage `json:"cards"`
		Choices [3]Choice        `json:"choices"`
	} `json:"carrousel_message"`
}

// ContactMessage is a union of message types that can be sent by a contact.
// It might be a simple text message, any king of file or media, or a location.
type ContactMessage struct {
	*TextMessage
	*MediaMessage
	*LocationMessage
}

// ProviderMessage is a union of message types that can be sent by a provider.
// It can send everyhing contact can send, plus a choice messages, decorated cards and carrousel with multiple messages.
type ProviderMessage struct {
	*TextMessage
	*MediaMessage
	*LocationMessage
	*ChoiceMessage
	*CardMessage
	*CarrouselMessage
}
