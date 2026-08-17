const changeEvent = (detail) =>
  new CustomEvent("will:change", { bubbles: true, detail });

const getItems = (root, selector) =>
  Array.from(root.querySelectorAll(selector));

const tabControllers = new WeakMap();
const stepControllers = new WeakMap();

const getPanel = (tab) => {
  const panelId = tab.getAttribute("aria-controls");
  return panelId ? tab.ownerDocument.getElementById(panelId) : null;
};

const ensureTabController = (tablist) => {
  const existing = tabControllers.get(tablist);
  if (existing) return existing;

  const tabs = () => getItems(tablist, ".will-tab");
  const select = (nextTab, focus = false, emit = true) => {
    if (!nextTab || !tablist.contains(nextTab)) return;

    tabs().forEach((tab) => {
      const selected = tab === nextTab;
      const panel = getPanel(tab);
      tab.setAttribute("role", "tab");
      tab.setAttribute("aria-selected", String(selected));
      tab.tabIndex = selected ? 0 : -1;

      if (panel) {
        panel.hidden = !selected;
        panel.setAttribute("role", "tabpanel");
      }
    });

    if (focus) nextTab.focus();
    if (emit) {
      tablist.dispatchEvent(
        changeEvent({
          component: "tabs",
          value: nextTab.dataset.value ?? nextTab.textContent?.trim() ?? "",
        }),
      );
    }
  };

  const controller = { tabs, select };
  tabControllers.set(tablist, controller);
  return controller;
};

export function initTabs(root = document) {
  getItems(root, ".will-tabs").forEach((tablist) => {
    if (tablist.dataset.willReady === "true") return;

    const controller = ensureTabController(tablist);
    if (!controller.tabs().length) return;

    tablist.dataset.willReady = "true";
    tablist.setAttribute("role", "tablist");

    const selected =
      controller.tabs().find((tab) => tab.getAttribute("aria-selected") === "true") ??
      controller.tabs()[0];
    controller.select(selected, false, false);

    tablist.addEventListener("click", (event) => {
      const tab = event.target.closest(".will-tab");
      if (tab && tablist.contains(tab)) controller.select(tab);
    });

    tablist.addEventListener("keydown", (event) => {
      const tab = event.target.closest(".will-tab");
      if (!tab || !tablist.contains(tab)) return;

      const tabs = controller.tabs();
      const index = tabs.indexOf(tab);
      let targetIndex = index;
      if (event.key === "ArrowRight") targetIndex = (index + 1) % tabs.length;
      if (event.key === "ArrowLeft")
        targetIndex = (index - 1 + tabs.length) % tabs.length;
      if (event.key === "Home") targetIndex = 0;
      if (event.key === "End") targetIndex = tabs.length - 1;
      if (targetIndex === index) return;
      event.preventDefault();
      controller.select(tabs[targetIndex], true);
    });
  });
}

export function addTab(tablist, options = {}) {
  const controller = ensureTabController(tablist);
  const nextIndex = Number(tablist.dataset.willNextTab ?? controller.tabs().length + 1);
  tablist.dataset.willNextTab = String(nextIndex + 1);

  const label = options.label ?? `Tab ${nextIndex}`;
  const value = options.value ?? `tab-${nextIndex}`;
  const panelId =
    options.panelId ?? `${tablist.id || "will-tabs"}-panel-${nextIndex}`;
  const tab = tablist.ownerDocument.createElement("button");
  tab.className = "will-tab";
  tab.type = "button";
  tab.dataset.value = value;
  tab.setAttribute("aria-controls", panelId);
  tab.append(label, " ");

  const count = tablist.ownerDocument.createElement("span");
  count.className = "will-tab__count";
  count.textContent = String(options.count ?? 0);
  tab.append(count);
  tablist.append(tab);

  const group = tablist.closest("[data-will-tab-group]") ?? tablist.parentElement;
  if (group) {
    const panel = tablist.ownerDocument.createElement("div");
    panel.id = panelId;
    panel.className = "will-tab-panel tab-panel-demo";
    panel.textContent = options.panelContent ?? `${label} 内容`;
    group.append(panel);
  }

  controller.select(tab, true);
  return tab;
}

