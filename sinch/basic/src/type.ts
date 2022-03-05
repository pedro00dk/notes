export type Channel =
    | 'INSTAGRAM'
    | 'KAKAOTALK'
    | 'LINE'
    | 'MESSENGER'
    | 'MMS'
    | 'RCS'
    | 'SMS'
    | 'TELEGRAM'
    | 'VIBER'
    | 'VIBERBM'
    | 'WECHAT'
    | 'WHATSAPP'

type TextMessage = { text_message: { text: string } }
type MediaMessage = { media_message: { url: string; thumbnail_url?: string } }
type LocationMessage = {
    location_message: { coordinates: { latitude: number; longitude: number }; title: string; label?: string }
}
type CallMessage = { call_message: { phone_number: string; title: string } }
type URLMessage = { text_message: { title: string; url: string } }
export type ChoiceMessage = {
    choice_message: { choices: (TextMessage | LocationMessage | CallMessage | URLMessage)[] } & Partial<TextMessage>
}
export type CardMessage = {
    card_message: {
        title: string
        description?: string
        height?: 'UNSPECIFIED_HEIGHT' | 'SHORT' | 'MEDIUM' | 'TALL'
        choices?: ChoiceMessage['choice_message']['choices']
    } & Partial<MediaMessage>
}
export type CarrouselMessage = {
    carrousel_message: { cards: CardMessage[]; choices?: ChoiceMessage['choice_message']['choices'] }
}

export type ContactMessage = TextMessage | MediaMessage | LocationMessage
export type ProviderMessage = ContactMessage | ChoiceMessage | CardMessage | CarrouselMessage
