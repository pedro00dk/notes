import * as bindgen from './index_bg'
import wasmInit from './index_bg.wasm?init'

import featherSpriteUrl from 'feather-icons/dist/feather-sprite.svg?url'
import { editor } from 'monaco-editor'

const imports = {
    './index_bg.js': bindgen,
    'feather-icons': { sprite: (name: string) => `${featherSpriteUrl}#${name}` },
    'monaco-editor': { editor: () => editor },
}

bindgen.__wbg_set_wasm((await wasmInit({ ...imports })).exports)
bindgen.mount()
