package pkg

// This module contains struct definitions that compose the message interface used by Sinch Conversation API.
// Extensive message documentation can be found at https://developers.sinch.com/docs/conversation/message-types/

type TextMessage struct {
	Text_message struct {
		Text string
	}
}

type MediaMessage struct {
	Media_message struct {
		Url           string
		Thumbnail_url string
	}
}

type LocationMessage struct {
	Location_message struct {
		Title       string
		Label       string
		Coordinates struct {
			Latitude  float64
			Longitude float64
		}
	}
}

type CallMessage struct {
	Call_message struct {
		Title        string
		Phone_number string
	}
}

type URLMessage struct {
	Url_message struct {
		Title string
		Url   string
	}
}

type Choice struct {
	TextMessage
	MediaMessage
	LocationMessage
	CallMessage
	URLMessage
}

type ChoiceMessage struct {
	Choice_message struct {
		Text    string
		Choices [3]Choice
	}
}

type CardMessage struct {
	Card_message struct {
		Title       string
		Description string
		Height      string
		Choices     [3]Choice
		MediaMessage
	}
}

type CarrouselMessage struct {
	Carrousel_message struct {
		Cards   [10]CardMessage
		Choices [3]Choice
	}
}

// ContactMessage is a union of message types that can be sent by a contact.
// It might be a simple text message, any king of file or media, or a location.
type ContactMessage struct {
	TextMessage
	MediaMessage
	LocationMessage
}

// ProviderMessage is a union of message types that can be sent by a provider.
// It can send everyhing contact can send, plus a choice messages, decorated cards and carrousel with multiple messages.
type ProviderMessage struct {
	TextMessage
	MediaMessage
	LocationMessage
	ChoiceMessage
	CardMessage
	CarrouselMessage
}
