import { withAuth } from "next-auth/middleware";

export default withAuth({
  pages: {
    signIn: "/login",
  },
});

// List every route that requires a login
export const config = {
  matcher: [
    "/home/:path*", 
    "/goals/:path*", 
    "/objectives/:path*"
  ],
};