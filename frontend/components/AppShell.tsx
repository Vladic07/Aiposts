"use client";

import { History, Image, LayoutDashboard, MessageSquareText, PenLine, Settings, Sparkles } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import { api, ContentProfile, ImageStyle, Post, Settings as AppSettings, TextStyle } from "@/lib/api";
import { GeneratePanel } from "@/components/GeneratePanel";
import { ResourceManager } from "@/components/ResourceManager";

type View = "dashboard" | "profiles" | "text" | "image" | "generate" | "history" | "settings";

const nav: { id: View; label: string; icon: React.ComponentType<{ size?: number }> }[] = [
  { id: "dashboard", label: "Dashboard", icon: LayoutDashboard },
  { id: "profiles", label: "Profiles", icon: PenLine },
  { id: "text", label: "Text Styles", icon: MessageSquareText },
  { id: "image", label: "Image Styles", icon: Image },
  { id: "generate", label: "Generate", icon: Sparkles },
  { id: "history", label: "History", icon: History },
  { id: "settings", label: "Settings", icon: Settings },
];

export function AppShell() {
  const [view, setView] = useState<View>("dashboard");
  const [profiles, setProfiles] = useState<ContentProfile[]>([]);
  const [textStyles, setTextStyles] = useState<TextStyle[]>([]);
  const [imageStyles, setImageStyles] = useState<ImageStyle[]>([]);
  const [posts, setPosts] = useState<Post[]>([]);
  const [settings, setSettings] = useState<AppSettings | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function refresh() {
    setError(null);
    try {
      const [profileData, textData, imageData, postData, settingsData] = await Promise.all([
        api.listProfiles(),
        api.listTextStyles(),
        api.listImageStyles(),
        api.listPosts(),
        api.getSettings(),
      ]);
      setProfiles(profileData);
      setTextStyles(textData);
      setImageStyles(imageData);
      setPosts(postData);
      setSettings(settingsData);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Failed to load data");
    }
  }

  useEffect(() => {
    queueMicrotask(() => {
      void refresh();
    });
  }, []);

  const stats = useMemo(
    () => [
      ["Profiles", profiles.length],
      ["Text styles", textStyles.length],
      ["Image styles", imageStyles.length],
      ["Posts", posts.length],
    ],
    [profiles.length, textStyles.length, imageStyles.length, posts.length],
  );

  return (
    <main className="min-h-screen">
      <div className="grid min-h-screen lg:grid-cols-[248px_1fr]">
        <aside className="border-b border-neutral-200 bg-white p-4 lg:border-b-0 lg:border-r">
          <div className="mb-6">
            <div className="text-base font-semibold">AI Content Studio</div>
            <div className="text-sm text-neutral-500">Local MVP workspace</div>
          </div>
          <nav className="grid grid-cols-2 gap-2 lg:grid-cols-1">
            {nav.map((item) => {
              const Icon = item.icon;
              return (
                <button
                  key={item.id}
                  onClick={() => setView(item.id)}
                  className={`flex items-center gap-2 rounded-md px-3 py-2 text-left text-sm ${
                    view === item.id ? "bg-neutral-900 text-white" : "text-neutral-700 hover:bg-neutral-100"
                  }`}
                >
                  <Icon size={16} />
                  {item.label}
                </button>
              );
            })}
          </nav>
        </aside>
        <section className="p-4 sm:p-6">
          {error ? <div className="mb-4 rounded-md border border-red-200 bg-red-50 p-3 text-sm text-red-700">{error}</div> : null}
          {view === "dashboard" ? (
            <div className="grid gap-4">
              <div>
                <h1 className="text-2xl font-semibold">Dashboard</h1>
                <p className="mt-1 text-sm text-neutral-600">Create profile memory, generate posts, and reuse saved content.</p>
              </div>
              <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
                {stats.map(([label, value]) => (
                  <div key={label} className="rounded-lg border border-neutral-200 bg-white p-4 shadow-sm">
                    <div className="text-sm text-neutral-500">{label}</div>
                    <div className="mt-2 text-3xl font-semibold">{value}</div>
                  </div>
                ))}
              </div>
              <div className="rounded-lg border border-neutral-200 bg-white p-4 shadow-sm">
                <h2 className="font-semibold">Latest posts</h2>
                <div className="mt-3 grid gap-2">
                  {posts.slice(0, 5).map((post) => (
                    <button key={post.id} onClick={() => setView("history")} className="rounded-md border border-neutral-200 p-3 text-left text-sm hover:bg-neutral-50">
                      <span className="font-medium">{post.topic}</span>
                      <span className="ml-2 text-neutral-500">{post.status}</span>
                    </button>
                  ))}
                  {posts.length === 0 ? <p className="text-sm text-neutral-500">No generations yet.</p> : null}
                </div>
              </div>
            </div>
          ) : null}
          {view === "profiles" ? (
            <ResourceManager
              title="Content Profiles"
              description="Memory for audience, positioning, tone, platforms, and constraints."
              items={profiles}
              fields={[
                { key: "name", label: "Name" },
                { key: "profile_type", label: "Profile type" },
                { key: "source_description", label: "Source description", type: "textarea" },
                { key: "audience", label: "Audience", type: "textarea" },
                { key: "tone", label: "Tone" },
                { key: "platforms", label: "Platforms", type: "tags", placeholder: "instagram, x, linkedin" },
              ]}
              onCreate={async (data) => {
                await api.createProfile(data);
                await refresh();
              }}
              onRefresh={refresh}
              renderMeta={(item) => (
                <>
                  <div>{item.profile_type || "Custom profile"}</div>
                  <div>{item.audience || "Audience not set"}</div>
                  <div>{item.platforms.join(", ") || "No platforms"}</div>
                </>
              )}
            />
          ) : null}
          {view === "text" ? (
            <ResourceManager
              title="Text Styles"
              description="Reusable writing rules, examples, length, emoji level, and CTA style."
              items={textStyles}
              fields={[
                { key: "name", label: "Name" },
                { key: "description", label: "Description", type: "textarea" },
                { key: "rules", label: "Rules", type: "textarea" },
                { key: "examples", label: "Examples", type: "tags", placeholder: "Example one, example two" },
              ]}
              onCreate={async (data) => {
                await api.createTextStyle(data);
                await refresh();
              }}
              onRefresh={refresh}
              renderMeta={(item) => (
                <>
                  <div>{item.description || "No description"}</div>
                  <div>{item.rules || "No rules yet"}</div>
                </>
              )}
            />
          ) : null}
          {view === "image" ? (
            <ResourceManager
              title="Image Styles"
              description="Visual memory for generated image prompts."
              items={imageStyles}
              fields={[
                { key: "name", label: "Name" },
                { key: "description", label: "Description", type: "textarea" },
                { key: "colors", label: "Colors", type: "tags", placeholder: "black, white, green" },
                { key: "mood", label: "Mood" },
                { key: "prompt_addon", label: "Prompt addon", type: "textarea" },
              ]}
              onCreate={async (data) => {
                await api.createImageStyle(data);
                await refresh();
              }}
              onRefresh={refresh}
              renderMeta={(item) => (
                <>
                  <div>{item.description || "No description"}</div>
                  <div>{item.colors.join(", ") || "No colors"}</div>
                </>
              )}
            />
          ) : null}
          {view === "generate" ? (
            <GeneratePanel
              profiles={profiles}
              textStyles={textStyles}
              imageStyles={imageStyles}
              onGenerated={(post) => {
                setPosts((current) => [post, ...current.filter((item) => item.id !== post.id)]);
              }}
            />
          ) : null}
          {view === "history" ? (
            <div className="grid gap-3">
              <h1 className="text-2xl font-semibold">History</h1>
              {posts.map((post) => (
                <article key={post.id} className="rounded-lg border border-neutral-200 bg-white p-4 shadow-sm">
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <h2 className="font-semibold">{post.topic}</h2>
                    <span className="rounded-md bg-neutral-100 px-2 py-1 text-xs">{post.status}</span>
                  </div>
                  <pre className="mt-3 max-h-80 overflow-auto rounded-md bg-neutral-950 p-3 text-xs text-neutral-50">{JSON.stringify(post.generated_content, null, 2)}</pre>
                </article>
              ))}
            </div>
          ) : null}
          {view === "settings" ? (
            <div className="rounded-lg border border-neutral-200 bg-white p-4 shadow-sm">
              <h1 className="text-2xl font-semibold">Settings</h1>
              <pre className="mt-4 overflow-auto rounded-md bg-neutral-950 p-4 text-xs text-neutral-50">{JSON.stringify(settings, null, 2)}</pre>
            </div>
          ) : null}
        </section>
      </div>
    </main>
  );
}
