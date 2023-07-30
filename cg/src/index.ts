import * as bindgen from './index_bg'
import wasmInit from './index_bg.wasm?init'

import 'feather-icons'
import { editor } from 'monaco-editor'

const imports = {
    './index_bg.js': bindgen,
    'monaco-editor': { editor: () => editor },
}

bindgen.__wbg_set_wasm((await wasmInit({ ...imports })).exports)
bindgen.mount()
