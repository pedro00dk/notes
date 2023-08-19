use crate::components::editor::Editor;
use crate::components::view::View;
use crate::math;
use crate::util::types::monaco_editor;
use crate::web;
use leptos::html;
use leptos::*;
use wasm_bindgen::prelude::*;

#[component]
pub fn Player(cx: Scope) -> impl IntoView {
    let rw_playing = create_rw_signal(cx, true);
    let (canvas, set_canvas) = create_signal::<Option<html::HtmlElement<html::Canvas>>>(cx, None);
    let (editor, set_editor) = create_signal::<Option<monaco_editor::StandaloneCodeEditor>>(cx, None);

    create_resource(
        cx,
        move || canvas,
        async move |canvas| {
            if let None = canvas.get() {
                return;
            }
            let canvas = canvas.get().unwrap();
            let webgpu = web::webgpu::WebGpu::new(Some(canvas)).await.unwrap();
            webgpu.print();
            web::webgpu::draw(&webgpu, math::mx!(VR[0.0, 0.3, 0.3, 1.0]));
        },
    );

    view! { cx,
        <div class="components_player">
            <View rw_playing=rw_playing set_canvas=set_canvas />
            <Editor language="wgsl" theme="vs-dark" on_change=Some(move ||web_sys::console::log_1(&JsValue::from(&editor.get().unwrap().get_model().get_value()))) set_editor=set_editor />
        </div>
    }
}
