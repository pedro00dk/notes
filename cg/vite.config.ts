import { execSync } from 'child_process'
import type { Plugin, UserConfig } from 'vite'

const wasmCompilePlugin = (): Plugin => ({
    name: 'wasmCompile',
    configureServer: async ({ config: { isProduction }, watcher }) => {
        const wasmCompile = () => {
            try {
                execSync(`npm run wasm:gen:${isProduction ? 'prd' : 'dev'}`, { stdio: 'inherit' })
            } catch {}
        }
        wasmCompile()
        watcher.on('change', file => void (file.endsWith('.rs') && wasmCompile()))
    },
})

export default {
    build: { target: 'esnext' },
    server: { port: 5000 },
    plugins: [wasmCompilePlugin()],
} as UserConfig
