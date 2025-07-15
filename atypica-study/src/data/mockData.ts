import { Study, Agent, Conversation } from '../types';

export const mockStudies: Study[] = [
  {
    id: 'mueXDjdMknAzkhMp',
    title: 'Agentic AI Study',
    description: 'Explore how AI agents can assist with complex tasks and decision-making processes.',
    imageUrl: 'https://images.pexels.com/photos/2599244/pexels-photo-2599244.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
    tags: ['AI', 'Agents', 'Decision-making'],
    createdAt: '2023-10-15T12:00:00Z',
    updatedAt: '2023-10-20T15:30:00Z',
    status: 'active',
    participants: 120,
    duration: '30 minutes'
  },
  {
    id: 'kLm7PqRs9TuVwXyZ',
    title: 'Natural Language Understanding',
    description: 'Test the capabilities of AI in understanding complex human language patterns and nuances.',
    imageUrl: 'https://images.pexels.com/photos/3861969/pexels-photo-3861969.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
    tags: ['NLP', 'Language', 'Understanding'],
    createdAt: '2023-09-05T10:15:00Z',
    updatedAt: '2023-09-18T14:20:00Z',
    status: 'active',
    participants: 85,
    duration: '25 minutes'
  },
  {
    id: 'aBcDeFgHiJkLmNoP',
    title: 'Creative Writing Assistant',
    description: 'Evaluate how AI can assist in creative writing tasks and storytelling.',
    imageUrl: 'https://images.pexels.com/photos/3059748/pexels-photo-3059748.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
    tags: ['Writing', 'Creativity', 'Storytelling'],
    createdAt: '2023-08-20T09:30:00Z',
    updatedAt: '2023-08-25T11:45:00Z',
    status: 'completed',
    participants: 210,
    duration: '40 minutes'
  },
  {
    id: 'qWeRtYuIoPaSdFgH',
    title: 'Code Generation and Debugging',
    description: 'Test AI capabilities in generating code and helping debug programming issues.',
    imageUrl: 'https://images.pexels.com/photos/546819/pexels-photo-546819.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
    tags: ['Coding', 'Programming', 'Debugging'],
    createdAt: '2023-11-01T08:45:00Z',
    updatedAt: '2023-11-10T16:20:00Z',
    status: 'active',
    participants: 150,
    duration: '35 minutes'
  },
  {
    id: 'zXcVbNmAsQwErTy',
    title: 'Visual Content Analysis',
    description: 'Explore how AI interprets and analyzes visual content and imagery.',
    imageUrl: 'https://images.pexels.com/photos/1779487/pexels-photo-1779487.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
    tags: ['Visual', 'Analysis', 'Imagery'],
    createdAt: '2023-07-12T11:20:00Z',
    updatedAt: '2023-07-20T13:10:00Z',
    status: 'draft',
    participants: 0,
    duration: '45 minutes'
  }
];

export const mockAgents: Agent[] = [
  {
    id: 'agent001',
    name: 'Research Assistant',
    description: 'Helps with research tasks, finding information, and summarizing content.',
    imageUrl: 'https://images.pexels.com/photos/7567434/pexels-photo-7567434.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
    capabilities: ['Information retrieval', 'Summarization', 'Citation generation'],
    status: 'active'
  },
  {
    id: 'agent002',
    name: 'Creative Companion',
    description: 'Assists with creative writing, brainstorming ideas, and storytelling.',
    imageUrl: 'https://images.pexels.com/photos/8386440/pexels-photo-8386440.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
    capabilities: ['Story development', 'Character creation', 'Plot suggestions'],
    status: 'active'
  },
  {
    id: 'agent003',
    name: 'Code Wizard',
    description: 'Helps with programming tasks, debugging, and code optimization.',
    imageUrl: 'https://images.pexels.com/photos/4164418/pexels-photo-4164418.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
    capabilities: ['Code generation', 'Debugging', 'Optimization suggestions'],
    status: 'active'
  }
];

export const mockConversations: Conversation[] = [
  {
    id: 'conv001',
    studyId: 'mueXDjdMknAzkhMp',
    agentId: 'agent001',
    messages: [
      {
        id: 'msg001',
        role: 'system',
        content: 'You are a helpful research assistant participating in a study about agentic AI.',
        timestamp: '2023-10-21T10:00:00Z'
      },
      {
        id: 'msg002',
        role: 'user',
        content: 'Can you help me find information about climate change impacts?',
        timestamp: '2023-10-21T10:01:00Z'
      },
      {
        id: 'msg003',
        role: 'agent',
        content: 'I\'d be happy to help you research climate change impacts. What specific aspects are you interested in? For example, are you looking for information on environmental impacts, economic consequences, health effects, or regional variations?',
        timestamp: '2023-10-21T10:01:30Z'
      }
    ],
    createdAt: '2023-10-21T10:00:00Z',
    updatedAt: '2023-10-21T10:01:30Z'
  }
];