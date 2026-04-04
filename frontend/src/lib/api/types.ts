export interface Task {
  id: string;
  title: string;
  description: string;
  is_completed: boolean;
}

export interface Goal {
  id: string;
  title: string;
  description: string;
  due_date: string | null;
  tasks: Task[];
}
