use js_sys::Function;
use leptos::*;
use wasm_bindgen::prelude::*;

use crate::util::{
    js::{js, js_fn},
    types::monaco_editor,
};

#[component]
pub fn Editor<TOnChange>(
    cx: Scope,
    #[prop(optional)] language: &'static str,
    #[prop(optional)] theme: &'static str,
    #[prop(optional)] set_editor: Option<WriteSignal<Option<monaco_editor::StandaloneCodeEditor>>>,
    #[prop(default = None)] on_change: Option<TOnChange>,
) -> impl IntoView
where
    TOnChange: Fn() + 'static,
{
    let root = view! { cx, <div style="width: 100%; height: 100%" /> };
    let options = js!({"automaticLayout": true, "language": language, "theme": theme});
    let code_editor = monaco_editor::editor().create(&root, &options);
    if let Some(set_editor) = set_editor {
        set_editor.set(Some(code_editor.clone()));
    }
    if let Some(on_change) = on_change {
        let model = code_editor.get_model();
        model.on_did_change_content(&js_fn!(<dyn Fn()> on_change));
    }
    root
}
