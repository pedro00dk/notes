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
                    messageDate: new Date(2020, 1, 1, 10, 0, 0),
                },
                {
                    name: 'Pedro Henrique',
                    channel: 'MESSENGER',
                    lastMessage: 'Olá, tudo bem?',
                    messageDate: new Date(2020, 1, 1, 10, 0, 0),
                },
                {
                    name: 'Pedro Henrique',
                    channel: 'MESSENGER',
                    lastMessage: 'Olá, tudo bem?',
                    messageDate: new Date(2020, 1, 1, 10, 0, 0),
                },
            ]}
            onSelect={() => {}}
        />
        <div>chat</div>
    </main>
)
