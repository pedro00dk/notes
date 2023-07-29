use js_sys::{Object, Reflect};
use leptos::{html::code, *};
use wasm_bindgen::prelude::*;

#[wasm_bindgen(raw_module = "monaco-editor")]
extern "C" {
    fn editor() -> Editor;

    #[wasm_bindgen(extends=Object)]
    #[derive(Debug, Clone)]
    type Editor;

    #[wasm_bindgen(method)]
    pub fn create(this: &Editor, element: &web_sys::Element, options: &Object) -> StandaloneCodeEditor;

    #[wasm_bindgen(extends=Object)]
    #[derive(Debug, Clone)]
    type StandaloneCodeEditor;

    #[wasm_bindgen(method, js_name = "getModel")]
    pub fn get_model(this: &StandaloneCodeEditor) -> TextModel;

    #[wasm_bindgen(extends=Object)]
    #[derive(Debug, Clone)]
    type TextModel;
}

#[component]
pub fn Editor(
    cx: Scope,
    #[prop(optional)] language: &'static str,
    #[prop(optional)] theme: &'static str,
    // #[prop(optional)] on_change: Option<Fn(i32): String>,
    // #[prop(optional)] get_value: Option<Fn()>,
) -> impl IntoView {
    let root = view! { cx, <div style="width: 100%; height: 100%" /> };
    let options = Object::new();
    Reflect::set(&options, &JsValue::from("automaticLayout"), &JsValue::TRUE).unwrap();
    Reflect::set(&options, &JsValue::from("language"), &JsValue::from(language)).unwrap();
    Reflect::set(&options, &JsValue::from("theme"), &JsValue::from(theme)).unwrap();
    let code_editor = editor().create(&root, &options);
    let model = code_editor.get_model();
    root
}
