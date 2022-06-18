import { listen } from './listener'
import { send } from './sender'

if (!process.env.PROJECT_ID) throw new Error('PROJECT_ID environment variable is required.')
if (!process.env.APP_ID) throw new Error('APP_ID environment variable is required.')
if (!process.env.APP_REGION) throw new Error('APP_REGION environment variable is required.')
if (!process.env.ACCESS_KEY) throw new Error('ACCESS_KEY environment variable is required.')
if (!process.env.ACCESS_SECRET) throw new Error('ACCESS_SECRET environment variable is required.')

const credentials = { key: process.env.ACCESS_KEY, secret: process.env.ACCESS_SECRET }
const region = process.env.APP_REGION as 'eu' | 'us'

listen(3000, request => {
    console.log(request)
    const { project_id, app_id, message } = request
    if (!message) return
    send(true, credentials, region, project_id, app_id, message.contact_id, {
        text_message: { text: 'message received' },
    })
})
