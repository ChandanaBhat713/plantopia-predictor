
import React from 'react';
import { cn } from "@/lib/utils";

const Loading = ({ text = "Processing", className }) => {
  return (
    <div className={cn("flex flex-col items-center justify-center py-12", className)}>
      <div className="relative w-16 h-16">
        <div className="absolute inset-0 rounded-full border-4 border-t-primary border-r-transparent border-b-transparent border-l-transparent animate-rotate"></div>
        <div className="absolute inset-2 rounded-full border-4 border-t-transparent border-r-primary border-b-transparent border-l-transparent animate-rotate" style={{ animationDuration: '1.2s' }}></div>
        <div className="absolute inset-4 rounded-full border-4 border-t-transparent border-r-transparent border-b-primary border-l-transparent animate-rotate" style={{ animationDuration: '1.4s' }}></div>
      </div>
      <p className="mt-4 text-muted-foreground text-sm font-medium">{text}</p>
    </div>
  );
};

export default Loading;
