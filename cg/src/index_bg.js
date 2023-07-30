let wasm;
export function __wbg_set_wasm(val) {
    wasm = val;
}


const cachedTextDecoder = (typeof TextDecoder !== 'undefined' ? new TextDecoder('utf-8', { ignoreBOM: true, fatal: true }) : { decode: () => { throw Error('TextDecoder not available') } } );

if (typeof TextDecoder !== 'undefined') { cachedTextDecoder.decode(); };

let cachedUint8Memory0 = null;

function getUint8Memory0() {
    if (cachedUint8Memory0 === null || cachedUint8Memory0.byteLength === 0) {
        cachedUint8Memory0 = new Uint8Array(wasm.memory.buffer);
    }
    return cachedUint8Memory0;
}

function getStringFromWasm0(ptr, len) {
    ptr = ptr >>> 0;
    return cachedTextDecoder.decode(getUint8Memory0().subarray(ptr, ptr + len));
}

let WASM_VECTOR_LEN = 0;

const cachedTextEncoder = (typeof TextEncoder !== 'undefined' ? new TextEncoder('utf-8') : { encode: () => { throw Error('TextEncoder not available') } } );

const encodeString = (typeof cachedTextEncoder.encodeInto === 'function'
    ? function (arg, view) {
    return cachedTextEncoder.encodeInto(arg, view);
}
    : function (arg, view) {
    const buf = cachedTextEncoder.encode(arg);
    view.set(buf);
    return {
        read: arg.length,
        written: buf.length
    };
});

function passStringToWasm0(arg, malloc, realloc) {

    if (realloc === undefined) {
        const buf = cachedTextEncoder.encode(arg);
        const ptr = malloc(buf.length, 1) >>> 0;
        getUint8Memory0().subarray(ptr, ptr + buf.length).set(buf);
        WASM_VECTOR_LEN = buf.length;
        return ptr;
    }

    let len = arg.length;
    let ptr = malloc(len, 1) >>> 0;

    const mem = getUint8Memory0();

    let offset = 0;

    for (; offset < len; offset++) {
        const code = arg.charCodeAt(offset);
        if (code > 0x7F) break;
        mem[ptr + offset] = code;
    }

    if (offset !== len) {
        if (offset !== 0) {
            arg = arg.slice(offset);
        }
        ptr = realloc(ptr, len, len = offset + arg.length * 3, 1) >>> 0;
        const view = getUint8Memory0().subarray(ptr + offset, ptr + len);
        const ret = encodeString(arg, view);

        offset += ret.written;
    }

    WASM_VECTOR_LEN = offset;
    return ptr;
}

function isLikeNone(x) {
    return x === undefined || x === null;
}

let cachedInt32Memory0 = null;

function getInt32Memory0() {
    if (cachedInt32Memory0 === null || cachedInt32Memory0.byteLength === 0) {
        cachedInt32Memory0 = new Int32Array(wasm.memory.buffer);
    }
    return cachedInt32Memory0;
}

function debugString(val) {
    // primitive types
    const type = typeof val;
    if (type == 'number' || type == 'boolean' || val == null) {
        return  `${val}`;
    }
    if (type == 'string') {
        return `"${val}"`;
    }
    if (type == 'symbol') {
        const description = val.description;
        if (description == null) {
            return 'Symbol';
        } else {
            return `Symbol(${description})`;
        }
    }
    if (type == 'function') {
        const name = val.name;
        if (typeof name == 'string' && name.length > 0) {
            return `Function(${name})`;
        } else {
            return 'Function';
        }
    }
    // objects
    if (Array.isArray(val)) {
        const length = val.length;
        let debug = '[';
        if (length > 0) {
            debug += debugString(val[0]);
        }
        for(let i = 1; i < length; i++) {
            debug += ', ' + debugString(val[i]);
        }
        debug += ']';
        return debug;
    }
    // Test for built-in
    const builtInMatches = /\[object ([^\]]+)\]/.exec(toString.call(val));
    let className;
    if (builtInMatches.length > 1) {
        className = builtInMatches[1];
    } else {
        // Failed to match the standard '[object ClassName]'
        return toString.call(val);
    }
    if (className == 'Object') {
        // we're a user defined class or Object
        // JSON.stringify avoids problems with cycles, and is generally much
        // easier than looping through ownProperties of `val`.
        try {
            return 'Object(' + JSON.stringify(val) + ')';
        } catch (_) {
            return 'Object';
        }
    }
    // errors
    if (val instanceof Error) {
        return `${val.name}: ${val.message}\n${val.stack}`;
    }
    // TODO we could test for more things here, like `Set`s and `Map`s.
    return className;
}

