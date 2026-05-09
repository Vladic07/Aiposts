"use client";

import { Save } from "lucide-react";
import { FormEvent, useState } from "react";
import { Settings } from "@/lib/api";

type SettingsPanelProps = {
  settings: Settings | null;
  onSave: (data: Partial<Settings>) => Promise<void>;
};

export function SettingsPanel({ settings, onSave }: SettingsPanelProps) {
  const [busy, setBusy] = useState(false);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    setBusy(true);
    try {
      await onSave({
        provider: String(form.get("provider") || "openai"),
        text_model: String(form.get("text_model") || "gpt-5-mini"),
        fast_model: String(form.get("fast_model") || "gpt-5-mini"),
        quality_model: String(form.get("quality_model") || "gpt-5.2"),
        image_model: String(form.get("image_model") || "gpt-image-1.5"),
        daily_generation_limit: Number(form.get("daily_generation_limit") || 100),
        default_language: String(form.get("default_language") || "ru"),
      });
    } finally {
      setBusy(false);
    }
  }

  if (!settings) {
    return <div className="rounded-lg border border-dashed border-neutral-300 p-6 text-sm text-neutral-500">Settings are loading.</div>;
  }

  return (
    <form onSubmit={submit} className="max-w-3xl rounded-lg border border-neutral-200 bg-white p-4 shadow-sm">
      <div>
        <h1 className="text-2xl font-semibold">Settings</h1>
        <p className="mt-1 text-sm text-neutral-600">Model and generation defaults used by the backend.</p>
      </div>
      <div className="mt-4 grid gap-3 sm:grid-cols-2">
        <label className="grid gap-1 text-sm font-medium text-neutral-700">
          Provider
          <input name="provider" defaultValue={settings.provider} className="rounded-md border border-neutral-300 px-3 py-2 outline-none focus:border-neutral-900" />
        </label>
        <label className="grid gap-1 text-sm font-medium text-neutral-700">
          Default Language
          <input name="default_language" defaultValue={settings.default_language} className="rounded-md border border-neutral-300 px-3 py-2 outline-none focus:border-neutral-900" />
        </label>
        <label className="grid gap-1 text-sm font-medium text-neutral-700">
          Text Model
          <input name="text_model" defaultValue={settings.text_model} className="rounded-md border border-neutral-300 px-3 py-2 outline-none focus:border-neutral-900" />
        </label>
        <label className="grid gap-1 text-sm font-medium text-neutral-700">
          Fast Model
          <input name="fast_model" defaultValue={settings.fast_model} className="rounded-md border border-neutral-300 px-3 py-2 outline-none focus:border-neutral-900" />
        </label>
        <label className="grid gap-1 text-sm font-medium text-neutral-700">
          Quality Model
          <input name="quality_model" defaultValue={settings.quality_model} className="rounded-md border border-neutral-300 px-3 py-2 outline-none focus:border-neutral-900" />
        </label>
        <label className="grid gap-1 text-sm font-medium text-neutral-700">
          Image Model
          <input name="image_model" defaultValue={settings.image_model} className="rounded-md border border-neutral-300 px-3 py-2 outline-none focus:border-neutral-900" />
        </label>
        <label className="grid gap-1 text-sm font-medium text-neutral-700">
          Daily Generation Limit
          <input
            name="daily_generation_limit"
            type="number"
            min={1}
            defaultValue={settings.daily_generation_limit}
            className="rounded-md border border-neutral-300 px-3 py-2 outline-none focus:border-neutral-900"
          />
        </label>
      </div>
      <button disabled={busy} className="mt-4 inline-flex items-center gap-2 rounded-md bg-neutral-900 px-3 py-2 text-sm font-medium text-white">
        <Save size={16} />
        Save Settings
      </button>
    </form>
  );
}
