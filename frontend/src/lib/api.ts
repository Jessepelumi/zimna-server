const BASE_URL = process.env.BASE_URL || "http://localhost:8000/api";

export const zimnaApi = {
  // Central fetcher to handle errors and headers in one place
  async fetcher<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const response = await fetch(`${BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        Authorization: `Basic ${process.env.NEXT_PUBLIC_ZIMNA_AUTH}`,
        ...options.headers,
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || "API Request Failed");
    }

    return response.json();
  },

  // Method for goal decomposition
  decomposeGoal: (text: string) =>
    zimnaApi.fetcher("/decompose/", {
      method: "POST",
      body: JSON.stringify({ text }),
    }),
};
