use js_sys::{Uint8ClampedArray, WebAssembly};
use leptos::*;
use wasm_bindgen::prelude::*;
use web_sys::CanvasRenderingContext2d;

fn main() {
    mount_to_body(|cx| view! { cx, <App /> })
}

#[component]
fn App(cx: Scope) -> impl IntoView {
    let canvas_ref = create_node_ref::<html::Canvas>(cx);

    create_effect(cx, move |_| {
        let canvas = canvas_ref.get();
        if let None = canvas {
            return;
        }
        let ctx = canvas
            .unwrap()
            .get_context("2d")
            .unwrap()
            .unwrap()
            .unchecked_into::<CanvasRenderingContext2d>();
        ctx.fill_rect(10.0, 10.0, 100.0, 70.0);

        let mut data = vec![0u8; 4 * 100 * 100];
        for (i, v) in data.iter_mut().enumerate() {
            *v = (i % 256) as u8;
        }

        let image = image_data(data, 100.0, 100.0);

        ctx.put_image_data(&image, 0.0, 0.0).unwrap();

        // ctx.
        log!("hello");
    });

    view! { cx, <canvas _ref=canvas_ref /> }
}

// Inline the definition of `ImageData`.
// `web_sys` definition uses `&Clamped<Vec<u8>>`, we need to pass a JsObject.
#[wasm_bindgen]
extern "C" {
    pub type ImageData;
    #[wasm_bindgen(constructor, catch)]
    fn new(data: &Uint8ClampedArray, width: f64, height: f64) -> Result<ImageData, JsValue>;
}

fn image_data(data: Vec<u8>, width: f64, height: f64) -> web_sys::ImageData {
    // get data reference in WebAssembly memory
    let start = data.as_ptr() as usize as u32;
    let length = data.len() as u32;
    let memory = wasm_bindgen::memory().unchecked_into::<WebAssembly::Memory>();

    // create js uint8 array copy (.slice), ImageData does not support shared arrays (.subarray)
    let array = Uint8ClampedArray::new(&memory.buffer()).slice(start, start + length);
    unsafe { std::mem::transmute(ImageData::new(&array, width, height).unwrap()) }
}
