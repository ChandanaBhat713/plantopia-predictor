
import React, { useState } from 'react';
import { cn } from "@/lib/utils";
import { AlertCircle, ArrowRight, Check, Copy, ExternalLink } from 'lucide-react';
import { toast } from "@/hooks/use-toast";

const ResultCard = ({ result, className }) => {
  const [copied, setCopied] = useState(false);
  
  if (!result) return null;
  
  const { disease, confidence, description, treatment, sources } = result;
  
  const handleCopy = () => {
    const textToCopy = `
Disease: ${disease}
Confidence: ${(confidence * 100).toFixed(1)}%
Description: ${description}
Treatment: ${treatment}
    `.trim();
    
    navigator.clipboard.writeText(textToCopy).then(() => {
      setCopied(true);
      toast({
        title: "Copied to clipboard",
        description: "The diagnosis results have been copied",
      });
      setTimeout(() => setCopied(false), 2000);
    });
  };

  return (
    <div 
      className={cn(
        "glass-card p-6 rounded-2xl space-y-4 shadow-sm animate-fade-in",
        className
      )}
    >
      <div className="flex items-start justify-between">
        <div>
          <div className="inline-flex items-center rounded-full bg-accent px-2.5 py-0.5 text-xs font-semibold text-accent-foreground mb-2">
            Diagnosis Result
          </div>
          <h3 className="text-xl font-semibold">{disease}</h3>
          <div className="flex items-center mt-1">
            <div className="w-full max-w-[140px] h-2 bg-secondary rounded-full overflow-hidden">
              <div 
                className="h-full bg-primary rounded-full"
                style={{ width: `${confidence * 100}%` }}
              />
            </div>
            <span className="ml-2 text-sm font-medium">{(confidence * 100).toFixed(1)}% confidence</span>
          </div>
        </div>
        
        <button 
          onClick={handleCopy}
          className="p-2 rounded-full hover:bg-secondary transition-colors"
          aria-label="Copy results"
        >
          {copied ? <Check className="w-5 h-5 text-green-500" /> : <Copy className="w-5 h-5" />}
        </button>
      </div>
      
      <div className="space-y-3">
        <div>
          <h4 className="text-sm font-medium mb-1">Description</h4>
          <p className="text-sm text-muted-foreground">{description}</p>
        </div>
        
        <div>
          <h4 className="text-sm font-medium mb-1">Treatment</h4>
          <p className="text-sm text-muted-foreground">{treatment}</p>
        </div>
        
        {sources && sources.length > 0 && (
          <div>
            <h4 className="text-sm font-medium mb-1">Learn More</h4>
            <div className="space-y-1">
              {sources.map((source, index) => (
                <a
                  key={index}
                  href={source.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center text-xs text-primary hover:underline"
                >
                  <ExternalLink className="w-3 h-3 mr-1" />
                  {source.title || source.url}
                </a>
              ))}
            </div>
          </div>
        )}
      </div>
      
      <div className="pt-2 border-t border-border">
        <div className="flex items-center justify-between">
          <div className="flex items-center text-xs text-muted-foreground">
            <AlertCircle className="w-3 h-3 mr-1" />
            <span>Consult with a professional for severe cases</span>
          </div>
          <a 
            href="#treatment"
            className="flex items-center text-xs font-medium text-primary hover:underline"
          >
            Full treatment guide <ArrowRight className="w-3 h-3 ml-1" />
          </a>
        </div>
      </div>
    </div>
  );
};

export default ResultCard;
