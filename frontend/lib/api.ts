export const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export type ContentProfile = {
  id: number;
  user_id: number;
  name: string;
  profile_type?: string | null;
  source_description?: string | null;
  niche?: string | null;
  description?: string | null;
  offer_or_focus?: string | null;
  audience?: string | null;
  geography?: string | null;
  tone?: string | null;
  goals?: string | null;
  platforms: string[];
  language: string;
  positioning?: string | null;
  content_pillars: string[];
  platform_strategy: Record<string, unknown>;
  favorite_words?: string | null;
  forbidden_words?: string | null;
  avoid_topics?: string | null;
  additional_notes?: string | null;
  created_at: string;
  updated_at: string;
};

export type TextStyle = {
  id: number;
  user_id: number;
  profile_id?: number | null;
  name: string;
  description?: string | null;
  rules?: string | null;
  examples: string[];
  emoji_level: string;
  post_length: string;
  cta_style: string;
  created_at: string;
  updated_at: string;
};

export type ImageStyle = {
  id: number;
  user_id: number;
  profile_id?: number | null;
  name: string;
  description?: string | null;
  colors: string[];
  mood?: string | null;
  composition?: string | null;
  avoid?: string | null;
  prompt_addon?: string | null;
  created_at: string;
  updated_at: string;
};

export type Post = {
  id: number;
  user_id: number;
  profile_id: number | null;
  text_style_id: number | null;
  image_style_id: number | null;
  generation_session_id: number | null;
  topic: string;
  goal?: string | null;
  platforms: string[];
  generation_mode: string;
  input_request?: string | null;
  generated_content: Record<string, unknown>;
  image_prompt: Record<string, unknown>;
  image_url?: string | null;
  analysis: Record<string, unknown>;
  score: Record<string, unknown>;
  status: string;
  tags: string[];
  notes?: string | null;
  model_used?: string | null;
  created_at: string;
  updated_at: string;
};

export type Settings = {
  id: number;
  provider: string;
  text_model: string;
  fast_model: string;
  quality_model: string;
  image_model: string;
  daily_generation_limit: number;
  default_language: string;
};

export type GenerationSession = {
  id: number;
  user_id: number;
  profile_id: number | null;
  mode: string;
  topic: string;
  platforms: string[];
  current_step: string;
  topic_analysis: Record<string, unknown>;
  expanded_angles: Record<string, unknown>[];
  hooks: Record<string, unknown>[];
  selected_hook?: string | null;
  drafts: Record<string, unknown>[];
  revision_requests: string[];
  final_content: Record<string, unknown>;
  image_prompts: Record<string, unknown>[];
  platform_analysis: Record<string, unknown>;
  created_at: string;
  updated_at: string;
};

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers || {}),
    },
    cache: "no-store",
  });
  if (!response.ok) {
    const body = await response.text();
    throw new Error(body || `Request failed: ${response.status}`);
  }
  if (response.status === 204) {
    return undefined as T;
  }
  return (await response.json()) as T;
}

export const api = {
  listProfiles: () => request<ContentProfile[]>("/api/content-profiles"),
  createProfile: (data: Partial<ContentProfile>) => request<ContentProfile>("/api/content-profiles", { method: "POST", body: JSON.stringify(data) }),
  updateProfile: (id: number, data: Partial<ContentProfile>) => request<ContentProfile>(`/api/content-profiles/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  deleteProfile: (id: number) => request<void>(`/api/content-profiles/${id}`, { method: "DELETE" }),
  listTextStyles: () => request<TextStyle[]>("/api/text-styles"),
  createTextStyle: (data: Partial<TextStyle>) => request<TextStyle>("/api/text-styles", { method: "POST", body: JSON.stringify(data) }),
  updateTextStyle: (id: number, data: Partial<TextStyle>) => request<TextStyle>(`/api/text-styles/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  deleteTextStyle: (id: number) => request<void>(`/api/text-styles/${id}`, { method: "DELETE" }),
  listImageStyles: () => request<ImageStyle[]>("/api/image-styles"),
  createImageStyle: (data: Partial<ImageStyle>) => request<ImageStyle>("/api/image-styles", { method: "POST", body: JSON.stringify(data) }),
  updateImageStyle: (id: number, data: Partial<ImageStyle>) => request<ImageStyle>(`/api/image-styles/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  deleteImageStyle: (id: number) => request<void>(`/api/image-styles/${id}`, { method: "DELETE" }),
  listPosts: () => request<Post[]>("/api/posts"),
  updatePost: (id: number, data: Partial<Post>) => request<Post>(`/api/posts/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  deletePost: (id: number) => request<void>(`/api/posts/${id}`, { method: "DELETE" }),
  generatePost: (data: Record<string, unknown>) => request<Post>("/api/posts/generate", { method: "POST", body: JSON.stringify(data) }),
  listGenerationSessions: () => request<GenerationSession[]>("/api/generation-sessions"),
  createGenerationSession: (data: Partial<GenerationSession>) => request<GenerationSession>("/api/generation-sessions", { method: "POST", body: JSON.stringify(data) }),
  deleteGenerationSession: (id: number) => request<void>(`/api/generation-sessions/${id}`, { method: "DELETE" }),
  getSettings: () => request<Settings>("/api/settings"),
  updateSettings: (data: Partial<Settings>) => request<Settings>("/api/settings", { method: "PUT", body: JSON.stringify(data) }),
};
