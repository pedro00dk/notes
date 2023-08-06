#![allow(unused)]
use js_sys::{
    Array, ArrayBuffer, BigInt64Array, BigUint64Array, Float32Array, Float64Array, Int16Array, Int32Array, Int8Array,
    SharedArrayBuffer, Uint16Array, Uint32Array, Uint8Array, Uint8ClampedArray, WebAssembly,
};
use std::iter::Iterator;
use std::mem::size_of;
use wasm_bindgen::{JsCast, JsValue};

/// Javascript interoperability utilities.

/// The `js!` macro provides utilities for creating and accessing [`js_sys::Object`] and [`js_sys::Array`].
/// All values involved in operation must be convertible to a [`wasm_bindgen::JsValue`].
///
/// Creating objects:
/// - empty object: `js!({})`
/// - filled object with literals: `js!({0: 0, "a": "a", false: true, "obj": js!({})})`
/// - filled object with expressions: `js!({[0]: 0, ["a"]: "a", [false]: true, ["obj"]: js!({})})`
/// - empty array: `js!([])`
/// - filled array: `js!([0, "a", true, js!([])])`
///
/// Accessing properties:
/// - getter: `let v = js!(object["a"])` or `let v = js!(array[0])`
/// - setter: `js!(object["a"] = v)` or `let v = js!(array[0] = v)`
macro_rules! js {

    // object init - literal keys
    ({$($key:literal: $value:expr),*}) => {{
        let object = js_sys::Object::new();
        $(js_sys::Reflect::set(&object, &JsValue::from($key), &wasm_bindgen::JsValue::from($value)).unwrap();)*
        object
    }};

    // object init - expression keys
    ({$([$key:expr]: $value:expr),*}) => {{
        let object = js_sys::Object::new();
        $(js_sys::Reflect::set(&object, &wasm_bindgen::JsValue::from($key), &wasm_bindgen::JsValue::from($value)).unwrap();)*
        object
    }};

    // object init - array
    ([$($value:expr),*]) => {{
        let array = js_sys::Array::new();
        $(array.push(&wasm_bindgen::JsValue::from($value));)*
        array
    }};

    // object getter
    ($object:ident[$key:expr]) => {
        js_sys::Reflect::get(&$object, &wasm_bindgen::JsValue::from($key)).unwrap_or(wasm_bindgen::JsValue::UNDEFINED)
    };

    // object getter option
    ($object:ident[$key:expr]?) => {
        js_sys::Reflect::get(&$object, &wasm_bindgen::JsValue::from($key)).ok()
    };

    // object getter or value
    ($object:ident[$key:expr] ?? $default:expr) => {
        js_sys::Reflect::get(&$object, &wasm_bindgen::JsValue::from($key)).unwrap_or(wasm_bindgen::JsValue::from(&$default))
    };

    // object getter and cast
    ($object:ident[$key:expr] as $type:ty) => {
        js_sys::Reflect::get(&$object, &wasm_bindgen::JsValue::from($key)).unwrap_or(wasm_bindgen::JsValue::UNDEFINED).unchecked_into::<$type>()
    };

    // object setter
    ($object:ident[$key:expr] = $value:expr) => {
        js_sys::Reflect::set(&$object, &wasm_bindgen::JsValue::from($key), &wasm_bindgen::JsValue::from(&$value)).err().unwrap_or(wasm_bindgen::JsValue::UNDEFINED)
    };
}

pub(crate) use js;

/// The `js_fn!` macro provides utilities for creating [`wasm_bindgen::closure::Closure`] and [`js_sys::Function`].
/// Function parameters and return types must all be convertible to [`wasm_bindgen::JsValue`].
/// Other constraints in [`wasm_bindgen::closure::Closure`] must also be followed.
///
/// Creating function:
/// - `let f = js_fn!(<dyn Fn()> move || {})`
/// - `let f = js_fn!(<dyn Fn(String) -> String> move |s| {s})`
macro_rules! js_fn {
    (<$type:ty>$function:expr) => {
        js_sys::Function::from(wasm_bindgen::closure::Closure::<$type>::new($function).into_js_value())
    };
}

pub(crate) use js_fn;

// memory buffers

/// Return the WebAssembly memory as an `ArrayBuffer`.
pub fn memory_buffer() -> ArrayBuffer {
    let memory = wasm_bindgen::memory().unchecked_into::<WebAssembly::Memory>();
    memory.buffer().unchecked_into::<ArrayBuffer>()
}

/// Return the WebAssembly memory as a `SharedArrayBuffer`.
pub fn memory_buffer_shared() -> SharedArrayBuffer {
    let memory = wasm_bindgen::memory().unchecked_into::<WebAssembly::Memory>();
    memory.buffer().unchecked_into::<SharedArrayBuffer>()
}

// typed array views

macro_rules! js_tav {
    ($name:ident $name_copy:ident $arr:ident::$t:ty) => {
        /// Return a typed array that contains the `data` memory region.
        ///
        /// The underlying typed array buffer is a subarray of the WebAssembly memory and is not copied.
        /// The buffer type will depend on the WebAssembly memory type.
        /// This might be unsafe, as the memory region might be altered from javascript operations.
        pub fn $name<T: Sized>(data: &T) -> $arr {
            let begin = data as *const T as u32 / size_of::<$t>() as u32;
            let end = begin + (size_of::<T>() / size_of::<$t>()) as u32;
            $arr::new(&memory_buffer()).subarray(begin, end)
        }

        /// Return a typed array that contains the `data` memory region.
        ///
        /// The underlying typed array buffer is copied from the WebAssembly memory.
        pub fn $name_copy<T: Sized>(data: &T) -> $arr {
            let begin = data as *const T as u32 / size_of::<$t>() as u32;
            let end = begin + (size_of::<T>() / size_of::<$t>()) as u32;
            $arr::new(&memory_buffer()).slice(begin, end)
        }
    };
}

js_tav!(tav_u8c tav_u8c_cp Uint8ClampedArray::u8);
js_tav!(tav_u8 tav_u8_cp Uint8Array::u8);
js_tav!(tav_u16 tav_u16_cp Uint16Array::u16);
js_tav!(tav_u32 tav_u32_cp Uint32Array::u32);
js_tav!(tav_u64 tav_u64_cp BigUint64Array::u64);
js_tav!(tav_i8 tav_i8_cp Int8Array::i8);
js_tav!(tav_i16 tav_i16_cp Int16Array::i16);
js_tav!(tav_i32 tav_i32_cp Int32Array::i32);
js_tav!(tav_i64 tav_i64_cp BigInt64Array::i64);
js_tav!(tav_f32 tav_f32_cp Float32Array::f32);
js_tav!(tav_f64 tav_f64_cp Float64Array::f64);
