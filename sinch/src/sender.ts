import { Buffer } from 'buffer'
import { ProviderMessage } from './message'

/**
 * Sinch Conversation API currently supported regions.
 */
type Region = 'eu' | 'us'

/**
 * Conversation API endpoint URL.
 * The first parameter of the template is the endpoint `Region`, the second is the project id.
 */
type SendRequestURL =
    | `https://${Region}.conversation.api.sinch.com/v1/projects/${string}/messages:send`
    | `https://api.${Region}1tst.conversation-api.staging.sinch.com/v1/projects/${string}/messages:send`

/**
 * Conversation API send message type.
 */
type SendRequest = {
    app_id: string
    recipient:
        | { contact_id: string }
        | { identified_by: { channel_entities: { app_id?: string; identity: string; channel: string }[] } }
    message: ProviderMessage & {
        explicit_channel_message?: { [key: string]: any }
        additionalProperties?: { contact_name?: string }
    }
    project_id?: string
    callback_url?: string
    channel_priority_order?: string[]
    channel_properties?: { [property: string]: string }
    message_metadata?: string
    conversation_metadata?: object
    queue?: 'NORMAL_PRIORITY' | 'HIGH_PRIORITY'
    ttl?: string
    processing_strategy?: 'DEFAULT' | 'DISPATCH_ONLY'
}

/**
 * Conversation API send message response type.
 */
export type SendResponse = {
    message_id: string
    accepted_time: string | Date
}

/**
 * Send a message to a contact using the Sinch Conversation API.
 *
 * @param staging If credentials belong to a staging account.
 * @param credentials API credentials. Access keys can be created at https://dashboard.sinch.com/settings/access-keys.
 * @param region The region depends on the app, available at https://dashboard.sinch.com/convapi/overview.
 * @param projectId Project id. The project id can be found at https://dashboard.sinch.com/settings/access-keys.
 * @param appId App ids can be found at https://dashboard.sinch.com/convapi/overview.
 * @param contactId Contact to send message to, usually obtained from already received messages.
 * @param message Message content to be sent.
 * @returns The response from the Conversation API containing the message id and accepted time.
 * @throws If the request fails.
 */
export const send = async (
    staging: boolean,
    credentials: { key: string; secret: string },
    region: Region,
    projectId: string,
    appId: string,
    contactId: string,
    message: SendRequest['message'],
) => {
    const url: SendRequestURL = !staging
        ? `https://${region}.conversation.api.sinch.com/v1/projects/${projectId}/messages:send`
        : `https://api.${region}1tst.conversation-api.staging.sinch.com/v1/projects/${projectId}/messages:send`
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            Authorization: `Basic ${Buffer.from(`${credentials.key}:${credentials.secret}`).toString('base64')}`,
        },
        body: JSON.stringify({ app_id: appId, recipient: { contact_id: contactId }, message } as SendRequest),
    })
    if (!response.ok) throw new Error(`${response.status} ${response.statusText}`)
    return (await response.json()) as SendResponse
}
