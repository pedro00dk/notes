use crate::components::editor::Editor;
use crate::math;
use crate::web;
use leptos::*;

#[component]
pub fn Index(cx: Scope) -> impl IntoView {
    let canvas_ref = create_node_ref::<html::Canvas>(cx);
    let (canvas, setCanvas) = create_signal(cx, 0);

    create_resource(cx, canvas, async move |canvas| {
        let webgpu = web::webgpu::WebGpu::new(canvas_ref.get()).await.unwrap();
        webgpu.print();
        web::webgpu::draw(&webgpu, math::mx!(VR[0.0, 0.3, 0.7, 1.0]));
    });

    view! { cx,
        <div>
            <canvas _ref=canvas_ref />
            <Editor language="wgsl" theme="vs-dark" />
        </div>
    }
}
