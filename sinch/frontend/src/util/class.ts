/*
 * Utilities for working with CSS classes.
 */

/**
 * Join classes contained in strings and objects.
 *
 * For objects, keys are used as classes, the key is only added if its value is truthy.
 * Other types of properties are stringified in order to obtain class strings.
 *
 * @param cl Classes to join.
 * @returns Resulting classes string.
 */
export const cl = (...cl: (string | { [cl: string]: any } | any)[]) =>
    cl
        .map(c => (typeof c !== 'object' ? c : Object.keys(c).filter(k => c[k])))
        .flat()
        .join(' ')
