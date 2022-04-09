import express from 'express'
import { ContactMessage } from './message'

/**
 * Conversation API message type sent to webhooks.
 */
type ListenRequest = {
    project_id: string
    app_id: string
    event_time: string | Date
    accepted_time: string | Date
    message_metadata: string
    message?: {
        id: string
        sender_id: string
        contact_id: string
        conversation_id: string
        channel_identity: { app_id: string; identity: string; channel: string }
        accept_time: string | Date
        direction: 'TO_APP'
        processing_mode: 'CONVERSATION'
        metadata: string
        contact_message: ContactMessage
    }
    message_delivery_report?: {
        message_id: string
        contact_id: string
        conversation_id: string
        channel_identity: { app_id: string; identity: string; channel: string }
        processing_mode: 'CONVERSATION'
        metadata: ''
        status: 'QUEUED_ON_CHANNEL' | 'DELIVERED'
    }
}

/**
 * Listen for messages from Sinch Conversation API and trigger `callback` when new messages are received.
 * The server is started automatically and listens on `port`.
 *
 * @param port Server port to listen on.
 * @param onRequest Callback triggered when a new message is received.
 * @returns The http server.
 */
export const listen = (port: number, onRequest: (request: ListenRequest) => void) => {
    const app = express()
    app.use(express.json())
    app.post('/', (request, response) => (response.sendStatus(200), onRequest(request.body)))
    return app.listen(port, () => console.log(`listening at http://localhost:${port}`))
}
