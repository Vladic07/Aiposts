"use client";

import { Send, Star } from "lucide-react";
import { FormEvent, useState } from "react";
import { api, ContentProfile, ImageStyle, Post, TextStyle } from "@/lib/api";

type GeneratePanelProps = {
  profiles: ContentProfile[];
  textStyles: TextStyle[];
  imageStyles: ImageStyle[];
  onGenerated: (post: Post) => void;
};

export function GeneratePanel({ profiles, textStyles, imageStyles, onGenerated }: GeneratePanelProps) {
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState<Post | null>(null);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const platforms = String(form.get("platforms") || "instagram,facebook,x")
      .split(",")
      .map((item) => item.trim())
      .filter(Boolean);
    setBusy(true);
    try {
      const post = await api.generatePost({
        profile_id: Number(form.get("profile_id")),
        text_style_id: form.get("text_style_id") ? Number(form.get("text_style_id")) : null,
        image_style_id: form.get("image_style_id") ? Number(form.get("image_style_id")) : null,
        topic: String(form.get("topic") || ""),
        goal: String(form.get("goal") || ""),
        platforms,
        generation_mode: form.get("generation_mode"),
        language: form.get("language") || "ru",
        save_to_history: true,
      });
      setResult(post);
      onGenerated(post);
    } finally {
      setBusy(false);
    }
  }

  return (
    <section className="grid gap-4 xl:grid-cols-[420px_1fr]">
      <form onSubmit={submit} className="rounded-lg border border-neutral-200 bg-white p-4 shadow-sm">
        <h2 className="text-lg font-semibold">Generate Post</h2>
        <div className="mt-4 grid gap-3">
          <label className="grid gap-1 text-sm font-medium text-neutral-700">
            Topic
            <textarea required name="topic" className="min-h-24 rounded-md border border-neutral-300 px-3 py-2 outline-none focus:border-neutral-900" />
          </label>
          <label className="grid gap-1 text-sm font-medium text-neutral-700">
            Goal
            <input name="goal" className="rounded-md border border-neutral-300 px-3 py-2 outline-none focus:border-neutral-900" />
          </label>
          <label className="grid gap-1 text-sm font-medium text-neutral-700">
            Content Profile
            <select required name="profile_id" className="rounded-md border border-neutral-300 px-3 py-2 outline-none focus:border-neutral-900">
              <option value="">Select profile</option>
              {profiles.map((profile) => (
                <option key={profile.id} value={profile.id}>
                  {profile.name}
                </option>
              ))}
            </select>
          </label>
          <div className="grid gap-3 sm:grid-cols-2">
            <label className="grid gap-1 text-sm font-medium text-neutral-700">
              Text Style
              <select name="text_style_id" className="rounded-md border border-neutral-300 px-3 py-2 outline-none focus:border-neutral-900">
                <option value="">Default</option>
                {textStyles.map((style) => (
                  <option key={style.id} value={style.id}>
                    {style.name}
                  </option>
                ))}
              </select>
            </label>
            <label className="grid gap-1 text-sm font-medium text-neutral-700">
              Image Style
              <select name="image_style_id" className="rounded-md border border-neutral-300 px-3 py-2 outline-none focus:border-neutral-900">
                <option value="">Default</option>
                {imageStyles.map((style) => (
                  <option key={style.id} value={style.id}>
                    {style.name}
                  </option>
                ))}
              </select>
            </label>
          </div>
          <div className="grid gap-3 sm:grid-cols-3">
            <label className="grid gap-1 text-sm font-medium text-neutral-700">
              Mode
              <select name="generation_mode" defaultValue="auto" className="rounded-md border border-neutral-300 px-3 py-2 outline-none focus:border-neutral-900">
                <option value="auto">Auto</option>
                <option value="guided">Guided</option>
              </select>
            </label>
            <label className="grid gap-1 text-sm font-medium text-neutral-700">
              Language
              <input name="language" defaultValue="ru" className="rounded-md border border-neutral-300 px-3 py-2 outline-none focus:border-neutral-900" />
            </label>
            <label className="grid gap-1 text-sm font-medium text-neutral-700">
              Platforms
              <input name="platforms" defaultValue="instagram,facebook,x" className="rounded-md border border-neutral-300 px-3 py-2 outline-none focus:border-neutral-900" />
            </label>
          </div>
        </div>
        <button disabled={busy || profiles.length === 0} className="mt-4 inline-flex items-center gap-2 rounded-md bg-neutral-900 px-3 py-2 text-sm font-medium text-white">
          <Send size={16} />
          Generate
        </button>
      </form>
      <article className="min-h-[420px] rounded-lg border border-neutral-200 bg-white p-4 shadow-sm">
        <h2 className="flex items-center gap-2 text-lg font-semibold">
          <Star size={18} />
          Result
        </h2>
        {result ? (
          <pre className="mt-4 max-h-[620px] overflow-auto rounded-md bg-neutral-950 p-4 text-xs leading-relaxed text-neutral-50">
            {JSON.stringify(
              {
                generated_content: result.generated_content,
                image_prompt: result.image_prompt,
                analysis: result.analysis,
              },
              null,
              2,
            )}
          </pre>
        ) : (
          <p className="mt-4 text-sm text-neutral-600">Generated content will appear here and will also be saved to history.</p>
        )}
      </article>
    </section>
  );
}
