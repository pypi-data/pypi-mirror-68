import { HTMLBox, HTMLBoxView } from "@bokehjs/models/layouts/html_box";
import * as p from "@bokehjs/core/properties";
import { ModelBundle } from "./manager";
export declare class IPyWidgetView extends HTMLBoxView {
    model: IPyWidget;
    private rendered;
    render(): void;
    has_finished(): boolean;
    _render(): Promise<void>;
}
export declare namespace IPyWidget {
    type Attrs = p.AttrsOf<Props>;
    type Props = HTMLBox.Props & {
        bundle: p.Property<ModelBundle>;
    };
}
export interface IPyWidget extends IPyWidget.Attrs {
}
export declare class IPyWidget extends HTMLBox {
    properties: IPyWidget.Props;
    constructor(attrs?: Partial<IPyWidget.Attrs>);
    static __name__: string;
    static __module__: string;
    static init_IPyWidget(): void;
    protected _doc_attached(): void;
}
