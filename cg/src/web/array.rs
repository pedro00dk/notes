#![allow(unused)]
use js_sys::{
    ArrayBuffer, BigInt64Array, BigUint64Array, Float32Array, Float64Array, Int16Array, Int32Array,
    Int8Array, SharedArrayBuffer, Uint16Array, Uint32Array, Uint8Array, Uint8ClampedArray,
    WebAssembly,
};
use std::mem::size_of;
use wasm_bindgen::JsCast;

pub fn memory_buffer() -> ArrayBuffer {
    let memory = wasm_bindgen::memory().unchecked_into::<WebAssembly::Memory>();
    memory.buffer().unchecked_into::<ArrayBuffer>()
}

pub fn memory_buffer_shared() -> SharedArrayBuffer {
    let memory = wasm_bindgen::memory().unchecked_into::<WebAssembly::Memory>();
    memory.buffer().unchecked_into::<SharedArrayBuffer>()
}

macro_rules! array_buffer {
    ($name:ident $arr:ident::$t:ty) => {
        pub fn $name<T: Sized>(data: T, copy: bool) -> $arr {
            let begin = [data].as_ptr() as u32 / size_of::<$t>() as u32;
            let end = begin + (size_of::<T>() / size_of::<$t>()) as u32;
            if copy {
                return $arr::new(&memory_buffer()).slice(begin, end);
            } else {
                return $arr::new(&memory_buffer()).subarray(begin, end);
            }
        }
    };
}

array_buffer!(typed_u8c Uint8ClampedArray::u8);
array_buffer!(typed_u8 Uint8Array::u8);
array_buffer!(typed_u16 Uint16Array::u16);
array_buffer!(typed_u32 Uint32Array::u32);
array_buffer!(typed_u64 BigUint64Array::u64);
array_buffer!(typed_i8 Int8Array::i8);
array_buffer!(typed_i16 Int16Array::i16);
array_buffer!(typed_i32 Int32Array::i32);
array_buffer!(typed_i64 BigInt64Array::i64);
array_buffer!(typed_f32 Float32Array::f32);
array_buffer!(typed_f64 Float64Array::f64);

// javascript

// impl<T, const R: usize, const C: usize> From<&MX<T, R, C>> for Array
// where
//     T: Copy,
//     JsValue: From<T>,
//     [(); R * C]:,
// {
//     fn from(value: &MX<T, R, C>) -> Self {
//         let array = Array::new_with_length(value.data.len() as u32);
//         value.data.iter().enumerate().for_each(|(i, v)| {
//             array.set(i as u32, JsValue::from(*v));
//         });
//         array
//     }
// }

// macro_rules! js_array_from {
//     ($arr:ident::$t:ty) => {
//         impl<const R: usize, const C: usize> From<&MX<$t, R, C>> for $arr
//         where
//             [(); R * C]:,
//         {
//             fn from(value: &MX<$t, R, C>) -> Self {
//                 let array = $arr::new_with_length(value.data.len() as u32);
//                 value.data.iter().enumerate().for_each(|(i, v)| {
//                     array.set_index(i as u32, *v);
//                 });
//                 array
//             }
//         }
//     };
// }

// js_array_from!(Float32Array::f32);
// js_array_from!(Float64Array::f64);
// js_array_from!(Uint8ClampedArray::u8);
// js_array_from!(Uint8Array::u8);
// js_array_from!(Uint16Array::u16);
// js_array_from!(Uint32Array::u32);
// js_array_from!(Int8Array::i8);
// js_array_from!(Int16Array::i16);
// js_array_from!(Int32Array::i32);
