export interface WillUIOptions {
  tabs?: boolean;
  inputs?: boolean;
  textareas?: boolean;
  steppers?: boolean;
  collections?: boolean;
}

export interface WillTabOptions {
  label?: string;
  value?: string;
  count?: number;
  panelId?: string;
  panelContent?: string;
}

export declare function initTabs(root?: ParentNode): void;
export declare function addTab(tablist: HTMLElement, options?: WillTabOptions): HTMLButtonElement;
export declare function removeTab(tablist: HTMLElement, tab?: HTMLElement): boolean;
export declare function initInputs(root?: ParentNode): void;
export declare function initTextareas(root?: ParentNode): void;
export declare function initSteppers(root?: ParentNode): void;
export declare function addStep(stepper: HTMLElement, label?: string): HTMLButtonElement;
export declare function removeStep(stepper: HTMLElement, step?: HTMLElement): boolean;
export declare function initCollectionControls(root?: ParentNode): void;
export declare function initWillUI(root?: ParentNode, options?: WillUIOptions): void;
