import React from 'react'
import { Channel, icon } from '../util/channel'
import { formatElapsed } from '../util/time'
import classes from './Contacts.module.scss'

/**
 * Render an ordered list of contacts based on their last message date.
 *
 * @param props.contacts List of contacts and which contacts are selected.
 * @param props.onSelect Callback triggered when a contact is selected.
 */
export const Contacts = (props: {
    contacts: { name: string; channel: Channel; lastMessage: string; messageDate: Date; selected?: boolean }[]
    onSelect: (contact: any) => void
}) => (
    <aside className={classes.root}>
        <ol>
            {[...props.contacts]
                .sort((a, b) => +b.messageDate - +a.messageDate)
                .map(contact => (
                    <Contact {...contact} />
                ))}
        </ol>
    </aside>
)

/**
 * Render a contact card.
 *
 * @param props Contact information.
 * @see Contacts
 */
const Contact = (props: Parameters<typeof Contacts>['0']['contacts'][number]) => (
    <li key={`${props.name}-${props.channel}`} className={classes.contact}>
        <h5>{props.name}</h5>
        <h6>{formatElapsed(props.messageDate)}</h6>
        {icon[props.channel]}
        <span>{props.lastMessage}</span>
    </li>
)
