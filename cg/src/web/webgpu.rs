use js_sys::{Array, Object, Reflect};
use wasm_bindgen::{JsCast, JsValue};
use wasm_bindgen_futures::JsFuture;
use web_sys::{self, GpuRenderPassDescriptor};

use super::array;

pub struct WebGpu {
    pub canvas: leptos::HtmlElement<leptos::html::Canvas>,
    pub context: web_sys::GpuCanvasContext,
    pub adapter: web_sys::GpuAdapter,
    pub device: web_sys::GpuDevice,
    pub format: web_sys::GpuTextureFormat,
}

impl WebGpu {
    pub async fn new(
        canvas: Option<leptos::HtmlElement<leptos::html::Canvas>>,
    ) -> Result<WebGpu, JsValue> {
        let canvas = canvas.ok_or(Some("adsf"))?;
        let context = canvas
            .get_context("webgpu")?
            .ok_or(Some("asdf"))?
            .unchecked_into::<web_sys::GpuCanvasContext>();
        let adapter = leptos::window() //
            .navigator()
            .gpu()
            .request_adapter();
        let adapter = JsFuture::from(adapter)
            .await?
            .unchecked_into::<web_sys::GpuAdapter>();
        let device = JsFuture::from(adapter.request_device())
            .await?
            .unchecked_into::<web_sys::GpuDevice>();
        let format = leptos::window()
            .navigator()
            .gpu()
            .get_preferred_canvas_format();
        context.configure(&web_sys::GpuCanvasConfiguration::new(
            &device,
            format.clone(),
        ));

        Result::Ok(WebGpu {
            canvas,
            context,
            adapter,
            device,
            format,
        })
    }

    pub fn print(&self) {
        let format = &self.format;
        web_sys::console::log_1(&self.context);
        web_sys::console::log_1(&self.adapter);
        web_sys::console::log_1(&self.device);
        leptos::log!("{format:?}");
    }
}

pub fn draw(webgpu: &WebGpu, clear: crate::math::MX<f32, 1, 4>) {
    let encoder = webgpu.device.create_command_encoder();
    web_sys::console::log_1(&encoder);
    let descriptor = Object::new();
    let color_attachment = Object::new();
    let color_attachments = Array::new();
    color_attachments.push(&color_attachment);
    Reflect::set(
        &descriptor,
        &JsValue::from("colorAttachments"),
        &color_attachments,
    )
    .unwrap();
    let texture = webgpu.context.get_current_texture();
    let view = texture.create_view();
    Reflect::set(
        //
        &color_attachment,
        &JsValue::from("view"),
        &view,
    )
    .unwrap();
    Reflect::set(
        &color_attachment,
        &JsValue::from("loadOp"),
        &JsValue::from("clear"),
    )
    .unwrap();
    Reflect::set(
        &color_attachment,
        &JsValue::from("storeOp"),
        &JsValue::from("store"),
    )
    .unwrap();

    //
    //

    // let clear1: Array = (&clear).into();
    // let clear2 = Float32Array::from(&clear);
    let clear3 = array::typed_f32(clear, false);
    // web_sys::console::log_1(&clear1);
    // web_sys::console::log_1(&clear2);
    web_sys::console::log_1(&clear3);

    Reflect::set(&color_attachment, &JsValue::from("clearValue"), &clear3).unwrap();

    web_sys::console::log_1(&texture);
    web_sys::console::log_1(&view);
    web_sys::console::log_1(&descriptor);

    //

    // web_sys::console::log_1(&memory_buffer());
    // web_sys::console::log_1(&data_array(clear, false));
    // web_sys::console::log_1(&data_array(clear, false));
    // web_sys::console::log_1(&data_array(clear, true));
    //
    //

    let pass = encoder.begin_render_pass(&GpuRenderPassDescriptor::new(&color_attachments));
    pass.end();
    let command_buffer = encoder.finish();
    let x = Array::new();
    x.push(&command_buffer);

    web_sys::console::log_1(&pass);
    web_sys::console::log_1(&command_buffer);

    webgpu.device.queue().submit(&x);
}
