export interface Study {
  id: string;
  title: string;
  description: string;
  imageUrl: string;
  tags: string[];
  createdAt: string;
  updatedAt: string;
  status: 'active' | 'completed' | 'draft';
  participants: number;
  duration: string;
}

export interface Agent {
  id: string;
  name: string;
  description: string;
  imageUrl: string;
  capabilities: string[];
  status: 'active' | 'inactive';
}

export interface Conversation {
  id: string;
  studyId: string;
  agentId: string;
  messages: Message[];
  createdAt: string;
  updatedAt: string;
}

export interface Message {
  id: string;
  role: 'user' | 'agent' | 'system';
  content: string;
  timestamp: string;
}