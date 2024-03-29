import { Kafka } from 'kafkajs'

const kafka = new Kafka({
    clientId: 'consumer-node',
    brokers: ['localhost:10200', 'localhost:10201', 'localhost:10202'],
})

const consumer = kafka.consumer({ groupId: 'consumer-foo' })
await consumer.connect()

process.on('SIGINT', async () => {
    console.log('Caught interrupt signal')
    await consumer.disconnect()
    process.exit()
})

await consumer.subscribe({ topic: 'foo', fromBeginning: true })
consumer.run({
    eachMessage: async ({ topic, partition, message }) =>
        console.log(`${topic}-${partition} key: ${message.key} value: ${message.value}`),
})
