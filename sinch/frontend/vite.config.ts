import pluginReactRefresh from '@vitejs/plugin-react-refresh'
import pluginAnalyzer from 'rollup-plugin-analyzer'
import { UserConfig } from 'vite'

const SERVER_PORT = process.env.SERVER_PORT
const PREVIEW_PORT = process.env.PREVIEW_PORT

const config: UserConfig = {
    root: './src/',
    publicDir: './public/',
    build: { outDir: '../build/', minify: 'esbuild', target: 'es2021' },
    server: { port: SERVER_PORT ? +SERVER_PORT : undefined },
    preview: { port: PREVIEW_PORT ? +PREVIEW_PORT : undefined },
    plugins: [pluginReactRefresh(), pluginAnalyzer()],
}

console.log(config)

export default config
