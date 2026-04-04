"use client";

import { IconProps } from "@phosphor-icons/react";

interface TableRowTitleProps {
  icon: React.ElementType<IconProps>;
  title: string;
}

export const TableRowTitle = ({ icon: Icon, title }: TableRowTitleProps) => {
  return (
    <div className="flex items-center gap-1 text-gray-400">
      <span>
        <Icon weight="bold" />
      </span>
      {title}
    </div>
  );
};
