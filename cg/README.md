# Computer Graphics

Collection of CG algorithms and techniques written in rust and compiled to the web.

## Installation

Check [asdf](https://asdf-vm.com/) `.tool-versions` for required languages tools.

The following block describes other tools and procedures required to run the project.

```shell
cd ./cg/
$ # trunk is a WASM bundler for the web
$ # https://crates.io/crates/trunk
$ cargo install trunk

$ # rust nightly is recommended by leptos
$ # wasm target require to compile for web
$ rustup toolchain install nightly
$ rustup default nightly
$ rustup target add wasm32-unknown-unknown
```

## Running

Run `trunk serve --open` to start a development server.
