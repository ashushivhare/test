import { Link } from 'react-router-dom';
import { Study } from '../types';

interface StudyCardProps {
  study: Study;
}

export default function StudyCard({ study }: StudyCardProps) {
  return (
    <div className="card hover:shadow-lg transition-shadow duration-300">
      <Link to={`/study/${study.id}`}>
        <img 
          src={study.imageUrl} 
          alt={study.title} 
          className="w-full h-48 object-cover"
        />
        <div className="p-4">
          <div className="flex justify-between items-start">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">{study.title}</h3>
            <span className={`px-2 py-1 text-xs rounded-full ${
              study.status === 'active' ? 'bg-green-100 text-green-800' : 
              study.status === 'completed' ? 'bg-blue-100 text-blue-800' : 
              'bg-gray-100 text-gray-800'
            }`}>
              {study.status.charAt(0).toUpperCase() + study.status.slice(1)}
            </span>
          </div>
          <p className="mt-2 text-sm text-gray-600 dark:text-gray-300 line-clamp-2">{study.description}</p>
          <div className="mt-3 flex flex-wrap gap-1">
            {study.tags.map((tag, index) => (
              <span key={index} className="bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-300 text-xs px-2 py-1 rounded">
                {tag}
              </span>
            ))}
          </div>
          <div className="mt-4 flex justify-between items-center text-sm text-gray-500 dark:text-gray-400">
            <span>{study.participants} participants</span>
            <span>{study.duration}</span>
          </div>
        </div>
      </Link>
    </div>
  );
}