export function removeTab(tablist, tab) {
  const controller = ensureTabController(tablist);
  const tabs = controller.tabs();
  if (tabs.length <= 1) return false;

  const target =
    tab ?? tabs.find((item) => item.getAttribute("aria-selected") === "true") ?? tabs.at(-1);
  const targetIndex = tabs.indexOf(target);
  if (targetIndex < 0) return false;

  const panel = getPanel(target);
  const wasSelected = target.getAttribute("aria-selected") === "true";
  target.remove();
  panel?.remove();

  if (wasSelected) {
    const remaining = controller.tabs();
    controller.select(remaining[Math.min(targetIndex, remaining.length - 1)], true);
  }
  return true;
}

export function initInputs(root = document) {
  getItems(root, "[data-will-clearable]").forEach((control) => {
    if (control.dataset.willReady === "true") return;

    const input = control.querySelector("input");
    const clearButton = control.querySelector(".will-input__clear");
    if (!input || !clearButton) return;

    control.dataset.willReady = "true";
    const sync = () => control.classList.toggle("has-value", input.value.length > 0);

    input.addEventListener("input", sync);
    clearButton.addEventListener("click", () => {
      input.value = "";
      sync();
      input.focus();
      input.dispatchEvent(new Event("input", { bubbles: true }));
    });
    sync();
  });
}

export function initTextareas(root = document) {
  getItems(root, "textarea[data-will-autogrow]").forEach((textarea) => {
    if (textarea.dataset.willReady === "true") return;

    textarea.dataset.willReady = "true";
    const resize = () => {
      textarea.style.height = "auto";
      textarea.style.height = `${textarea.scrollHeight}px`;
    };

    textarea.addEventListener("input", resize);
    resize();
  });
}

function ensureStepController(stepper) {
  const existing = stepControllers.get(stepper);
  if (existing) return existing;

  const steps = () => getItems(stepper, ".will-step");
  const select = (nextIndex, focus = false, emit = true) => {
    const items = steps();
    if (!items.length) return;
    const safeIndex = Math.max(0, Math.min(nextIndex, items.length - 1));

    items.forEach((step, index) => {
      const state =
        index < safeIndex ? "complete" : index === safeIndex ? "current" : "pending";
      step.dataset.state = state;
      step.setAttribute("role", "listitem");
      step.setAttribute("aria-current", state === "current" ? "step" : "false");
      step.tabIndex = state === "current" ? 0 : -1;
      const number = step.querySelector(".will-step__number");
      if (number) number.textContent = String(index + 1);
    });

    if (focus) items[safeIndex].focus();
    if (emit) {
      stepper.dispatchEvent(
        changeEvent({
          component: "steps",
          value: safeIndex,
          label: items[safeIndex].querySelector(".will-step__label")?.textContent?.trim() ?? "",
        }),
      );
    }
  };

  const controller = { steps, select };
  stepControllers.set(stepper, controller);
  return controller;
}

export function initSteppers(root = document) {
  getItems(root, ".will-steps[data-interactive]").forEach((stepper) => {
    if (stepper.dataset.willReady === "true") return;

    const controller = ensureStepController(stepper);
    if (!controller.steps().length) return;

    stepper.dataset.willReady = "true";
    stepper.setAttribute("role", "list");

    const initialIndex = Math.max(
      0,
      controller.steps().findIndex((step) => step.dataset.state === "current"),
    );
    controller.select(initialIndex, false, false);

    stepper.addEventListener("click", (event) => {
      const step = event.target.closest(".will-step");
      if (!step || !stepper.contains(step)) return;
      controller.select(controller.steps().indexOf(step));
    });

    stepper.addEventListener("keydown", (event) => {
      if (!["ArrowRight", "ArrowLeft", "Home", "End"].includes(event.key)) return;
      const step = event.target.closest(".will-step");
      if (!step || !stepper.contains(step)) return;

      event.preventDefault();
      const steps = controller.steps();
      const index = steps.indexOf(step);
      let nextIndex = index;
      if (event.key === "ArrowRight") nextIndex = Math.min(index + 1, steps.length - 1);
      if (event.key === "ArrowLeft") nextIndex = Math.max(index - 1, 0);
      if (event.key === "Home") nextIndex = 0;
      if (event.key === "End") nextIndex = steps.length - 1;
      controller.select(nextIndex, true);
    });
  });
}

