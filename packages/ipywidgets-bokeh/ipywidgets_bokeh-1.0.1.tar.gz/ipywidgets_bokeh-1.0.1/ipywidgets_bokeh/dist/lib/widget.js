import { HTMLBox, HTMLBoxView } from "@bokehjs/models/layouts/html_box";
import { MessageSentEvent } from "@bokehjs/document/events";
import * as p from "@bokehjs/core/properties";
import { isString } from "@bokehjs/core/util/types";
import { require_loader } from "./loader";
import { WidgetManager } from "./manager";
const widget_managers = new WeakMap();
export class IPyWidgetView extends HTMLBoxView {
    constructor() {
        super(...arguments);
        this.rendered = false;
    }
    render() {
        super.render();
        if (!this.rendered) {
            this._render().then(() => {
                this.rendered = true;
                this.invalidate_layout();
                this.notify_finished();
            });
        }
    }
    has_finished() {
        return this.rendered && super.has_finished();
    }
    async _render() {
        const manager = widget_managers.get(this.model.document);
        await manager.render(this.model.bundle, this.el);
    }
}
export class IPyWidget extends HTMLBox {
    constructor(attrs) {
        super(attrs);
    }
    static init_IPyWidget() {
        this.prototype.default_view = IPyWidgetView;
        this.define({
            bundle: [p.Any],
        });
    }
    _doc_attached() {
        const doc = this.document;
        if (!widget_managers.has(doc)) {
            const manager = new WidgetManager({ loader: require_loader });
            widget_managers.set(doc, manager);
            manager.bk_open((data) => {
                const event = new MessageSentEvent(doc, "ipywidgets_bokeh", data);
                doc._trigger_on_change(event);
            });
            doc.on_message("ipywidgets_bokeh", (data) => {
                if (isString(data) || data instanceof ArrayBuffer) {
                    manager.bk_recv(data);
                }
                else {
                    console.error(`expected a string or ArrayBuffer, got ${typeof data}`);
                }
            });
        }
    }
}
IPyWidget.__name__ = "IPyWidget";
IPyWidget.__module__ = "ipywidgets_bokeh.widget";
IPyWidget.init_IPyWidget();
