"use client";

import { Plus, RefreshCw } from "lucide-react";
import { FormEvent, useState } from "react";

type Field = {
  key: string;
  label: string;
  type?: "text" | "textarea" | "tags";
  placeholder?: string;
};

type ResourceManagerProps<T extends { id: number; name: string }> = {
  title: string;
  description: string;
  items: T[];
  fields: Field[];
  onCreate: (data: Record<string, unknown>) => Promise<void>;
  onRefresh: () => Promise<void>;
  renderMeta: (item: T) => React.ReactNode;
};

function parseFieldValue(field: Field, value: FormDataEntryValue | null): unknown {
  const text = String(value || "").trim();
  if (field.type === "tags") {
    return text ? text.split(",").map((item) => item.trim()).filter(Boolean) : [];
  }
  return text || undefined;
}

export function ResourceManager<T extends { id: number; name: string }>({
  title,
  description,
  items,
  fields,
  onCreate,
  onRefresh,
  renderMeta,
}: ResourceManagerProps<T>) {
  const [busy, setBusy] = useState(false);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setBusy(true);
    try {
      const formData = new FormData(event.currentTarget);
      const data = Object.fromEntries(fields.map((field) => [field.key, parseFieldValue(field, formData.get(field.key))]));
      await onCreate(data);
      event.currentTarget.reset();
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
          <article key={item.id} className="rounded-lg border border-neutral-200 bg-white p-4 shadow-sm">
            <h3 className="font-semibold">{item.name}</h3>
            <div className="mt-2 text-sm text-neutral-600">{renderMeta(item)}</div>
          </article>
        ))}
        {items.length === 0 ? <div className="rounded-lg border border-dashed border-neutral-300 p-6 text-sm text-neutral-500">No saved items yet.</div> : null}
      </div>
    </section>
  );
}
