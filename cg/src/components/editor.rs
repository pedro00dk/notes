use js_sys::{Function, JsString, Object, Reflect};
use leptos::*;
use wasm_bindgen::prelude::*;

use crate::util::types::{editor, StandaloneCodeEditor};

#[component]
pub fn Editor<TOnChange>(
    cx: Scope,
    #[prop(optional)] language: &'static str,
    #[prop(optional)] theme: &'static str,
    #[prop(optional)] set_editor: Option<WriteSignal<Option<StandaloneCodeEditor>>>,
    #[prop(default = None)] on_change: Option<TOnChange>,
) -> impl IntoView
where
    TOnChange: Fn() + 'static,
{
    let root = view! { cx, <div style="width: 100%; height: 100%" /> };
    let options = Object::new();
    Reflect::set(&options, &JsValue::from("automaticLayout"), &JsValue::TRUE).unwrap();
    Reflect::set(&options, &JsValue::from("language"), &JsValue::from(language)).unwrap();
    Reflect::set(&options, &JsValue::from("theme"), &JsValue::from(theme)).unwrap();
    let code_editor = editor().create(&root, &options);
    if let Some(set_editor) = set_editor {
        set_editor.set(Some(code_editor.clone()));
    }
    if let Some(on_change) = on_change {
        let model = code_editor.get_model();
        let callback = Function::from(Closure::<dyn Fn()>::new(on_change).into_js_value());
        model.on_did_change_content(&callback);
    }
    root
}
