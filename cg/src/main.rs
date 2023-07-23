#![allow(incomplete_features)]
#![feature(generic_const_exprs)]
// mod math;
// mod raytrace;

use leptos::*;
use wasm_bindgen::JsCast;
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
        web_sys::console::log_1(&ctx);
        log!("hello");
    });

    view! { cx, <canvas _ref=canvas_ref /> }
}
