import {
  CaretUpIcon,
  LineVerticalIcon,
  PlusIcon,
  XIcon,
} from "@phosphor-icons/react/dist/ssr";
import { useRouter } from "next/navigation";

interface GoalTileProps {
  id: string;
  title: string;
  count: number;
  isOpen: boolean;
  onToggle: () => void;
  onDelete: (id: string) => void;
  isDeleting?: boolean;
}

export const GoalTile = ({
  id,
  title,
  count,
  isOpen,
  onToggle,
  onDelete,
  isDeleting,
}: GoalTileProps) => {
  const router = useRouter();

  const handleOpenConsole = (e: React.MouseEvent) => {
    e.stopPropagation();
    router.push(`/console/${id}`);
  };

  const handleDelete = (e: React.MouseEvent) => {
    e.stopPropagation(); // Stop accordion from toggling
    if (confirm(`Are you sure you want to delete "${title}"?`)) {
      onDelete(id);
    }
  };

  return (
    <div
      onClick={onToggle}
      className={`flex justify-between items-center gap-2 w-full border border-gray-200 cursor-default ${isOpen ? "bg-blue-50" : ""} hover:bg-blue-50 px-5 py-3 rounded-lg`}
    >
      <div className="flex items-center">
        <div className="pr-3 flex items-center justify-center">
          <span
            className={`flex transition-transform duration-300 ${isOpen ? "rotate-180" : ""}`}
          >
            <CaretUpIcon size={21} />
          </span>
        </div>

        <div className="flex gap-1 items-center">
          <h2 className="font-bold text-sm line-clamp-1 min-w-0 flex-1">
            {title}
          </h2>
          <span className="font-light text-xs bg-blue-200 px-1 rounded text-blue-700">
            {count}
          </span>
        </div>
      </div>

      <div className="flex items-center">
        <button
          onClick={handleDelete}
          disabled={isDeleting}
          className="group  border-black px-1.5 py-1 rounded flex items-center gap-0 transition-all duration-300 hover:gap-2 hover:text-red-600"
        >
          <XIcon weight="bold" size={14} className="shrink-0" />
          <span className="text-sm text-red-600 overflow-hidden whitespace-nowrap max-w-0 transition-all duration-300 group-hover:max-w-32">
            {isDeleting ? "deleting..." : "delete"}
          </span>
        </button>

        <LineVerticalIcon className="text-gray-400" />

        <button
          onClick={handleOpenConsole}
          className="group  border-black px-1.5 py-1 rounded flex items-center gap-0 transition-all duration-300 hover:gap-2 hover:text-blue-700"
        >
          <PlusIcon size={14} className="shrink-0" />
          <span className="text-sm text-blue-700 overflow-hidden whitespace-nowrap max-w-0 transition-all duration-300 group-hover:max-w-32">
            open in console
          </span>
        </button>
      </div>
    </div>
  );
};
