/**
 * Utilities for printing dates.
 */

import { differenceInCalendarDays } from 'date-fns'

export const formatTime = Intl.DateTimeFormat('en-US', { hour12: true, hour: '2-digit', minute: '2-digit' })
export const formatWeek = Intl.DateTimeFormat('en-US', { weekday: 'long' })
export const formatDate = Intl.DateTimeFormat('en-US', { day: '2-digit', month: '2-digit', year: 'numeric' })

/**
 * Print `date` with different formats depending on the current date.
 * If it is the same day, prints the time, if is within the last week, prints the weekday, otherwise prints the date.
 * If `date` is in the future, excluding the current day, prints the date.
 *
 * @param date Date to be printed.
 * @param from Base date to check difference, defaults to `new Date()`.
 * @returns String representation of `date`.
 */
export const formatElapsed = (date: Date, from = new Date()) => {
    const difference = differenceInCalendarDays(new Date(), from)
    ;(!difference ? formatTime : difference > 0 && difference < 7 ? formatWeek : formatDate).format(date)
}