const CLOSURE_DTORS = new FinalizationRegistry(state => {
    wasm.__wbindgen_export_3.get(state.dtor)(state.a, state.b)
});

function makeClosure(arg0, arg1, dtor, f) {
    const state = { a: arg0, b: arg1, cnt: 1, dtor };
    const real = (...args) => {
        // First up with a closure we increment the internal reference
        // count. This ensures that the Rust closure environment won't
        // be deallocated while we're invoking it.
        state.cnt++;
        try {
            return f(state.a, state.b, ...args);
        } finally {
            if (--state.cnt === 0) {
                wasm.__wbindgen_export_3.get(state.dtor)(state.a, state.b);
                state.a = 0;
                CLOSURE_DTORS.unregister(state)
            }
        }
    };
    real.original = state;
    CLOSURE_DTORS.register(real, state, state);
    return real;
}
function __wbg_adapter_24(arg0, arg1) {
    wasm._dyn_core__ops__function__Fn_____Output___R_as_wasm_bindgen__closure__WasmClosure___describe__invoke__h2456d04ec546b7bf(arg0, arg1);
}

function makeMutClosure(arg0, arg1, dtor, f) {
    const state = { a: arg0, b: arg1, cnt: 1, dtor };
    const real = (...args) => {
        // First up with a closure we increment the internal reference
        // count. This ensures that the Rust closure environment won't
        // be deallocated while we're invoking it.
        state.cnt++;
        const a = state.a;
        state.a = 0;
        try {
            return f(a, state.b, ...args);
        } finally {
            if (--state.cnt === 0) {
                wasm.__wbindgen_export_3.get(state.dtor)(a, state.b);
                CLOSURE_DTORS.unregister(state)
            } else {
                state.a = a;
            }
        }
    };
    real.original = state;
    CLOSURE_DTORS.register(real, state, state);
    return real;
}
function __wbg_adapter_27(arg0, arg1) {
    wasm._dyn_core__ops__function__FnMut_____Output___R_as_wasm_bindgen__closure__WasmClosure___describe__invoke__h162254376d9d8cac(arg0, arg1);
}

function __wbg_adapter_30(arg0, arg1, arg2) {
    wasm.closure279_externref_shim(arg0, arg1, arg2);
}

/**
*/
export function mount() {
    wasm.mount();
}

function addToExternrefTable0(obj) {
    const idx = wasm.__externref_table_alloc();
    wasm.__wbindgen_export_2.set(idx, obj);
    return idx;
}

function getFromExternrefTable0(idx) { return wasm.__wbindgen_export_2.get(idx); }

function getCachedStringFromWasm0(ptr, len) {
    if (ptr === 0) {
        return getFromExternrefTable0(len);
    } else {
        return getStringFromWasm0(ptr, len);
    }
}

function handleError(f, args) {
    try {
        return f.apply(this, args);
    } catch (e) {
        const idx = addToExternrefTable0(e);
        wasm.__wbindgen_exn_store(idx);
    }
}

function notDefined(what) { return () => { throw new Error(`${what} is not defined`); }; }

export function __wbg_create_fc3d67116b8319ae(arg0, arg1, arg2) {
    const ret = arg0.create(arg1, arg2);
    return ret;
};

