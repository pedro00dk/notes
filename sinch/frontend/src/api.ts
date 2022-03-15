export const API_ENDPOINT = import.meta.env['VITE_API_ENDPOINT']

// if (!API_ENDPOINT) throw new Error('API_ENDPOINT not set')

export const api = (path: string) => `${API_ENDPOINT}${path}`
