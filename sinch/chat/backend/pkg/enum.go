package pkg

// This module contains common enumerations used by Sinch Conversation API.

// Channel enumerates the available channel providers.
type Channel string

const (
	ChannelInstagram Channel = "INSTAGRAM"
	ChannelKakaoTalk Channel = "KAKAOTALK"
	ChannelLine      Channel = "LINE"
	ChannelMessenger Channel = "MESSENGER"
	ChannelMms       Channel = "MMS"
	ChannelRcs       Channel = "RCS"
	ChannelSms       Channel = "SMS"
	ChannelTelegram  Channel = "TELEGRAM"
	ChannelViber     Channel = "VIBER"
	ChannelViberBM   Channel = "VIBERBM"
	ChannelWechat    Channel = "WECHAT"
	ChannelWhatsapp  Channel = "WHATSAPP"
)

type Direction string

const (
	DirectionToApp Direction = "TO_APP"
)

type ProcessingMode string

const (
	ProcessingModeConversation ProcessingMode = "TO_APP"
)

type Status string

const (
	StatusQueuedOnChannel Status = "QUEUED_ON_CHANNEL"
	StatusDelivered       Status = "DELIVERED"
)
