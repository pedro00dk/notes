import { subDays } from 'date-fns'
import React from 'react'
import classes from './App.module.scss'
import { Contacts } from './Contacts'

export const App = () => (
    <main className={classes.root}>
        <Contacts
            contacts={[
                {
                    name: 'Pedro Henrique',
                    channel: 'MESSENGER',
                    lastMessage: 'Olá, tudo bem?',
                    messageDate: subDays(new Date(), -2),
                },
                {
                    name: 'Pedro Henrique',
                    channel: 'WHATSAPP',
                    lastMessage: 'Olá, tudo bem?',
                    messageDate: subDays(new Date(), -1),
                },
                {
                    name: 'Pedro Henrique',
                    channel: 'KAKAOTALK',
                    lastMessage: 'Olá, tudo bem?',
                    messageDate: new Date(),
                },
                {
                    name: 'Pedro Henrique',
                    channel: 'TELEGRAM',
                    lastMessage: 'Olá, tudo bem?',
                    messageDate: subDays(new Date(), 1),
                },
                {
                    name: 'Pedro Henrique',
                    channel: 'MESSENGER',
                    lastMessage: 'Olá, tudo bem?',
                    messageDate: subDays(new Date(), 2),
                },
                {
                    name: 'Pedro Henrique',
                    channel: 'MESSENGER',
                    lastMessage: 'Olá, tudo bem?',
                    messageDate: subDays(new Date(), 3),
                },
                {
                    name: 'Pedro Henrique',
                    channel: 'MESSENGER',
                    lastMessage: 'Olá, tudo bem?',
                    messageDate: subDays(new Date(), 4),
                },
                {
                    name: 'Pedro Henrique',
                    channel: 'MESSENGER',
                    lastMessage: 'Olá, tudo bem?',
                    messageDate: subDays(new Date(), 5),
                },
                {
                    name: 'Pedro Henrique',
                    channel: 'MESSENGER',
                    lastMessage: 'Olá, tudo bem?',
                    messageDate: subDays(new Date(), 6),
                },
                {
                    name: 'Pedro Henrique',
                    channel: 'MESSENGER',
                    lastMessage: 'Olá, tudo bem?',
                    messageDate: subDays(new Date(), 7),
                },
                {
                    name: 'Pedro Henrique',
                    channel: 'MESSENGER',
                    lastMessage: 'Olá, tudo bem?',
                    messageDate: subDays(new Date(), 8),
                },
                {
                    name: 'Pedro Henrique',
                    channel: 'MESSENGER',
                    lastMessage: 'Olá, tudo bem?',
                    messageDate: subDays(new Date(), 9),
                },
            ]}
            onSelect={() => {}}
        />
        <div>chat</div>
    </main>
)
