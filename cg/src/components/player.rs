use js_sys::{Function, JsString, Object, Reflect};
use leptos::{html, *};
use wasm_bindgen::prelude::*;

#[component]
pub fn Player(
    cx: Scope,
    // #[prop(optional)] language: &'static str,
    // #[prop(optional)] theme: &'static str,
    // #[prop(optional)] set_editor: Option<WriteSignal<Option<StandaloneCodeEditor>>>,
    // #[prop(default = None)] on_change: Option<TOnChange>,
) -> impl IntoView
// where
//     TOnChange: Fn() + 'static,
{
    let canvas_ref = create_node_ref::<html::Canvas>(cx);
    let player = view! {
        cx,
        <div>
            <canvas _ref=canvas_ref />
            <div>
                <button />
                <button />
                <span></span>
                <span></span>
                <span></span>
                <button></button>
                <button></button>
            </div>
        </div>
    };

    let canvas = canvas_ref.get().unwrap();
    web_sys::console::log_1(&canvas);

    player
}
