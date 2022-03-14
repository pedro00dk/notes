import React from 'react'
import { cl } from '../../util/class'
import classes from './Input.module.scss'

export type InputProps = {
    size?: 'small' | 'medium' | 'large'
    left?: React.ReactNode
    right?: React.ReactNode
    rootProps?: React.ComponentPropsWithRef<'div'>
} & React.ComponentPropsWithRef<'input'>

/**
 * Decorated input component with extensible layout.
 *
 * @see InputProps
 */
export const Input = React.forwardRef<
    HTMLInputElement,
    InputProps
    //
>(({ size = 'medium', left, right, rootProps, ...props }, ref) => {
    const input$ = React.useRef<HTMLInputElement | null>()

    return (
        <div
            {...rootProps}
            className={cl(classes.root, classes.theme, classes[size], rootProps?.className)}
            onClick={e => (input$.current?.focus(), rootProps?.onClick?.(e))}
        >
            {left}
            <input
                ref={r => (ref && typeof ref === 'object' ? (ref.current = r) : ref?.(r), (input$.current = r))}
                {...props}
            />
            {right}
        </div>
    )
})
