import { HTMLManager } from "@jupyter-widgets/html-manager";
import { shims } from "@jupyter-widgets/base";
import { KernelManager } from "@jupyterlab/services";
import { isString } from "@bokehjs/core/util/types";
let _kernel_id = 0;
export class WidgetManager extends HTMLManager {
    constructor(options) {
        super(options);
        this._known_models = {};
        this.ws = null;
        const settings = {
            baseUrl: "",
            appUrl: "",
            wsUrl: "",
            token: "",
            init: { cache: "no-store", credentials: "same-origin" },
            fetch: async (_input, _init) => {
                // returns an empty list of kernels to make KernelManager happy
                return new Response("[]", { status: 200 });
            },
            Headers,
            Request,
            WebSocket: this.make_WebSocket(),
        };
        this.kernel_manager = new KernelManager({ serverSettings: settings });
        const kernel_model = { name: "bokeh_kernel", id: `${_kernel_id++}` };
        this.kernel = this.kernel_manager.connectTo({ model: kernel_model, handleComms: true });
        this.kernel.registerCommTarget(this.comm_target_name, (comm, msg) => {
            this.handle_comm_open(new shims.services.Comm(comm), msg);
        });
    }
    make_WebSocket() {
        var _a;
        const manager = this;
        return _a = class PseudoWebSocket {
                constructor(url, _protocols) {
                    this.url = url;
                    this.CLOSED = 0;
                    this.CLOSING = 1;
                    this.CONNECTING = 2;
                    this.OPEN = 3;
                    this.onclose = null;
                    this.onerror = null;
                    this.onmessage = null;
                    this.onopen = null;
                    manager.ws = this;
                }
                close(code, reason) {
                    var _a;
                    const event = new CloseEvent("close", { code, reason });
                    (_a = this.onclose) === null || _a === void 0 ? void 0 : _a.call(this, event);
                }
                send(data) {
                    var _a;
                    if (isString(data) || data instanceof ArrayBuffer) {
                        (_a = manager.bk_send) === null || _a === void 0 ? void 0 : _a.call(manager, data);
                    }
                    else {
                        console.error(`only string and ArrayBuffer types are supported, got ${typeof data}`);
                    }
                }
                addEventListener(_type, _listener, _options) {
                    throw new Error("not implemented");
                }
                removeEventListener(_type, _listener, _options) {
                    throw new Error("not implemented");
                }
                dispatchEvent(_event) {
                    throw new Error("not implemented");
                }
            },
            _a.CLOSED = 0,
            _a.CLOSING = 1,
            _a.CONNECTING = 2,
            _a.OPEN = 3,
            _a;
    }
    bk_open(send_fn) {
        var _a, _b;
        if (this.ws != null) {
            this.bk_send = send_fn;
            (_b = (_a = this.ws).onopen) === null || _b === void 0 ? void 0 : _b.call(_a, new Event("open"));
        }
    }
    bk_recv(data) {
        var _a, _b;
        if (this.ws != null) {
            (_b = (_a = this.ws).onmessage) === null || _b === void 0 ? void 0 : _b.call(_a, new MessageEvent("message", { data }));
        }
    }
    async render(bundle, el) {
        const { spec, state } = bundle;
        const new_models = state.state;
        for (const id in new_models) {
            this._known_models[id] = new_models[id];
        }
        try {
            const models = await this.set_state(state);
            const model = models.find((item) => item.model_id == spec.model_id);
            if (model != null) {
                await this.display_model(undefined, model, { el });
            }
        }
        finally {
            for (const id in new_models) {
                delete this._known_models[id];
            }
        }
    }
    async _create_comm(target_name, model_id, data, metadata, buffers) {
        const comm = this.kernel.createComm(target_name, model_id);
        if (data || metadata) {
            comm.open(data, metadata, buffers);
        }
        return new shims.services.Comm(comm);
    }
    _get_comm_info() {
        return Promise.resolve(this._known_models);
    }
    async new_model(options, serialized_state) {
        // XXX: this is a hack that allows to connect to a live comm and use initial
        // state sent via a state bundle, essentially turning new_model(modelCreate)
        // into new_model(modelCreate, modelState) in ManagerBase.set_state(), possibly
        // breaking safe guard rule (1) of that method. This is done this way to avoid
        // reimplementing set_state().
        if (serialized_state === undefined) {
            const models = this._known_models;
            const { model_id } = options;
            if (model_id != null && models[model_id] != null) {
                const model = models[model_id];
                serialized_state = model.state;
            }
            else
                throw new Error("internal error in new_model()");
        }
        return super.new_model(options, serialized_state);
    }
}
