// Core API Client
import { getSession } from "next-auth/react";

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
    const text = await response.text();
    // Handle 401 error
    if (response.status === 404) console.error("Endpoint not found:", endpoint);

    throw new Error(`Error ${response.status}: ${text}`);
  }

  return response.json();
}
