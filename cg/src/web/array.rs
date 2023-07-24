#![allow(unused)]
use js_sys::{
    Array, ArrayBuffer, BigInt64Array, BigUint64Array, Float32Array, Float64Array, Int16Array,
    Int32Array, Int8Array, SharedArrayBuffer, Uint16Array, Uint32Array, Uint8Array,
    Uint8ClampedArray, WebAssembly,
};
use std::iter::Iterator;
use std::mem::size_of;
use wasm_bindgen::{JsCast, JsValue};

// memory

/// Return the WebAssembly memory as an ArrayBuffer.
pub fn memory_buffer() -> ArrayBuffer {
    let memory = wasm_bindgen::memory().unchecked_into::<WebAssembly::Memory>();
    memory.buffer().unchecked_into::<ArrayBuffer>()
}

/// Return the WebAssembly memory as a SharedArrayBuffer.
pub fn memory_buffer_shared() -> SharedArrayBuffer {
    let memory = wasm_bindgen::memory().unchecked_into::<WebAssembly::Memory>();
    memory.buffer().unchecked_into::<SharedArrayBuffer>()
}

// typed arrays

macro_rules! array_buffer {
    ($name:ident $name_copy:ident $arr:ident::$t:ty) => {
        /// Return a typed array that contains the `data` memory region.
        ///
        /// The underlying typed array buffer is a subarray of the WebAssembly memory and is not copied.
        /// The buffer type will depend on the WebAssembly memory type.
        /// This might be unsafe, as the memory region might be altered from javascript operations.
        pub fn $name<T: Sized>(data: T) -> $arr {
            let begin = [data].as_ptr() as u32 / size_of::<$t>() as u32;
            let end = begin + (size_of::<T>() / size_of::<$t>()) as u32;
            $arr::new(&memory_buffer()).subarray(begin, end)
        }

        /// Return a typed array that contains the `data` memory region.
        ///
        /// The underlying typed array buffer is copied from the WebAssembly memory.
        pub fn $name_copy<T: Sized>(data: T) -> $arr {
            let begin = [data].as_ptr() as u32 / size_of::<$t>() as u32;
            let end = begin + (size_of::<T>() / size_of::<$t>()) as u32;
            $arr::new(&memory_buffer()).slice(begin, end)
        }
    };
}

array_buffer!(typed_u8c typed_u8c_copy Uint8ClampedArray::u8);
array_buffer!(typed_u8 typed_u8_copy Uint8Array::u8);
array_buffer!(typed_u16 typed_u16_copy Uint16Array::u16);
array_buffer!(typed_u32 typed_u32_copy Uint32Array::u32);
array_buffer!(typed_u64 typed_u64_copy BigUint64Array::u64);
array_buffer!(typed_i8 typed_i8_copy Int8Array::i8);
array_buffer!(typed_i16 typed_i16_copy Int16Array::i16);
array_buffer!(typed_i32 typed_i32_copy Int32Array::i32);
array_buffer!(typed_i64 typed_i64_copy BigInt64Array::i64);
array_buffer!(typed_f32 typed_f32_copy Float32Array::f32);
array_buffer!(typed_f64 typed_f64_copy Float64Array::f64);

// arrays

/// Wrap a single `&JsValue` into a js `Array`.
pub fn wrap(value: &JsValue) -> Array {
    let array = Array::new();
    array.push(value);
    array
}

/// Wrap a single value that `JsValue From<value>` is implemented for into a js `Array`.
pub fn wrap_cast<T>(value: T) -> Array
where
    JsValue: From<T>,
{
    let array = Array::new();
    array.push(&JsValue::from(value));
    array
}