export function __wbg_getModel_3835af0538c3f0eb(arg0) {
    const ret = arg0.getModel();
    return ret;
};

export function __wbg_getValue_730b5fd4e77a5329(arg0) {
    const ret = arg0.getValue();
    return ret;
};

export function __wbg_onDidChangeContent_a599e776557dcb0e(arg0, arg1) {
    const ret = arg0.onDidChangeContent(arg1);
    return ret;
};

export function __wbindgen_number_new(arg0) {
    const ret = arg0;
    return ret;
};

export function __wbindgen_string_new(arg0, arg1) {
    const ret = getStringFromWasm0(arg0, arg1);
    return ret;
};

export function __wbindgen_is_undefined(arg0) {
    const ret = arg0 === undefined;
    return ret;
};

export function __wbindgen_string_get(arg0, arg1) {
    const obj = arg1;
    const ret = typeof(obj) === 'string' ? obj : undefined;
    var ptr1 = isLikeNone(ret) ? 0 : passStringToWasm0(ret, wasm.__wbindgen_malloc, wasm.__wbindgen_realloc);
    var len1 = WASM_VECTOR_LEN;
    getInt32Memory0()[arg0 / 4 + 1] = len1;
    getInt32Memory0()[arg0 / 4 + 0] = ptr1;
};

export function __wbindgen_cb_drop(arg0) {
    const obj = arg0.original;
    if (obj.cnt-- == 1) {
        obj.a = 0;
        return true;
    }
    const ret = false;
    return ret;
};

export function __wbg_instanceof_Window_9029196b662bc42a(arg0) {
    let result;
    try {
        result = arg0 instanceof Window;
    } catch {
        result = false;
    }
    const ret = result;
    return ret;
};

export function __wbg_document_f7ace2b956f30a4f(arg0) {
    const ret = arg0.document;
    return isLikeNone(ret) ? 0 : addToExternrefTable0(ret);
};

export function __wbg_navigator_7c9103698acde322(arg0) {
    const ret = arg0.navigator;
    return ret;
};

export function __wbg_body_674aec4c1c0910cd(arg0) {
    const ret = arg0.body;
    return isLikeNone(ret) ? 0 : addToExternrefTable0(ret);
};

export function __wbg_createComment_6b5ea2660a7c961a(arg0, arg1, arg2) {
    var v0 = getCachedStringFromWasm0(arg1, arg2);
    const ret = arg0.createComment(v0);
    return ret;
};

export function __wbg_createDocumentFragment_2570c0407199fba9(arg0) {
    const ret = arg0.createDocumentFragment();
    return ret;
};

export function __wbg_createElement_4891554b28d3388b() { return handleError(function (arg0, arg1, arg2) {
    var v0 = getCachedStringFromWasm0(arg1, arg2);
    const ret = arg0.createElement(v0);
    return ret;
}, arguments) };

export function __wbg_createElementNS_119acf9e82482041() { return handleError(function (arg0, arg1, arg2, arg3, arg4) {
    var v0 = getCachedStringFromWasm0(arg1, arg2);
    var v1 = getCachedStringFromWasm0(arg3, arg4);
    const ret = arg0.createElementNS(v0, v1);
    return ret;
}, arguments) };

export function __wbg_getElementById_cc0e0d931b0d9a28(arg0, arg1, arg2) {
    var v0 = getCachedStringFromWasm0(arg1, arg2);
    const ret = arg0.getElementById(v0);
    return isLikeNone(ret) ? 0 : addToExternrefTable0(ret);
};

export function __wbg_querySelector_52ded52c20e23921() { return handleError(function (arg0, arg1, arg2) {
    var v0 = getCachedStringFromWasm0(arg1, arg2);
    const ret = arg0.querySelector(v0);
    return isLikeNone(ret) ? 0 : addToExternrefTable0(ret);
}, arguments) };

