"use client";

import { signIn } from "next-auth/react";

export default function Login() {
  return (
    <div className="h-dvh w-full flex justify-center items-center flex-col space-y-3">
      <h1>Login to your Zimna account</h1>

      <button
        onClick={() => signIn("google", { callbackUrl: "/home" })}
        className="border rounded-lg py-1 px-3 hover:border-black"
      >
        Sign in with Google
      </button>
    </div>
  );
}
