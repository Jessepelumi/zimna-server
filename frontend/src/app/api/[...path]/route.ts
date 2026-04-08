import { NextRequest, NextResponse } from "next/server";

const BACKEND_URL = process.env.BASE_URL;

async function proxyHandler(
  req: NextRequest,
  { params }: { params: Promise<{ path: string[] }> },
) {
  const resolvedParams = await params;
  const pathSegments = resolvedParams.path;

  // Prevent proxying NextAuth routes
  if (pathSegments[0] === "auth") {
    return new NextResponse(null, { status: 404 });
  }

  // Construct the backend URL
  // Ensure we add a trailing slash for Django compatibility
  const relativePath = pathSegments.filter(Boolean).join("/");
  const url = `${BACKEND_URL}/${relativePath}/`;

  // Prepare headers (Forward the JWT)
  const authHeader = req.headers.get("authorization");
  const headers = new Headers({
    "Content-Type": "application/json",
  });
  if (authHeader) headers.set("Authorization", authHeader);

  // Extract body for non-GET requests
  let body = undefined;
  if (req.method !== "GET" && req.method !== "HEAD") {
    try {
      body = await req.text();
    } catch (e) {
      console.error("Failed to parse request body:", e);
    }
  }

  try {
    const response = await fetch(url, {
      method: req.method,
      headers,
      body,
      // For Next.js caching control
      cache: "no-store",
    });

    const data = await response.text();

    return new NextResponse(data, {
      status: response.status,
      headers: {
        "Content-Type": "application/json",
      },
    });
  } catch (error) {
    console.error("Proxy Error:", error);
    return NextResponse.json(
      { error: "Failed to connect to backend service" },
      { status: 502 },
    );
  }
}

// Exporting all necessary methods using the same handler
export const GET = proxyHandler;
export const POST = proxyHandler;
export const PUT = proxyHandler;
export const PATCH = proxyHandler;
export const DELETE = proxyHandler;
