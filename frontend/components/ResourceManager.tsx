"use client";

import { Check, Pencil, Plus, RefreshCw, Trash2, X } from "lucide-react";
import { FormEvent, useState } from "react";

export type ResourceField = {
  key: string;
  label: string;
  type?: "text" | "textarea" | "tags";
  placeholder?: string;
};

type ResourceManagerProps<T extends { id: number; name: string }> = {
  title: string;
  description: string;
  items: T[];
  fields: ResourceField[];
  onCreate: (data: Record<string, unknown>) => Promise<void>;
  onUpdate: (id: number, data: Record<string, unknown>) => Promise<void>;
  onDelete: (id: number) => Promise<void>;
  onRefresh: () => Promise<void>;
  renderMeta: (item: T) => React.ReactNode;
  activeItemId?: number | null;
  onSelectItem?: (item: T) => void;
  selectLabel?: string;
};

function parseFieldValue(field: ResourceField, value: FormDataEntryValue | null): unknown {
  const text = String(value || "").trim();
  if (field.type === "tags") {
    return text ? text.split(",").map((item) => item.trim()).filter(Boolean) : [];
  }
  return text || undefined;
}

function formatFieldValue(value: unknown): string {
  if (Array.isArray(value)) {
    return value.join(", ");
  }
  if (typeof value === "string") {
    return value;
  }
  if (value == null) {
    return "";
  }
  return String(value);
}

function dataFromForm(fields: ResourceField[], form: HTMLFormElement): Record<string, unknown> {
  const formData = new FormData(form);
  return Object.fromEntries(fields.map((field) => [field.key, parseFieldValue(field, formData.get(field.key))]));
}

