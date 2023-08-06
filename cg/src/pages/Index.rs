use crate::components::editor::Editor;
use crate::components::player::Player;
use crate::math;
use crate::util::types::monaco_editor;
use crate::web;
use leptos::*;
use wasm_bindgen::prelude::*;

#[component]
pub fn Index(cx: Scope) -> impl IntoView {
    let canvas_ref = create_node_ref::<html::Canvas>(cx);
    let (canvas, setCanvas) = create_signal(cx, 0);
    let (editor, set_editor) = create_signal::<Option<monaco_editor::StandaloneCodeEditor>>(cx, None);

    create_resource(cx, canvas, async move |canvas| {
        let webgpu = web::webgpu::WebGpu::new(canvas_ref.get()).await.unwrap();
        webgpu.print();
        web::webgpu::draw(&webgpu, math::mx!(VR[0.0, 0.3, 0.7, 1.0]));
    });

    view! { cx,
        <div>
            <canvas _ref=canvas_ref />
            <Player />
            <Editor language="wgsl" theme="vs-dark" on_change=Some(move ||web_sys::console::log_1(&JsValue::from(&editor.get().unwrap().get_model().get_value()))) set_editor=set_editor />
        </div>
    }
}
