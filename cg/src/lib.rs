#![allow(incomplete_features)]
#![feature(async_closure)]
#![feature(generic_const_exprs)]

mod components;
mod math;
mod pages;
mod web;

use leptos::*;
use pages::Index::Index;
use wasm_bindgen::prelude::*;

#[wasm_bindgen]
extern "C" {
    fn alert(s: &str);
}

#[wasm_bindgen]
pub fn mount() {
    mount_to_body(|cx| view! { cx, <Index /> })
}
