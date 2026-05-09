"use client";

import { Archive, Clipboard, Copy, RefreshCw, Send, Trash2 } from "lucide-react";
import { FormEvent, useMemo, useState } from "react";
import { ContentProfile, Post } from "@/lib/api";

const statuses = ["draft", "liked", "planned", "published", "archived"];

type HistoryWorkspaceProps = {
  posts: Post[];
  profiles: ContentProfile[];
  onUpdatePost: (id: number, data: Partial<Post>) => Promise<void>;
  onDeletePost: (id: number) => Promise<void>;
  onReusePost: (post: Post) => void;
  onRefresh: () => Promise<void>;
};

function formatDate(value: string): string {
  return new Intl.DateTimeFormat("en", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value));
}

function textFromValue(value: unknown): string {
  if (typeof value === "string") {
    return value;
  }
  if (Array.isArray(value)) {
    return value.map(textFromValue).filter(Boolean).join("\n\n");
  }
  if (value && typeof value === "object") {
    const record = value as Record<string, unknown>;
    const preferred = ["post", "text", "caption", "content", "body", "script"];
    for (const key of preferred) {
      const text = textFromValue(record[key]);
      if (text) {
        return text;
      }
    }
  }
  return "";
}

function generatedText(post: Post): string {
  return Object.entries(post.generated_content)
    .map(([platform, value]) => {
      const text = textFromValue(value);
      return text ? `${platform}\n${text}` : "";
    })
    .filter(Boolean)
    .join("\n\n---\n\n");
}

function imagePromptText(post: Post): string {
  const prompt = typeof post.image_prompt.prompt === "string" ? post.image_prompt.prompt : "";
  const negative = typeof post.image_prompt.negative_prompt === "string" ? post.image_prompt.negative_prompt : "";
  const textOnImage = typeof post.image_prompt.text_on_image === "string" ? post.image_prompt.text_on_image : "";
  return [prompt, negative ? `Negative: ${negative}` : "", textOnImage ? `Text on image: ${textOnImage}` : ""].filter(Boolean).join("\n");
}

