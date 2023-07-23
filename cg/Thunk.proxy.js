const http = require('http')
const { argv } = require('process')

const args = argv.slice(argv.indexOf(__filename) + 1)
const [proxyPort, targetPort] = args[0].split(':').map(port => +port)
const injectHeaders = args.slice(1).map(header => header.split(':'))

const server = http.createServer((req, res) => {
    const options = { hostname: 'localhost', port: targetPort, path: req.url, method: req.method, headers: req.headers }
    const proxyRequest = http.request(options, proxyResponse => {
        injectHeaders.forEach(([name, value]) => (proxyResponse.headers[name.toLowerCase()] = value))
        res.writeHead(proxyResponse.statusCode, proxyResponse.headers)
        proxyResponse.pipe(res, { end: true })
    })
    req.pipe(proxyRequest, { end: true })
})

server.listen(proxyPort, () => console.log(`${' '.repeat(33)} 📡 proxy  listening at http://127.0.0.1:${proxyPort}`))
