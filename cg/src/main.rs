#![allow(incomplete_features)]
#![feature(async_closure)]
#![feature(generic_const_exprs)]

mod math;
mod pages;
mod web;

use leptos::*;
use pages::Index::Index;

fn main() {
    mount_to_body(|cx| view! { cx, <Index /> })
}
