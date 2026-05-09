export const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export type ContentProfile = {
  id: number;
  name: string;
  profile_type?: string | null;
  source_description?: string | null;
  niche?: string | null;
  description?: string | null;
  audience?: string | null;
  tone?: string | null;
  platforms: string[];
  language: string;
};

export type TextStyle = {
  id: number;
  profile_id?: number | null;
  name: string;
  description?: string | null;
  rules?: string | null;
  examples: string[];
  emoji_level: string;
  post_length: string;
  cta_style: string;
};

export type ImageStyle = {
  id: number;
  profile_id?: number | null;
  name: string;
  description?: string | null;
  colors: string[];
  mood?: string | null;
  composition?: string | null;
  avoid?: string | null;
  prompt_addon?: string | null;
};

export type Post = {
  id: number;
  profile_id: number | null;
  topic: string;
  goal?: string | null;
  platforms: string[];
  generated_content: Record<string, unknown>;
  image_prompt: Record<string, unknown>;
  analysis: Record<string, unknown>;
  status: string;
  tags: string[];
  notes?: string | null;
  model_used?: string | null;
  created_at: string;
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
  listTextStyles: () => request<TextStyle[]>("/api/text-styles"),
  createTextStyle: (data: Partial<TextStyle>) => request<TextStyle>("/api/text-styles", { method: "POST", body: JSON.stringify(data) }),
  listImageStyles: () => request<ImageStyle[]>("/api/image-styles"),
  createImageStyle: (data: Partial<ImageStyle>) => request<ImageStyle>("/api/image-styles", { method: "POST", body: JSON.stringify(data) }),
  listPosts: () => request<Post[]>("/api/posts"),
  updatePost: (id: number, data: Partial<Post>) => request<Post>(`/api/posts/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  generatePost: (data: Record<string, unknown>) => request<Post>("/api/posts/generate", { method: "POST", body: JSON.stringify(data) }),
  getSettings: () => request<Settings>("/api/settings"),
  updateSettings: (data: Partial<Settings>) => request<Settings>("/api/settings", { method: "PUT", body: JSON.stringify(data) }),
};
