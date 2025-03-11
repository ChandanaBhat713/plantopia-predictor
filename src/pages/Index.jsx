
import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import ImageUploader from '../components/ImageUploader';
import ResultCard from '../components/ResultCard';
import PlantInfo from '../components/PlantInfo';
import Loading from '../components/Loading';
import apiService from '../services/api';
import { toast } from "@/hooks/use-toast";
import { AlertCircle, Leaf, Loader2 } from 'lucide-react';

const Index = () => {
  const [image, setImage] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState(null);
  const [plantInfo, setPlantInfo] = useState(null);
  
  // Mock data for development - remove in production
  const mockResult = {
    disease: "Tomato Late Blight",
    confidence: 0.95,
    description: "Late blight is a devastating disease that affects tomato plants, characterized by dark lesions on leaves and stems that spread rapidly under cool, wet conditions.",
    treatment: "Remove and destroy all infected plant parts. Apply copper-based fungicides as a preventive measure. Ensure good air circulation and avoid overhead watering.",
    sources: [
      { title: "Cornell University Plant Disease", url: "https://www.cornell.edu/plant-disease" },
      { title: "Plant MD Database", url: "https://www.example.com/plant-md" }
    ]
  };
  
  const mockPlantInfo = {
    name: "Tomato Plant",
    scientificName: "Solanum lycopersicum",
    care: {
      water: "Keep soil consistently moist but not soggy",
      sunlight: "Full sun (6-8 hours daily)",
      temperature: "65-85°F (18-29°C)",
      airflow: "Good circulation to prevent fungal issues"
    },
    preventionTips: [
      "Plant resistant varieties when possible",
      "Provide adequate spacing between plants for airflow",
      "Use drip irrigation or soaker hoses to keep foliage dry",
      "Apply preventative fungicide during wet conditions"
    ]
  };
  
  const handleImageUpload = (file) => {
    setImage(file);
    // Reset results when new image is uploaded
    if (file) {
      setResult(null);
      setPlantInfo(null);
    }
  };
  
  const analyzePlant = async () => {
    if (!image) return;
    
    setIsAnalyzing(true);
    
    try {
      // For production, replace this with actual API call
      // const response = await apiService.analyzePlant(image);
      
      // Simulating API delay
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Mock response
      setResult(mockResult);
      setPlantInfo(mockPlantInfo);
      
      toast({
        title: "Analysis complete",
        description: "We've analyzed your plant image",
      });
    } catch (error) {
      console.error("Error analyzing plant:", error);
      toast({
        title: "Error analyzing plant",
        description: error.message || "Please try again later",
        variant: "destructive"
      });
    } finally {
      setIsAnalyzing(false);
    }
  };
  
  useEffect(() => {
    // Clear results when component mounts
    setResult(null);
    setPlantInfo(null);
    setImage(null);
  }, []);

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      
      {/* Hero Section */}
      <section className="pt-28 pb-12 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center justify-center p-2 bg-accent rounded-full mb-6 animate-fade-in">
            <Leaf className="w-5 h-5 text-primary" />
          </div>
          <h1 className="text-4xl md:text-5xl font-bold tracking-tight animate-slide-down">
            Plant Disease Detection
          </h1>
          <p className="mt-4 text-lg text-muted-foreground max-w-2xl mx-auto animate-slide-down" style={{ animationDelay: '100ms' }}>
            Upload a photo of your plant and our AI will analyze it to identify diseases and provide treatment solutions.
          </p>
        </div>
      </section>
      
      {/* Upload Section */}
      <section className="py-6 px-6">
        <div className="max-w-4xl mx-auto">
          <ImageUploader onImageUpload={handleImageUpload} isLoading={isAnalyzing} />
          
          {image && !isAnalyzing && !result && (
            <div className="mt-6 flex justify-center">
              <button
                onClick={analyzePlant}
                className="px-6 py-3 bg-primary text-primary-foreground rounded-full text-base font-medium transition-all hover:opacity-90 flex items-center"
              >
                Analyze Plant
              </button>
            </div>
          )}
          
          {isAnalyzing && (
            <Loading text="Analyzing your plant..." className="mt-8" />
          )}
        </div>
      </section>
      
      {/* Results Section */}
      {result && (
        <section className="py-8 px-6">
          <div className="max-w-5xl mx-auto">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <ResultCard result={result} />
              <PlantInfo plantData={plantInfo} />
            </div>
          </div>
        </section>
      )}
      
      {/* Features Section */}
      <section className="py-16 px-6 bg-accent/40 mt-auto">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-2xl md:text-3xl font-bold">How It Works</h2>
            <p className="mt-2 text-muted-foreground">Our advanced AI analyzes your plant images in three simple steps</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                title: "Upload Image",
                description: "Take a clear photo of your plant showing the affected areas and upload it to our system."
              },
              {
                title: "AI Analysis",
                description: "Our CNN model analyzes the image to identify the disease with high accuracy."
              },
              {
                title: "Get Solutions",
                description: "Receive detailed diagnosis and treatment recommendations from our LLM."
              }
            ].map((feature, index) => (
              <div key={index} className="glass-card p-6 rounded-xl text-center">
                <div className="w-12 h-12 bg-primary rounded-full flex items-center justify-center text-primary-foreground font-bold text-lg mx-auto mb-4">
                  {index + 1}
                </div>
                <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                <p className="text-muted-foreground">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
      
      {/* Footer */}
      <footer className="py-6 px-6 border-t">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center">
          <div className="flex items-center mb-4 md:mb-0">
            <Leaf className="w-5 h-5 text-primary mr-2" />
            <span className="font-medium">Plantopia</span>
          </div>
          
          <div className="text-sm text-muted-foreground">
            © {new Date().getFullYear()} Plantopia. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Index;