export function addStep(stepper, label) {
  const controller = ensureStepController(stepper);
  const nextIndex = Number(stepper.dataset.willNextStep ?? controller.steps().length + 1);
  stepper.dataset.willNextStep = String(nextIndex + 1);

  const step = stepper.ownerDocument.createElement("button");
  step.className = "will-step";
  step.type = "button";

  const content = stepper.ownerDocument.createElement("span");
  content.className = "will-step__content";
  const marker = stepper.ownerDocument.createElement("span");
  marker.className = "will-step__marker";
  const number = stepper.ownerDocument.createElement("span");
  number.className = "will-step__number";
  const labelElement = stepper.ownerDocument.createElement("span");
  labelElement.className = "will-step__label";
  labelElement.textContent = label ?? `新步骤 ${nextIndex}`;
  const bar = stepper.ownerDocument.createElement("span");
  bar.className = "will-step__bar";
  marker.append(number);
  content.append(marker, labelElement);
  step.append(content, bar);
  stepper.append(step);

  controller.select(controller.steps().length - 1, true);
  return step;
}

export function removeStep(stepper, step) {
  const controller = ensureStepController(stepper);
  const steps = controller.steps();
  if (steps.length <= 1) return false;

  const target =
    step ?? steps.find((item) => item.dataset.state === "current") ?? steps.at(-1);
  const targetIndex = steps.indexOf(target);
  if (targetIndex < 0) return false;

  target.remove();
  controller.select(Math.min(targetIndex, controller.steps().length - 1), true);
  return true;
}

export function initCollectionControls(root = document) {
  getItems(root, "[data-will-action][data-will-target]").forEach((button) => {
    if (button.dataset.willReady === "true") return;
    button.dataset.willReady = "true";

    const getTarget = () => button.ownerDocument.querySelector(button.dataset.willTarget);
    const sync = () => {
      const target = getTarget();
      if (!target) return;
      const isRemove = button.dataset.willAction.startsWith("remove-");
      const itemSelector = target.matches(".will-tabs") ? ".will-tab" : ".will-step";
      if (isRemove) button.disabled = getItems(target, itemSelector).length <= 1;
    };

    button.addEventListener("click", () => {
      const target = getTarget();
      if (!target) return;

      const action = button.dataset.willAction;
      if (action === "add-tab") addTab(target);
      if (action === "remove-tab") removeTab(target);
      if (action === "add-step") addStep(target);
      if (action === "remove-step") removeStep(target);

      getItems(root, `[data-will-target="${button.dataset.willTarget}"]`).forEach(
        (control) => {
          const isRemove = control.dataset.willAction.startsWith("remove-");
          const itemSelector = target.matches(".will-tabs") ? ".will-tab" : ".will-step";
          if (isRemove) control.disabled = getItems(target, itemSelector).length <= 1;
        },
      );
    });
    sync();
  });
}

export function initWillUI(root = document, options = {}) {
  const config = {
    tabs: true,
    inputs: true,
    textareas: true,
    steppers: true,
    collections: true,
    ...options,
  };

  if (config.tabs) initTabs(root);
  if (config.inputs) initInputs(root);
  if (config.textareas) initTextareas(root);
  if (config.steppers) initSteppers(root);
  if (config.collections) initCollectionControls(root);
}
