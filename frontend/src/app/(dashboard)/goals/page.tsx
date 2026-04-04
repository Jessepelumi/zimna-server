"use client";

import { useGoals } from "@/hooks/useGoals";
import { GoalAccordion } from "@/components/custom/goalAccordion";

export default function Goals() {
  const { data: goals, isLoading, isError } = useGoals();

  if (isLoading) {
    return (
      <div className="p-8 flex justify-center">
        <span className="animate-pulse text-slate-500">
          Loading your goals...
        </span>
      </div>
    );
  }

  if (isError) {
    return (
      <div className="p-8 text-red-500 text-center">
        Failed to load goals. Please check your connection.
      </div>
    );
  }

  return (
    <div className="w-full space-y-5">
      <div>
        <h1 className="text-2xl">Dashboard</h1>
        <p className="text-gray-400 text-sm w-2/3 lg:w-full">
          These are your goals. Toggle the tile to view the associated tasks.
        </p>
      </div>

      {goals?.map((goal) => (
        <GoalAccordion key={goal.id} title={goal.title} tasks={goal.tasks} />
      ))}

      {goals?.length === 0 && (
        <div className="text-center py-20 border-2 border-dashed rounded-xl">
          <p className="text-slate-400">
            No goals found. Start by creating one!
          </p>
        </div>
      )}
    </div>
  );
}
