import React, { useState } from 'react';
import { useTaskService } from '../services/taskService';

interface Task {
  id: string;
  title: string;
  due_date: string;
  priority: number;
  category: string;
}

interface TaskInputProps {
  onTaskCreated: (task: Task) => void;
  onError: (error: string) => void;
}

export const TaskInput: React.FC<TaskInputProps> = ({ onTaskCreated, onError }) => {
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const taskService = useTaskService();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!input.trim()) {
      onError('Please enter a task description');
      return;
    }

    setIsLoading(true);
    
    try {
      const task = await taskService.createTask(input);
      onTaskCreated(task);
      setInput('');
    } catch (error) {
      onError(error instanceof Error ? error.message : 'Failed to create task');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="task-input-container">
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Enter your task in natural language..."
        className="task-input"
        disabled={isLoading}
      />
      <button 
        type="submit" 
        className="submit-button"
        disabled={isLoading || !input.trim()}
      >
        {isLoading ? 'Adding...' : 'Add Task'}
      </button>
    </form>
  );
}; 