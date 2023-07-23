#![allow(incomplete_features)]
#![feature(async_closure)]
#![feature(generic_const_exprs)]

mod web;
mod math;

use leptos::*;

fn main() {
    mount_to_body(|cx| view! { cx, <App /> })
}

#[component]
fn App(cx: Scope) -> impl IntoView {
    let canvas_ref = create_node_ref::<html::Canvas>(cx);
    // let (canvas, setCanvas) = create_signal(cx, None);
    let (canvas, setCanvas) = create_signal(cx, 0);
    // create_effect(cx, move |_| setCanvas(canvas_ref.get()));

    create_resource(cx, canvas, async move |canvas| {
        let c = canvas_ref.get().unwrap();
        web_sys::console::log_1(&c);
        let webgpu = web::webgpu::WebGpu::new(canvas_ref.get()).await.unwrap();
        webgpu.print();
        webgpu.print();
        web::webgpu::draw(
            &webgpu,
            matrix!(VR[0.0 0.3 0.7 1.0]).transpose().transpose(),
        );
        if let 0 = canvas {
            log!("None");
            return;
        }
        log!("Some");
    });

    // create_effect(cx, move |_| {
    //     log!("1");
    //     log!("hello");
    // });

    view! { cx, <canvas _ref=canvas_ref /> }
}