export function HistoryWorkspace({ posts, profiles, onUpdatePost, onDeletePost, onReusePost, onRefresh }: HistoryWorkspaceProps) {
  const [selectedId, setSelectedId] = useState<number | null>(posts[0]?.id ?? null);
  const selectedPost = useMemo(() => posts.find((post) => post.id === selectedId) ?? posts[0] ?? null, [posts, selectedId]);
  const selectedProfile = profiles.find((profile) => profile.id === selectedPost?.profile_id);
  const [busy, setBusy] = useState(false);
  const [copied, setCopied] = useState<string | null>(null);

  async function saveMetadata(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!selectedPost) {
      return;
    }
    const form = new FormData(event.currentTarget);
    const status = String(form.get("status") || "draft");
    const tagsText = String(form.get("tags") || "");
    const notes = String(form.get("notes") || "");
    setBusy(true);
    try {
      await onUpdatePost(selectedPost.id, {
        status,
        tags: tagsText.split(",").map((tag) => tag.trim()).filter(Boolean),
        notes: notes.trim() || null,
      });
    } finally {
      setBusy(false);
    }
  }

  async function archivePost() {
    if (!selectedPost) {
      return;
    }
    setBusy(true);
    try {
      await onUpdatePost(selectedPost.id, { status: "archived" });
    } finally {
      setBusy(false);
    }
  }

  async function removePost() {
    if (!selectedPost || !window.confirm(`Delete "${selectedPost.topic}"?`)) {
      return;
    }
    setBusy(true);
    try {
      await onDeletePost(selectedPost.id);
      setSelectedId(null);
    } finally {
      setBusy(false);
    }
  }

  async function copyText(label: string, value: string) {
    if (!value) {
      return;
    }
    await navigator.clipboard.writeText(value);
    setCopied(label);
    window.setTimeout(() => setCopied(null), 1600);
  }

  if (!selectedPost) {
    return (
      <section className="grid gap-4">
        <div className="flex items-center justify-between gap-3">
          <h1 className="text-2xl font-semibold">History</h1>
          <button type="button" onClick={onRefresh} className="inline-flex items-center gap-2 rounded-md border border-neutral-300 px-3 py-2 text-sm">
            <RefreshCw size={16} />
            Refresh
          </button>
        </div>
        <div className="rounded-lg border border-dashed border-neutral-300 p-6 text-sm text-neutral-500">No generated posts yet.</div>
      </section>
    );
  }

  return (
    <section className="grid gap-4 xl:grid-cols-[340px_1fr]">
      <div className="grid content-start gap-3">
        <div className="flex items-center justify-between gap-3">
          <h1 className="text-2xl font-semibold">History</h1>
          <button type="button" onClick={onRefresh} className="inline-flex items-center gap-2 rounded-md border border-neutral-300 px-3 py-2 text-sm">
            <RefreshCw size={16} />
            Refresh
          </button>
        </div>
        {posts.map((post) => (
          <button
            key={post.id}
            type="button"
            onClick={() => setSelectedId(post.id)}
            className={`rounded-lg border bg-white p-3 text-left shadow-sm hover:bg-neutral-50 ${
              selectedPost.id === post.id ? "border-neutral-900" : "border-neutral-200"
            }`}
          >
            <div className="font-medium">{post.topic}</div>
            <div className="mt-2 flex flex-wrap items-center gap-2 text-xs text-neutral-500">
              <span className="rounded-md bg-neutral-100 px-2 py-1">{post.status}</span>
              <span>{formatDate(post.created_at)}</span>
            </div>
          </button>
        ))}
      </div>

      <article className="rounded-lg border border-neutral-200 bg-white p-4 shadow-sm">
        <div className="flex flex-wrap items-start justify-between gap-3">
          <div>
            <h2 className="text-xl font-semibold">{selectedPost.topic}</h2>
            <div className="mt-2 flex flex-wrap gap-2 text-xs text-neutral-500">
              <span>{selectedProfile?.name || "Profile not set"}</span>
              <span>{selectedPost.model_used || "model not saved"}</span>
              <span>{formatDate(selectedPost.created_at)}</span>
            </div>
          </div>
          <div className="flex flex-wrap gap-2">
            <button
              type="button"
              onClick={() => void copyText("content", generatedText(selectedPost))}
              className="inline-flex items-center gap-2 rounded-md border border-neutral-300 px-3 py-2 text-sm hover:bg-neutral-50"
            >
              <Copy size={16} />
              Copy Text
            </button>
            <button
              type="button"
              onClick={() => void copyText("image", imagePromptText(selectedPost))}
              className="inline-flex items-center gap-2 rounded-md border border-neutral-300 px-3 py-2 text-sm hover:bg-neutral-50"
            >
              <Clipboard size={16} />
              Copy Image Prompt
            </button>
            <button
              type="button"
              onClick={() => onReusePost(selectedPost)}
              className="inline-flex items-center gap-2 rounded-md bg-neutral-900 px-3 py-2 text-sm font-medium text-white"
            >
              <Send size={16} />
              Reuse
            </button>
          </div>
        </div>
        {copied ? <div className="mt-3 rounded-md bg-green-50 px-3 py-2 text-sm text-green-700">Copied {copied}.</div> : null}

        <form key={selectedPost.id} onSubmit={saveMetadata} className="mt-4 grid gap-3 rounded-lg border border-neutral-200 p-3 sm:grid-cols-[160px_1fr]">
          <label className="grid gap-1 text-sm font-medium text-neutral-700">
            Status
            <select name="status" defaultValue={selectedPost.status} className="rounded-md border border-neutral-300 px-3 py-2 outline-none focus:border-neutral-900">
              {statuses.map((item) => (
                <option key={item} value={item}>
                  {item}
                </option>
              ))}
            </select>
          </label>
          <label className="grid gap-1 text-sm font-medium text-neutral-700">
            Tags
            <input name="tags" defaultValue={selectedPost.tags.join(", ")} placeholder="workflow, launch, x" className="rounded-md border border-neutral-300 px-3 py-2 outline-none focus:border-neutral-900" />
          </label>
          <label className="grid gap-1 text-sm font-medium text-neutral-700 sm:col-span-2">
            Notes
            <textarea name="notes" defaultValue={selectedPost.notes || ""} className="min-h-24 rounded-md border border-neutral-300 px-3 py-2 outline-none focus:border-neutral-900" />
          </label>
          <div className="flex flex-wrap gap-2 sm:col-span-2">
            <button disabled={busy} className="rounded-md bg-neutral-900 px-3 py-2 text-sm font-medium text-white">Save Metadata</button>
            <button type="button" disabled={busy} onClick={() => void archivePost()} className="inline-flex items-center gap-2 rounded-md border border-neutral-300 px-3 py-2 text-sm">
              <Archive size={16} />
              Archive
            </button>
            <button type="button" disabled={busy} onClick={() => void removePost()} className="inline-flex items-center gap-2 rounded-md border border-red-200 px-3 py-2 text-sm text-red-700">
              <Trash2 size={16} />
              Delete
            </button>
          </div>
        </form>

        <div className="mt-4 grid gap-4">
          <section>
            <h3 className="font-semibold">Generated Content</h3>
            <pre className="mt-2 max-h-96 overflow-auto rounded-md bg-neutral-950 p-4 text-xs leading-relaxed text-neutral-50">{JSON.stringify(selectedPost.generated_content, null, 2)}</pre>
          </section>
          <section>
            <h3 className="font-semibold">Image Prompt</h3>
            <pre className="mt-2 max-h-60 overflow-auto rounded-md bg-neutral-950 p-4 text-xs leading-relaxed text-neutral-50">{JSON.stringify(selectedPost.image_prompt, null, 2)}</pre>
          </section>
          <section>
            <h3 className="font-semibold">Analysis</h3>
            <pre className="mt-2 max-h-80 overflow-auto rounded-md bg-neutral-950 p-4 text-xs leading-relaxed text-neutral-50">{JSON.stringify(selectedPost.analysis, null, 2)}</pre>
          </section>
        </div>
      </article>
    </section>
  );
}
