// Core API Client
import { getSession, signOut } from "next-auth/react";

const BASE_URL = "/api";

type FetchOptions = RequestInit & {
  auth?: boolean;
};

export async function apiClient<T>(
  endpoint: string,
  options: FetchOptions = {},
): Promise<T> {
  const { auth = true, ...rest } = options;

  const headers = new Headers({
    "Content-Type": "application/json",
    ...(rest.headers as Record<string, string>),
  });

  // Automatically attach the Django JWT if auth is required
  if (auth) {
    const session = await getSession();
    if (session?.accessToken) {
      headers.set("Authorization", `Bearer ${session.accessToken}`);
    }
  }

  const response = await fetch(`${BASE_URL}${endpoint}`, {
    ...rest,
    headers,
  });

  if (!response.ok) {
    // Handle 401 Unauthorized (JWT Expired)
    if (response.status === 401) {
      console.warn("Session expired. Signing out...");
      await signOut({ callbackUrl: "/login" });
      throw new Error("Session expired. Please log in again.");
    }

    if (response.status === 404) {
      console.error("Endpoint not found:", endpoint);
    }

    const text = await response.text();
    throw new Error(`Error ${response.status}: ${text}`);
  }

  return response.json();
}
