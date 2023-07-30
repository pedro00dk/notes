use js_sys::{Function, JsString, Object};
use wasm_bindgen::prelude::*;

#[wasm_bindgen(raw_module = "feather-icons")]
extern "C" {
    pub fn sprite(name: &str) -> JsString;
}

#[wasm_bindgen(raw_module = "monaco-editor")]
extern "C" {
    pub fn editor() -> Editor;

    #[wasm_bindgen(extends=Object)]
    #[derive(Debug, Clone)]
    pub type Editor;
    #[wasm_bindgen(method)]
    pub fn create(this: &Editor, element: &web_sys::Element, options: &Object) -> StandaloneCodeEditor;

    #[wasm_bindgen(extends=Object)]
    #[derive(Debug, Clone)]
    pub type StandaloneCodeEditor;
    #[wasm_bindgen(method, js_name = "getModel")]
    pub fn get_model(this: &StandaloneCodeEditor) -> TextModel;

    #[wasm_bindgen(extends=Object)]
    #[derive(Debug, Clone)]
    pub type TextModel;
    #[wasm_bindgen(method, js_name = "getValue")]
    pub fn get_value(this: &TextModel) -> JsString;
    #[wasm_bindgen(method, js_name = "onDidChangeContent")]
    pub fn on_did_change_content(this: &TextModel, listener: &Function) -> TextModel;
}
