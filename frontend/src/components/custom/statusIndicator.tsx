interface StatusIndicatorProps {
  isCompleted: boolean;
}

export const StatusIndicator = ({ isCompleted }: StatusIndicatorProps) => {
  const styles = isCompleted
    ? "text-green-600 bg-green-100 border-green-600"
    : "text-yellow-600 bg-yellow-100 border-yellow-600";

  const label = isCompleted ? "Completed" : "Ongoing";

  return (
    <div className={`w-fit text-xs text-center border px-1.5 py-1 rounded-full ${styles}`}>
      {label}
    </div>
  );
};
