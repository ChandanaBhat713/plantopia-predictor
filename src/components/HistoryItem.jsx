
import React from 'react';
import { cn } from "@/lib/utils";
import { ArrowRight, Calendar, Clock } from 'lucide-react';
import { format } from 'date-fns';
import { Link } from 'react-router-dom';

const HistoryItem = ({ scan, onClick, className }) => {
  const formattedDate = format(new Date(scan.timestamp), 'MMM dd, yyyy');
  const formattedTime = format(new Date(scan.timestamp), 'hh:mm a');
  
  return (
    <div 
      className={cn(
        "glass-card p-4 rounded-xl cursor-pointer transition-all hover:shadow-md",
        className
      )}
      onClick={onClick}
    >
      <div className="flex items-center space-x-4">
        <div className="w-16 h-16 rounded-md overflow-hidden bg-secondary flex-shrink-0">
          <img 
            src={scan.imageUrl} 
            alt={scan.disease} 
            className="w-full h-full object-cover"
          />
        </div>
        
        <div className="flex-grow">
          <h3 className="font-medium text-base line-clamp-1">{scan.disease}</h3>
          <div className="flex items-center space-x-3 mt-1">
            <div className="flex items-center text-xs text-muted-foreground">
              <Calendar className="w-3 h-3 mr-1" />
              {formattedDate}
            </div>
            <div className="flex items-center text-xs text-muted-foreground">
              <Clock className="w-3 h-3 mr-1" />
              {formattedTime}
            </div>
          </div>
        </div>
        
        <Link 
          to={`/history/${scan.id}`}
          className="p-2 hover:bg-secondary rounded-full transition-colors"
          onClick={(e) => e.stopPropagation()}
        >
          <ArrowRight className="w-4 h-4" />
        </Link>
      </div>
    </div>
  );
};

export default HistoryItem;
