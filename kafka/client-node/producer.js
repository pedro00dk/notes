import { Kafka } from 'kafkajs'

const kafka = new Kafka({
    clientId: 'producer-node',
    brokers: ['localhost:10200', 'localhost:10201', 'localhost:10202'],
})

const producer = kafka.producer()
await producer.connect()

process.on('SIGINT', async () => {
    console.log('Caught interrupt signal')
    await producer.disconnect()
    process.exit()
})

while (true) {
    const nextMessage = { key: 'node', value: new Date().toString().split(' ')[4] }
    console.log('producing:', nextMessage)
    await producer.send({ topic: 'foo', messages: [nextMessage] })
    await new Promise(resolve => setTimeout(resolve, 1000 + 9000 * Math.random()))
}
