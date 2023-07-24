use std::{cell, mem::size_of};

use crate::{count, matrix};
use js_sys::{Array, JsString, Object, Reflect};
use wasm_bindgen::{JsCast, JsValue};
use wasm_bindgen_futures::JsFuture;

use web_sys::*;

use crate::math::Triangle;

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
    let clear3 = array::typed_f32(clear);
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

    let triangles: [Triangle<2>; 2] = [
        (
            matrix!(VR[-0.8f32, -0.8f32]),
            matrix!(VR[0.8f32, -0.8f32]),
            matrix!(VR[0.8f32, 0.8f32]),
        ),
        (
            matrix!(VR[-0.8f32, -0.8f32]),
            matrix!(VR[0.8f32, 0.8f32]),
            matrix!(VR[-0.8f32, 0.8f32]),
        ),
    ];

    let x = &array::typed_f32(triangles);
    web_sys::console::log_1(&array::typed_f32(triangles));

    let dd = GpuBufferDescriptor::new(x.byte_length() as f64, 8 | 32);
    let bff = webgpu.device.create_buffer(&dd);
    bff.set_label("triangles");
    web_sys::console::log_1(&dd);
    web_sys::console::log_1(&bff);

    webgpu
        .device
        .queue()
        .write_buffer_with_u32_and_buffer_source(&bff, 0, &x);

    let attr = Object::new();
    Reflect::set(&attr, &JsValue::from("format"), &JsValue::from("float32x2")).unwrap();
    Reflect::set(&attr, &JsValue::from("offset"), &JsValue::from(0)).unwrap();
    Reflect::set(&attr, &JsValue::from("shaderLocation"), &JsValue::from(0)).unwrap();

    let layout = GpuVertexBufferLayout::new(8.0, &array::wrap(&attr));
    web_sys::console::log_1(&layout);

    let sha = GpuShaderModuleDescriptor::new(
        "
@vertex
fn vertex_main(@location(0) pos: vec4f) -> @builtin(position) vec4f {
    // return pos;
    return vec4f(pos[0], pos[1], 0.0, 1.0);
    }
    
    @fragment
    fn fragment_main() -> @location(0) vec4f
    {
    return vec4f(1.0, 0.0, 0.0, 1.0);
    }
        ",
    );
    let cell_shader_module = webgpu.device.create_shader_module(&sha);
    web_sys::console::log_1(&cell_shader_module);

    let mut gvs = GpuVertexState::new("vertex_main", &cell_shader_module);
    gvs.buffers(&array::wrap(&layout));
    web_sys::console::log_1(&gvs);
    let mut gfs = GpuFragmentState::new("fragment_main", &cell_shader_module, &JsValue::UNDEFINED);

    let targ = Object::new();
    Reflect::set(
        &targ,
        &JsValue::from("format"),
        &JsValue::from(webgpu.format),
    )
    .unwrap();
    // gfs.targets(&array::wrap(&targ));
    gfs.targets(&array::wrap(&targ));
    web_sys::console::log_1(&gfs);

    let mut pip = GpuRenderPipelineDescriptor::new(&JsValue::from("auto"), &gvs);
    // pip.for
    pip.fragment(&gfs);
    web_sys::console::log_1(&pip);
    let pipeline = webgpu.device.create_render_pipeline(&pip);
    web_sys::console::log_1(&pipeline);

    pass.set_pipeline(&pipeline);
    pass.set_vertex_buffer(0, &bff);
    // pass.draw(triangles.length / 2); // 6 vertices
    pass.draw(12 / 2); // 6 vertices

    //
    //
    //

    pass.end();
    let command_buffer = encoder.finish();

    // let x = Array::new();
    // x.push(&command_buffer);

    web_sys::console::log_1(&pass);
    web_sys::console::log_1(&command_buffer);

    webgpu.device.queue().submit(&array::wrap(&command_buffer));
}
