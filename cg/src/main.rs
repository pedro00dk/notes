use leptos::*;
// use js_sys::
use wasm_bindgen::JsCast;
use web_sys::CanvasRenderingContext2d;

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
            .get_context("2d")
            .unwrap()
            .unwrap()
            .dyn_into::<CanvasRenderingContext2d>()
            .unwrap();
        ctx.fill_rect(10.0, 10.0, 100.0, 70.0);
        log!("hello");
    });

    view! { cx, <canvas _ref=canvas_ref /> }
}
