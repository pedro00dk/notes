use js_sys::{Function, Object, Reflect};
use leptos::*;
use wasm_bindgen::prelude::*;

#[wasm_bindgen(raw_module = "monaco-editor")]
extern "C" {
    fn editor() -> Editor;

    #[wasm_bindgen(extends=Object)]
    #[derive(Debug, Clone)]
    type Editor;
    #[wasm_bindgen(extends=Object)]
    #[derive(Debug, Clone)]
    type StandaloneCodeEditor;
    #[wasm_bindgen(extends=Object)]
    #[derive(Debug, Clone)]
    type TextModel;

    #[wasm_bindgen(method)]
    pub fn create(this: &Editor, element: &web_sys::Element, options: &Object) -> StandaloneCodeEditor;

    #[wasm_bindgen(method, js_name = "getModel")]
    pub fn get_model(this: &StandaloneCodeEditor) -> TextModel;

    #[wasm_bindgen(method, js_name = "onDidChangeContent")]
    pub fn on_did_change_content(this: &TextModel, listener: &JsValue) -> TextModel;
}

#[component]
pub fn Editor<T>(
    cx: Scope,
    #[prop(optional)] language: &'static str,
    #[prop(optional)] theme: &'static str,
    #[prop(default = None)] on_change: Option<T>,
    // #[prop(optional)] get_value: Option<Fn()>,
) -> impl IntoView
where
    T: Fn() + 'static,
{
    let options = Object::new();

    Reflect::set(&options, &JsValue::from("automaticLayout"), &JsValue::TRUE).unwrap();
    Reflect::set(&options, &JsValue::from("language"), &JsValue::from(language)).unwrap();
    Reflect::set(&options, &JsValue::from("theme"), &JsValue::from(theme)).unwrap();
    let root = view! { cx, <div style="width: 100%; height: 100%" /> };
    let code_editor = editor().create(&root, &options);
    let model = code_editor.get_model();
    if let Some(on_change) = on_change {
        model.on_did_change_content(&Closure::<dyn Fn()>::new(on_change).into_js_value());
    }

    // on_change();
    // on_change();
    // let b = a.as_ref().unchecked_ref();
    // Function::from();
    // model.on_did_change_content(&a);
    root
}