export function ResourceManager<T extends { id: number; name: string }>({
  title,
  description,
  items,
  fields,
  onCreate,
  onUpdate,
  onDelete,
  onRefresh,
  renderMeta,
  activeItemId,
  onSelectItem,
  selectLabel = "Use",
}: ResourceManagerProps<T>) {
  const [busy, setBusy] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setBusy(true);
    try {
      const data = dataFromForm(fields, event.currentTarget);
      await onCreate(data);
      event.currentTarget.reset();
    } finally {
      setBusy(false);
    }
  }

  async function submitEdit(item: T, event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setBusy(true);
    try {
      await onUpdate(item.id, dataFromForm(fields, event.currentTarget));
      setEditingId(null);
    } finally {
      setBusy(false);
    }
  }

  async function remove(item: T) {
    const confirmed = window.confirm(`Delete "${item.name}"?`);
    if (!confirmed) {
      return;
    }
    setBusy(true);
    try {
      await onDelete(item.id);
      if (editingId === item.id) {
        setEditingId(null);
      }
    } finally {
      setBusy(false);
    }
  }

  return (
    <section className="grid gap-4 lg:grid-cols-[380px_1fr]">
      <form onSubmit={submit} className="rounded-lg border border-neutral-200 bg-white p-4 shadow-sm">
        <div className="mb-4">
          <h2 className="text-lg font-semibold">{title}</h2>
          <p className="mt-1 text-sm text-neutral-600">{description}</p>
        </div>
        <div className="grid gap-3">
          {fields.map((field) => (
            <label key={field.key} className="grid gap-1 text-sm font-medium text-neutral-700">
              {field.label}
              {field.type === "textarea" ? (
                <textarea
                  name={field.key}
                  placeholder={field.placeholder}
                  className="min-h-24 rounded-md border border-neutral-300 bg-white px-3 py-2 text-sm outline-none focus:border-neutral-900"
                />
              ) : (
                <input
                  name={field.key}
                  placeholder={field.placeholder}
                  className="rounded-md border border-neutral-300 bg-white px-3 py-2 text-sm outline-none focus:border-neutral-900"
                />
              )}
            </label>
          ))}
        </div>
        <div className="mt-4 flex gap-2">
          <button disabled={busy} className="inline-flex items-center gap-2 rounded-md bg-neutral-900 px-3 py-2 text-sm font-medium text-white">
            <Plus size={16} />
            Save
          </button>
          <button type="button" onClick={onRefresh} className="inline-flex items-center gap-2 rounded-md border border-neutral-300 px-3 py-2 text-sm">
            <RefreshCw size={16} />
            Refresh
          </button>
        </div>
      </form>
      <div className="grid content-start gap-3">
        {items.map((item) => (
          <article
            key={item.id}
            className={`rounded-lg border bg-white p-4 shadow-sm ${
              activeItemId === item.id ? "border-neutral-900" : "border-neutral-200"
            }`}
          >
            {editingId === item.id ? (
              <form onSubmit={(event) => submitEdit(item, event)} className="grid gap-3">
                {fields.map((field) => (
                  <label key={field.key} className="grid gap-1 text-sm font-medium text-neutral-700">
                    {field.label}
                    {field.type === "textarea" ? (
                      <textarea
                        name={field.key}
                        defaultValue={formatFieldValue((item as Record<string, unknown>)[field.key])}
                        placeholder={field.placeholder}
                        className="min-h-24 rounded-md border border-neutral-300 bg-white px-3 py-2 text-sm outline-none focus:border-neutral-900"
                      />
                    ) : (
                      <input
                        name={field.key}
                        defaultValue={formatFieldValue((item as Record<string, unknown>)[field.key])}
                        placeholder={field.placeholder}
                        className="rounded-md border border-neutral-300 bg-white px-3 py-2 text-sm outline-none focus:border-neutral-900"
                      />
                    )}
                  </label>
                ))}
                <div className="flex flex-wrap gap-2">
                  <button disabled={busy} className="inline-flex items-center gap-2 rounded-md bg-neutral-900 px-3 py-2 text-sm font-medium text-white">
                    <Check size={16} />
                    Save
                  </button>
                  <button
                    type="button"
                    disabled={busy}
                    onClick={() => setEditingId(null)}
                    className="inline-flex items-center gap-2 rounded-md border border-neutral-300 px-3 py-2 text-sm"
                  >
                    <X size={16} />
                    Cancel
                  </button>
                </div>
              </form>
            ) : (
              <>
                <div className="flex flex-wrap items-start justify-between gap-3">
                  <div>
                    <h3 className="font-semibold">{item.name}</h3>
                    <div className="mt-2 grid gap-1 text-sm text-neutral-600">{renderMeta(item)}</div>
                  </div>
                  {activeItemId === item.id ? <span className="rounded-md bg-neutral-900 px-2 py-1 text-xs text-white">Active</span> : null}
                </div>
                <div className="mt-4 flex flex-wrap gap-2">
                  {onSelectItem ? (
                    <button
                      type="button"
                      onClick={() => onSelectItem(item)}
                      className="inline-flex items-center gap-2 rounded-md border border-neutral-300 px-3 py-2 text-sm hover:bg-neutral-50"
                    >
                      <Check size={16} />
                      {selectLabel}
                    </button>
                  ) : null}
                  <button
                    type="button"
                    disabled={busy}
                    onClick={() => setEditingId(item.id)}
                    className="inline-flex items-center gap-2 rounded-md border border-neutral-300 px-3 py-2 text-sm hover:bg-neutral-50"
                  >
                    <Pencil size={16} />
                    Edit
                  </button>
                  <button
                    type="button"
                    disabled={busy}
                    onClick={() => void remove(item)}
                    className="inline-flex items-center gap-2 rounded-md border border-red-200 px-3 py-2 text-sm text-red-700 hover:bg-red-50"
                  >
                    <Trash2 size={16} />
                    Delete
                  </button>
                </div>
              </>
            )}
          </article>
        ))}
        {items.length === 0 ? <div className="rounded-lg border border-dashed border-neutral-300 p-6 text-sm text-neutral-500">No saved items yet.</div> : null}
      </div>
    </section>
  );
}
