"use client";

import { IconProps } from "@phosphor-icons/react";
import { SignOutIcon } from "@phosphor-icons/react/dist/ssr";
import Link from "next/link";
import { usePathname } from "next/navigation";
import React from "react";

import { signOut } from "next-auth/react";

interface SidebarItemProps {
  icon: React.ElementType<IconProps>;
  text: string;
  href: string;
  isCollapsed?: boolean;
}

export const SidebarItem = ({
  icon: Icon,
  text,
  href,
  isCollapsed,
}: SidebarItemProps) => {
  const pathname = usePathname();
  const isActive = pathname == href;

  return (
    <Link href={href}>
      <div
        className={`flex items-center rounded-md px-2 py-1.5 ${isCollapsed ? "gap-0" : "gap-2"} ${isActive ? "bg-blue-100 " : "hover:bg-blue-50"}`}
      >
        <Icon
          size={20}
          className={`${isActive ? "text-blue-700" : "text-gray-500"}`}
        />
        {!isCollapsed && (
          <p
            className={`text-sm ${isActive ? "text-blue-700" : "text-gray-500"}`}
          >
            {text}
          </p>
        )}
      </div>
    </Link>
  );
};

export const SidebarItemVariant = ({
  icon: Icon,
  text,
  href,
  isCollapsed,
}: SidebarItemProps) => {
  const pathname = usePathname();
  const isActive = pathname == href;

  return (
    <Link href={href}>
      <div
        className={`flex items-center px-2 py-1.5 ${isCollapsed ? "gap-0" : "gap-2"} ${isActive ? "text-blue-700 " : "text-gray-500 group-hover:text-blue-700 group"}`}
      >
        <Icon
          size={20}
          className={`${isActive ? "text-blue-700" : "text-gray-500 group-hover:text-blue-700"}`}
        />
        {!isCollapsed && (
          <p
            className={`text-sm ${isActive ? "text-blue-700" : "text-gray-500 group-hover:text-blue-700"}`}
          >
            {text}
          </p>
        )}
      </div>
    </Link>
  );
};

interface LogOutProps {
  isCollapsed?: boolean,
}

export const LogOut = ({ isCollapsed }: LogOutProps) => {
  const handleLogout = async () => {
    // This clears the NextAuth cookie and the Django session/JWT
    // from the browser's memory.
    await signOut({
      callbackUrl: "/",
      redirect: true,
    });
  };

  return (
    <button onClick={handleLogout} className="p-0">
      <div
        className={`flex items-center ${isCollapsed ? "gap-0" : "gap-2"} rounded-md px-2 py-1.5 text-sm text-red-600 bg-red-100 hover:text-red-700 hover:bg-red-200`}
      >
        <SignOutIcon size={20} />
        {isCollapsed ? "" : "Log out"}
      </div>
    </button>
  );
};
