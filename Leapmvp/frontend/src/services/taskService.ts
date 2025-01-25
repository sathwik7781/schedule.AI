import { useState, useCallback } from 'react';

interface Task {
  id: string;
  title: string;
  due_date: string;
  priority: number;
  category: string;
}

export const useTaskService = () => {
  const [error, setError] = useState<string | null>(null);

  const createTask = async (description: string): Promise<Task> => {
    try {
      const response = await fetch('/api/tasks', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ description }),
      });

      if (!response.ok) {
        throw new Error('Failed to create task');
      }

      return await response.json();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create task');
      throw err;
    }
  };

  return { createTask, error };
}; 