import * as bindgen from './index_bg'
import wasmInit from './index_bg.wasm?init'

document.body.appendChild(document.createElement('span')).textContent = 'hello world!'

const wasmModule = await wasmInit({ './index_bg.js': bindgen })
bindgen.__wbg_set_wasm(wasmModule.exports)
bindgen.mount()
