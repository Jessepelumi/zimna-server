import {
  CaretUpIcon,
  DotOutlineIcon,
  PlusIcon,
  TrashSimpleIcon,
} from "@phosphor-icons/react/dist/ssr";

interface GoalTileProps {
  title: string;
  count: number;
  isOpen: boolean;
  onToggle: () => void;
}

export const GoalTile = ({ title, count, isOpen, onToggle }: GoalTileProps) => {
  return (
    <div
      onClick={onToggle}
      className={`flex justify-between items-center gap-2 w-full border border-gray-200 ${isOpen ? "bg-blue-50" : ""} hover:bg-blue-50 px-5 py-3 rounded-lg`}
    >
      <div className="flex items-center">
        <div className="pr-3 flex items-center justify-center">
          <span
            className={`flex transition-transform duration-300 ${isOpen ? "rotate-180" : ""}`}
          >
            <CaretUpIcon size={21} />
          </span>
        </div>

        <div>
          <h2 className="font-bold text-sm">
            {title}{" "}
            <span className="font-light bg-blue-200 px-1 rounded text-blue-700">
              {count}
            </span>
          </h2>
        </div>
      </div>

      <div className="flex items-center">
        <button
          onClick={(e) => e.stopPropagation()}
          className="group  border-black px-1.5 py-1 rounded flex items-center gap-0 transition-all duration-300 hover:gap-2 hover:text-red-600"
        >
          <TrashSimpleIcon size={14} className="shrink-0" />
          <span className="text-sm text-red-600 overflow-hidden whitespace-nowrap max-w-0 transition-all duration-300 group-hover:max-w-32">
            delete
          </span>
        </button>

        <DotOutlineIcon weight="fill" />

        <button
          onClick={(e) => e.stopPropagation()}
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
