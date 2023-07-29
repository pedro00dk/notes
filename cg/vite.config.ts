import { execSync } from 'child_process'
import type { Plugin, UserConfig } from 'vite'

function wasmCompile(): Plugin {
    return {
        name: 'wasmCompile',
        configureServer: async server => {
            server.watcher.on('change', file => {
                if (!file.endsWith('.rs')) return
                console.log(file)
                execSync(`npm run wasm:gen:${server.config.isProduction ? 'prd' : 'dev'}`, { stdio: 'inherit' })
            })
        },
    }
}

export default {
    server: { port: 5000 },
    plugins: [wasmCompile()],
} as UserConfig
