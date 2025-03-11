
import React from 'react';
import { cn } from "@/lib/utils";
import { Sun, Droplets, Thermometer, Wind } from 'lucide-react';

const PlantInfo = ({ plantData, className }) => {
  if (!plantData) return null;
  
  const { name, scientificName, care, preventionTips } = plantData;
  
  const careIcons = {
    water: <Droplets className="w-4 h-4" />,
    sunlight: <Sun className="w-4 h-4" />,
    temperature: <Thermometer className="w-4 h-4" />,
    airflow: <Wind className="w-4 h-4" />
  };

  return (
    <div className={cn("glass-card p-6 rounded-2xl shadow-sm animate-fade-in", className)}>
      <div className="flex flex-col space-y-4">
        <div>
          <div className="inline-flex items-center rounded-full bg-accent px-2.5 py-0.5 text-xs font-semibold text-accent-foreground mb-2">
            Plant Information
          </div>
          <h3 className="text-xl font-semibold">{name}</h3>
          <p className="text-sm italic text-muted-foreground">{scientificName}</p>
        </div>
        
        <div className="grid grid-cols-2 gap-3">
          {Object.entries(care).map(([key, value]) => (
            <div key={key} className="flex items-start">
              <div className="mt-1 mr-2 p-1.5 bg-accent rounded-md">
                {careIcons[key] || null}
              </div>
              <div>
                <h4 className="text-sm font-medium capitalize">{key}</h4>
                <p className="text-xs text-muted-foreground">{value}</p>
              </div>
            </div>
          ))}
        </div>
        
        <div>
          <h4 className="text-sm font-medium mb-2">Prevention Tips</h4>
          <ul className="space-y-2">
            {preventionTips.map((tip, index) => (
              <li key={index} className="flex items-start">
                <span className="inline-flex items-center justify-center rounded-full bg-primary text-white w-5 h-5 text-xs mr-2 mt-0.5">
                  {index + 1}
                </span>
                <p className="text-sm text-muted-foreground">{tip}</p>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default PlantInfo;
