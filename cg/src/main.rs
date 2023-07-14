#![feature(generic_const_exprs)]
#![cfg(web_sys_unstable_apis)]

mod math;
mod raytrace;

use js_sys::{Uint8ClampedArray, WebAssembly};
use leptos::*;
use wasm_bindgen::prelude::*;
use web_sys::GpuCanvasContext;

fn main() {
    mount_to_body(|cx| view! { cx, <App /> })
}

#[component]
fn App(cx: Scope) -> impl IntoView {
    let canvas_ref = create_node_ref::<html::Canvas>(cx);

    create_effect(cx, move |_| {
        let canvas = canvas_ref.get();
        if let None = canvas {
            return;
        }
        let ctx = canvas
            .unwrap()
            .get_context("webgpu")
            .unwrap()
            .unwrap()
            .unchecked_into::<GpuCanvasContext>();

        // ctx.
        log!("hello");
    });

    view! { cx, <canvas _ref=canvas_ref /> }
}
