use crate::components::player::Player;
use leptos::*;

#[component]
pub fn Index(cx: Scope) -> impl IntoView {
    return view! {cx, <Player />};
}
