import React from 'react'
import classes from './Contacts.module.scss'
export const Contacts = (props: {
    contacts: { name: string; channel: string; lastMessage: string; messageDate: Date; selected?: boolean }[]
    onSelect: (contact: any) => void
}) => (
    <aside className={classes.root}>
        <ol>
            {[...props.contacts]
                .sort((a, b) => +a.messageDate - +b.messageDate)
                .map(({ name, channel, lastMessage, messageDate: messageDate }) => (
                    <li
                        key={`${name}-${channel}`}
                        className={classes.contact}
                        onClick={() => props.onSelect({ name, channel })}
                    >
                        <h5>{name}</h5>
                        <h6>{channel}</h6>
                        <h6>{messageDate.toString()}</h6>
                        <span>{lastMessage}</span>
                    </li>
                ))}
        </ol>
    </aside>
)
