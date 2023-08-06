use crate::util::{
    js::{js, js_fn},
    types::feather_icons,
};
use js_sys::{Array, Function, JsString, Reflect};
use leptos::{
    html,
    MaybeSignal::{Dynamic, Static},
    *,
};
use wasm_bindgen::prelude::*;
use web_sys::MouseEvent;

#[component]
pub fn Player(
    cx: Scope,
    // #[prop(optional)] playing: bool,
    // #[prop(optional)] theme: &'static str,
    // #[prop(optional)] set_editor: Option<WriteSignal<Option<StandaloneCodeEditor>>>,
    // #[prop(default = None)] on_change: Option<TOnChange>,
    // #[prop(default = None)] on_change: Option<TOnChange>,
) -> impl IntoView
// where
//     TOnChange: Fn() + 'static,
{
    let (playing, set_playing) = create_signal(cx, false);
    let icon = Signal::derive(cx, move || if playing() { "pause" } else { "play" });
    let canvas_ref = create_node_ref::<html::Canvas>(cx);
    let (resolution, set_resolution) = create_signal(cx, (0, 0));
    let root = view! {
        cx,
        <div class="components_player">
            <canvas _ref=canvas_ref />
            <div>
                <PlayerButton icon=Static("skip-back")/>
                <PlayerButton icon=Dynamic(icon) on:click=move |_|set_playing(!playing()) />
                <span>140.3</span>
                <span>60.1fps</span>
                <span>{move || format!("{}x{}", resolution().0, resolution().1)}</span>
                <PlayerButton icon=Static("circle") />
                <PlayerButton icon=Static("maximize") />
            </div>
        </div>
    };
    web_sys::ResizeObserver::new(&js_fn!(<dyn Fn(Array)> move |entries: Array| {
        let entry = js!(entries[0] as web_sys::ResizeObserverEntry).content_box_size().at(0);
        let block = js!(entry["blockSize"]).as_f64().unwrap_or_default() as i32;
        let inline = js!(entry["inlineSize"]).as_f64().unwrap_or_default() as i32;
        set_resolution((block as i32, inline as i32));
    }))
    .unwrap()
    .observe(&canvas_ref.get().unwrap());

    create_effect(cx, move |_| log!("{} -- {}", playing(), icon()));

    root
}

#[component]
fn PlayerButton(cx: Scope, icon: MaybeSignal<&'static str>) -> impl IntoView {
    view! { cx, <button><svg viewBox="0 0 24 24"><use_ href=feather_icons::name(icon.get()) /></svg></button> }
}
