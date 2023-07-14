# Computer Graphics

Collection of CG algorithms and techniques written in rust and compiled to the web.

## Installation

Check [asdf](https://asdf-vm.com) `.tool-versions` for required languages tools.

The following block describes other tools and procedures required to run the project.

```shell
cd ./cg/

$ # rust nightly is recommended by leptos
$ # wasm target required to compile for web
$ rustup toolchain install nightly
$ rustup default nightly
$ rustup target add wasm32-unknown-unknown

$ # trunk is a WASM bundler for the web
$ # https://crates.io/crates/trunk
$ cargo install trunk
```

## Running

Run `trunk serve` to start a development server and access `http://localhost:3000`.

The thunk dev server will start on port 3001, and a reverse proxy will also start and allow access on port 3000. The proxy is required because some web necessary features require HTTP headers to be provided, Thunk does not support adding extra headers to the responses.

The proxy (`Thunk.proxy.js`) is started and stopped together with Thunk using a Thunk hook (see `Thunk.toml`). The proxy required to enable shared memory features, more specifically `SharedArrayBuffer`, which is enabled by providing a couple headers in responses.