export function __wbg_namespaceURI_31718ed49b5343a3(arg0, arg1) {
    const ret = arg1.namespaceURI;
    var ptr1 = isLikeNone(ret) ? 0 : passStringToWasm0(ret, wasm.__wbindgen_malloc, wasm.__wbindgen_realloc);
    var len1 = WASM_VECTOR_LEN;
    getInt32Memory0()[arg0 / 4 + 1] = len1;
    getInt32Memory0()[arg0 / 4 + 0] = ptr1;
};

export function __wbg_setinnerHTML_b089587252408b67(arg0, arg1, arg2) {
    var v0 = getCachedStringFromWasm0(arg1, arg2);
    arg0.innerHTML = v0;
};

export function __wbg_outerHTML_f7749ceff37b5832(arg0, arg1) {
    const ret = arg1.outerHTML;
    const ptr1 = passStringToWasm0(ret, wasm.__wbindgen_malloc, wasm.__wbindgen_realloc);
    const len1 = WASM_VECTOR_LEN;
    getInt32Memory0()[arg0 / 4 + 1] = len1;
    getInt32Memory0()[arg0 / 4 + 0] = ptr1;
};

export function __wbg_removeAttribute_d8404da431968808() { return handleError(function (arg0, arg1, arg2) {
    var v0 = getCachedStringFromWasm0(arg1, arg2);
    arg0.removeAttribute(v0);
}, arguments) };

export function __wbg_setAttribute_e7e80b478b7b8b2f() { return handleError(function (arg0, arg1, arg2, arg3, arg4) {
    var v0 = getCachedStringFromWasm0(arg1, arg2);
    var v1 = getCachedStringFromWasm0(arg3, arg4);
    arg0.setAttribute(v0, v1);
}, arguments) };

export function __wbg_before_208bff4b64d8f1f7() { return handleError(function (arg0, arg1) {
    arg0.before(arg1);
}, arguments) };

export function __wbg_setlabel_fe3b606c39ff9783(arg0, arg1, arg2) {
    var v0 = getCachedStringFromWasm0(arg1, arg2);
    arg0.label = v0;
};

export function __wbg_configure_93a57a4e5e0f8bcf(arg0, arg1) {
    arg0.configure(arg1);
};

export function __wbg_getCurrentTexture_ecedc4f6f71990d2(arg0) {
    const ret = arg0.getCurrentTexture();
    return ret;
};

export function __wbg_append_4672bfcd9b84298e() { return handleError(function (arg0, arg1, arg2) {
    arg0.append(arg1, arg2);
}, arguments) };

export function __wbg_getContext_7c5944ea807bf5d3() { return handleError(function (arg0, arg1, arg2) {
    var v0 = getCachedStringFromWasm0(arg1, arg2);
    const ret = arg0.getContext(v0);
    return isLikeNone(ret) ? 0 : addToExternrefTable0(ret);
}, arguments) };

export function __wbg_createView_5c2f05175c1c8770(arg0) {
    const ret = arg0.createView();
    return ret;
};

export const __wbg_log_1d3ae0273d8f4f8a = typeof console.log == 'function' ? console.log : notDefined('console.log');

export const __wbg_warn_d60e832f9882c1b2 = typeof console.warn == 'function' ? console.warn : notDefined('console.warn');

export function __wbg_submit_3104e9b014f75846(arg0, arg1) {
    arg0.submit(arg1);
};

export function __wbg_writeBuffer_d625aa039f4f09ee(arg0, arg1, arg2, arg3) {
    arg0.writeBuffer(arg1, arg2 >>> 0, arg3);
};

export function __wbg_queue_f2aeb5c277e56f93(arg0) {
    const ret = arg0.queue;
    return ret;
};

export function __wbg_createBuffer_36e159f52cc644a7(arg0, arg1) {
    const ret = arg0.createBuffer(arg1);
    return ret;
};

export function __wbg_createCommandEncoder_99ee7d5b1a72b0cf(arg0) {
    const ret = arg0.createCommandEncoder();
    return ret;
};

