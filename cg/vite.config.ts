import { execSync } from 'child_process'
import type { Plugin, UserConfig } from 'vite'

const wasmCompilePlugin = (): Plugin => ({
    name: 'wasmCompile',
    configureServer: async ({ config: { isProduction }, watcher }) => {
        const wasmCompile = () => execSync(`npm run wasm:gen:${isProduction ? 'prd' : 'dev'}`, { stdio: 'inherit' })
        wasmCompile()
        watcher.on('change', file => void (file.endsWith('.rs') && wasmCompile()))
    },
})

export default {
    server: { port: 5000 },
    plugins: [wasmCompilePlugin()],
} as UserConfig
