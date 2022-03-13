import { differenceInCalendarDays, isToday } from 'date-fns'

export const formatTime = Intl.DateTimeFormat('en-US', { hour12: true, hour: '2-digit', minute: '2-digit' })
export const formatWeek = Intl.DateTimeFormat('en-US', { weekday: 'long' })
export const formatDate = Intl.DateTimeFormat('en-US', { day: '2-digit', month: '2-digit', year: 'numeric' })

/**
 * Print `date` with different formats depending on the current date.
 * If it is the same day, prints the time, if is within the last week, prints the weekday, otherwise prints the date.
 * If `date` is in the future, excluding the current day, prints the date.
 *
 * @param date Date to be printed.
 * @returns String representation of `date`.
 */
export const formatElapsed = (date: Date) =>
    differenceInCalendarDays(new Date(), date) < 0
        ? formatDate.format(date)
        : isToday(date)
        ? formatTime.format(date)
        : differenceInCalendarDays(new Date(), date) < 7
        ? formatWeek.format(date)
        : formatDate.format(date)
