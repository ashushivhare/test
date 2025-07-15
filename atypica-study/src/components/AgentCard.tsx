import { Link } from 'react-router-dom';
import { Agent } from '../types';

interface AgentCardProps {
  agent: Agent;
}

export default function AgentCard({ agent }: AgentCardProps) {
  return (
    <div className="card hover:shadow-lg transition-shadow duration-300">
      <Link to={`/agent/${agent.id}`}>
        <img 
          src={agent.imageUrl} 
          alt={agent.name} 
          className="w-full h-48 object-cover"
        />
        <div className="p-4">
          <div className="flex justify-between items-start">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">{agent.name}</h3>
            <span className={`px-2 py-1 text-xs rounded-full ${
              agent.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
            }`}>
              {agent.status.charAt(0).toUpperCase() + agent.status.slice(1)}
            </span>
          </div>
          <p className="mt-2 text-sm text-gray-600 dark:text-gray-300">{agent.description}</p>
          <div className="mt-3">
            <h4 className="text-xs font-medium text-gray-500 dark:text-gray-400">Capabilities:</h4>
            <ul className="mt-1 space-y-1">
              {agent.capabilities.map((capability, index) => (
                <li key={index} className="text-xs text-gray-600 dark:text-gray-300 flex items-center">
                  <span className="mr-1">•</span> {capability}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </Link>
    </div>
  );
}