export function __wbg_createRenderPipeline_745f00bcb1ca6edf(arg0, arg1) {
    const ret = arg0.createRenderPipeline(arg1);
    return ret;
};

export function __wbg_createShaderModule_59bbf537b8b5cf7c(arg0, arg1) {
    const ret = arg0.createShaderModule(arg1);
    return ret;
};

export function __wbg_length_7aeee1534dbcb390(arg0) {
    const ret = arg0.length;
    return ret;
};

export function __wbg_getPreferredCanvasFormat_1f6c9ef810196b92(arg0) {
    const ret = arg0.getPreferredCanvasFormat();
    return ret;
};

export function __wbg_requestAdapter_af2e85790cc34f22(arg0) {
    const ret = arg0.requestAdapter();
    return ret;
};

export function __wbg_beginRenderPass_d04327f7231bd5af(arg0, arg1) {
    const ret = arg0.beginRenderPass(arg1);
    return ret;
};

export function __wbg_finish_5153789564a5eee5(arg0) {
    const ret = arg0.finish();
    return ret;
};

export function __wbg_gpu_24536c9523d924b1(arg0) {
    const ret = arg0.gpu;
    return ret;
};

export function __wbg_end_bdfb66792e0c59a2(arg0) {
    arg0.end();
};

export function __wbg_draw_2f6ba330409db18a(arg0, arg1) {
    arg0.draw(arg1 >>> 0);
};

export function __wbg_setPipeline_18ce556bdea62cc5(arg0, arg1) {
    arg0.setPipeline(arg1);
};

export function __wbg_setVertexBuffer_7fca5cf8722e2c4a(arg0, arg1, arg2) {
    arg0.setVertexBuffer(arg1 >>> 0, arg2);
};

export function __wbg_nodeName_52cfd8a325f14a75(arg0, arg1) {
    const ret = arg1.nodeName;
    const ptr1 = passStringToWasm0(ret, wasm.__wbindgen_malloc, wasm.__wbindgen_realloc);
    const len1 = WASM_VECTOR_LEN;
    getInt32Memory0()[arg0 / 4 + 1] = len1;
    getInt32Memory0()[arg0 / 4 + 0] = ptr1;
};

export function __wbg_childNodes_64dab37cf9d252dd(arg0) {
    const ret = arg0.childNodes;
    return ret;
};

export function __wbg_nextSibling_304d9aac7c2774ae(arg0) {
    const ret = arg0.nextSibling;
    return isLikeNone(ret) ? 0 : addToExternrefTable0(ret);
};

export function __wbg_settextContent_28d80502cf08bde7(arg0, arg1, arg2) {
    var v0 = getCachedStringFromWasm0(arg1, arg2);
    arg0.textContent = v0;
};

export function __wbg_appendChild_51339d4cde00ee22() { return handleError(function (arg0, arg1) {
    const ret = arg0.appendChild(arg1);
    return ret;
}, arguments) };

export function __wbg_cloneNode_1f7cce4ea8b708e2() { return handleError(function (arg0) {
    const ret = arg0.cloneNode();
    return ret;
}, arguments) };

export function __wbg_requestDevice_0c06b3bc58737ad1(arg0) {
    const ret = arg0.requestDevice();
    return ret;
};

export function __wbg_new_898a68150f225f2e() {
    const ret = new Array();
    return ret;
};

export function __wbg_push_ca1c26067ef907ac(arg0, arg1) {
    const ret = arg0.push(arg1);
    return ret;
};

export function __wbg_newnoargs_581967eacc0e2604(arg0, arg1) {
    var v0 = getCachedStringFromWasm0(arg0, arg1);
    const ret = new Function(v0);
    return ret;
};

export function __wbg_call_cb65541d95d71282() { return handleError(function (arg0, arg1) {
    const ret = arg0.call(arg1);
    return ret;
}, arguments) };

