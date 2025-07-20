// types/api.ts
export interface AuthResponse {
  access_token: string;
  refresh_token: string;
}

export interface UserInfo {
  id: number;
  nickname?: string;
  username?: string;
  name?: string;
  email?: string;
  avatar?: string;
  created_at?: string;
}
