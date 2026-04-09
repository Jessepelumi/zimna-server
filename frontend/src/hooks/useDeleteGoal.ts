import { useQueryClient } from "@tanstack/react-query";
import { useMutation } from "@tanstack/react-query";
import { goalsApi } from "@/lib/api/goals";

export const useDeleteGoal = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: string) => goalsApi.delete(id),
    onSuccess: () => {
      // Refresh the goals list immediately
      queryClient.invalidateQueries({ queryKey: ["goals"] });
    },
    onError: (error: Error) => {
      console.error("Zimna Delete Error:", error.message);
    },
  });
};