export function __wbg_call_01734de55d61e11d() { return handleError(function (arg0, arg1, arg2) {
    const ret = arg0.call(arg1, arg2);
    return ret;
}, arguments) };

export function __wbg_is_205d914af04a8faa(arg0, arg1) {
    const ret = Object.is(arg0, arg1);
    return ret;
};

export function __wbg_new_b51585de1b234aff() {
    const ret = new Object();
    return ret;
};

export function __wbg_resolve_53698b95aaf7fcf8(arg0) {
    const ret = Promise.resolve(arg0);
    return ret;
};

export function __wbg_then_f7e06ee3c11698eb(arg0, arg1) {
    const ret = arg0.then(arg1);
    return ret;
};

export function __wbg_then_b2267541e2a73865(arg0, arg1, arg2) {
    const ret = arg0.then(arg1, arg2);
    return ret;
};

export function __wbg_globalThis_1d39714405582d3c() { return handleError(function () {
    const ret = globalThis.globalThis;
    return ret;
}, arguments) };

export function __wbg_self_1ff1d729e9aae938() { return handleError(function () {
    const ret = self.self;
    return ret;
}, arguments) };

export function __wbg_window_5f4faef6c12b79ec() { return handleError(function () {
    const ret = window.window;
    return ret;
}, arguments) };

export function __wbg_global_651f05c6a0944d1c() { return handleError(function () {
    const ret = global.global;
    return ret;
}, arguments) };

export function __wbg_new_d086a66d1c264b3f(arg0) {
    const ret = new Float32Array(arg0);
    return ret;
};

export function __wbg_subarray_6814da0bb52e50aa(arg0, arg1, arg2) {
    const ret = arg0.subarray(arg1 >>> 0, arg2 >>> 0);
    return ret;
};

export function __wbg_byteLength_6d476b29e9708b42(arg0) {
    const ret = arg0.byteLength;
    return ret;
};

export function __wbg_buffer_085ec1f694018c4f(arg0) {
    const ret = arg0.buffer;
    return ret;
};

export function __wbg_get_97b561fb56f034b5() { return handleError(function (arg0, arg1) {
    const ret = Reflect.get(arg0, arg1);
    return ret;
}, arguments) };

export function __wbg_set_092e06b0f9d71865() { return handleError(function (arg0, arg1, arg2) {
    const ret = Reflect.set(arg0, arg1, arg2);
    return ret;
}, arguments) };

export function __wbindgen_debug_string(arg0, arg1) {
    const ret = debugString(arg1);
    const ptr1 = passStringToWasm0(ret, wasm.__wbindgen_malloc, wasm.__wbindgen_realloc);
    const len1 = WASM_VECTOR_LEN;
    getInt32Memory0()[arg0 / 4 + 1] = len1;
    getInt32Memory0()[arg0 / 4 + 0] = ptr1;
};

export function __wbindgen_throw(arg0, arg1) {
    throw new Error(getStringFromWasm0(arg0, arg1));
};

export function __wbindgen_memory() {
    const ret = wasm.memory;
    return ret;
};

export function __wbindgen_closure_wrapper1065(arg0, arg1, arg2) {
    const ret = makeClosure(arg0, arg1, 132, __wbg_adapter_24);
    return ret;
};

export function __wbindgen_closure_wrapper2906(arg0, arg1, arg2) {
    const ret = makeMutClosure(arg0, arg1, 245, __wbg_adapter_27);
    return ret;
};

export function __wbindgen_closure_wrapper7014(arg0, arg1, arg2) {
    const ret = makeMutClosure(arg0, arg1, 280, __wbg_adapter_30);
    return ret;
};

export function __wbindgen_init_externref_table() {
    const table = wasm.__wbindgen_export_2;
    const offset = table.grow(4);
    table.set(0, undefined);
    table.set(offset + 0, undefined);
    table.set(offset + 1, null);
    table.set(offset + 2, true);
    table.set(offset + 3, false);
    ;
};

