import React from 'react'
import iconFacebook from '../image/icon-facebook.svg'
import iconKakaotalk from '../image/icon-kakaotalk.svg'
import iconTelegram from '../image/icon-telegram.svg'
import iconWhatsapp from '../image/icon-whatsapp.svg'

/**
 * Enumeration containing a non-exhaustive list of channels.
 */
export type Channel =
    | 'INSTAGRAM'
    | 'KAKAOTALK'
    | 'LINE'
    | 'MESSENGER'
    | 'MMS'
    | 'RCS'
    | 'SMS'
    | 'TELEGRAM'
    | 'VIBER'
    | 'VIBERBM'
    | 'WECHAT'
    | 'WHATSAPP'

/**
 * Channel icons.
 */
export const icon: Partial<{ [channel in Channel]: React.ReactElement }> = {
    MESSENGER: React.createElement('img', { src: iconFacebook, alt: 'messenger' }),
    KAKAOTALK: React.createElement('img', { src: iconKakaotalk, alt: 'kakaotalk' }),
    TELEGRAM: React.createElement('img', { src: iconTelegram, alt: 'telegram' }),
    WHATSAPP: React.createElement('img', { src: iconWhatsapp, alt: 'whatsapp' }),
}
