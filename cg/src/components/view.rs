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
pub fn View(
    cx: Scope,
    rw_playing: RwSignal<bool>,
    set_canvas: WriteSignal<Option<html::HtmlElement<html::Canvas>>>,
) -> impl IntoView {
    let canvas_ref = create_node_ref::<html::Canvas>(cx);
    let (playing, set_playing) = rw_playing.split();
    let icon = Signal::derive(cx, move || if playing() { "pause" } else { "play" });
    let (resolution, set_resolution) = create_signal(cx, (0, 0));
    let root = view! {
        cx,
        <div class="components_view">
            <canvas _ref=canvas_ref />
            <div>
                <PlayerButton icon="skip-back"/>
                <PlayerButton icon=icon on:click=move |_|set_playing(!playing()) />
                <span>140.3</span>
                <span>60.1fps</span>
                <span>{move || format!("{}x{}", resolution().0, resolution().1)}</span>
                <PlayerButton icon="maximize" />
            </div>
        </div>
    };
    let canvas = &canvas_ref.get().unwrap();
    set_canvas(Some(canvas.clone()));
    web_sys::ResizeObserver::new(&js_fn!(<dyn Fn(Array)> move |entries: Array| {
        let entry = js!(entries[0] as web_sys::ResizeObserverEntry).content_box_size().at(0);
        let block = js!(entry["blockSize"]).as_f64().unwrap_or_default() as i32;
        let inline = js!(entry["inlineSize"]).as_f64().unwrap_or_default() as i32;
        set_resolution((inline as i32, block as i32));
    }))
    .unwrap()
    .observe(canvas);
    root
}

#[component]
fn PlayerButton(cx: Scope, #[prop(into)] icon: MaybeSignal<&'static str>) -> impl IntoView {
    view! { cx, <button><svg viewBox="0 0 24 24"><use_ href=move||feather_icons::name(icon.get()) /></svg></button> }
}
