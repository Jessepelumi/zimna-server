const BACKEND_URL = process.env.BASE_URL!;

async function handler(req: Request, path: string[]) {
  // Don't proxy URL meant for NextAuth
  if (path[0] === "auth") {
    return new Response(null, { status: 404 }); 
  }

  const url = `${BACKEND_URL}/${path.filter(Boolean).join("/")}/`;

  // Capture the Authorization header sent by our apiClient
  const authHeader = req.headers.get("authorization");

  const response = await fetch(url, {
    method: req.method,
    headers: {
      "Content-Type": "application/json",
      // Pass the Bearer token through to the backend
      ...(authHeader ? { "Authorization": authHeader } : {}),
    },
    body: req.method !== "GET" ? await req.text() : undefined,
  });

  return new Response(await response.text(), {
    status: response.status,
    headers: {
      "Content-Type": "application/json",
    },
  });
}

export async function GET(
  req: Request,
  { params }: { params: Promise<{ path: string[] }> },
) {
  const resolvedParams = await params;
  return handler(req, resolvedParams.path);
}

export async function POST(
  req: Request,
  { params }: { params: Promise<{ path: string[] }> },
) {
  const resolvedParams = await params;
  return handler(req, resolvedParams.path);
}
