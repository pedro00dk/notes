#![allow(incomplete_features)]
#![feature(async_closure)]
#![feature(generic_const_exprs)]

mod math;
mod web;

use leptos::*;

fn main() {
    mount_to_body(|cx| view! { cx, <App /> })
}

#[component]
fn App(cx: Scope) -> impl IntoView {
    let canvas_ref = create_node_ref::<html::Canvas>(cx);
    let (canvas, setCanvas) = create_signal(cx, 0);

    create_resource(cx, canvas, async move |canvas| {
        let webgpu = web::webgpu::WebGpu::new(canvas_ref.get()).await.unwrap();
        webgpu.print();
        web::webgpu::draw(&webgpu, matrix!(VR[0.0, 0.3, 0.7, 1.0]));
    });

    let x = matrix!(VR[10000u32,10001,10002,10003]);
    let a = &web::array::typed_u32(&x);
    web_sys::console::log_1(&a);
    web_sys::console::log_1(&js_sys::JSON::stringify(&a).unwrap());
    web_sys::console::log_1(&a);
    web_sys::console::log_1(&js_sys::JSON::stringify(&a).unwrap());

    view! { cx, <canvas _ref=canvas_ref /> }
}
