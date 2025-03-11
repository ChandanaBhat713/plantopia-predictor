
import React from 'react';
import Navbar from '../components/Navbar';
import { cn } from "@/lib/utils";
import { Brain, Code, Database, Image, Leaf, Microscope, Network } from 'lucide-react';

const FeatureCard = ({ icon, title, description, className }) => (
  <div className={cn("glass-card p-6 rounded-xl", className)}>
    <div className="w-12 h-12 rounded-lg bg-accent flex items-center justify-center mb-4">
      {icon}
    </div>
    <h3 className="text-lg font-medium mb-2">{title}</h3>
    <p className="text-muted-foreground text-sm">{description}</p>
  </div>
);

const About = () => {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      
      {/* Hero Section */}
      <section className="pt-28 pb-12 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center justify-center p-2 bg-accent rounded-full mb-6 animate-fade-in">
            <Leaf className="w-5 h-5 text-primary" />
          </div>
          <h1 className="text-4xl md:text-5xl font-bold tracking-tight animate-slide-down">About Plantopia</h1>
          <p className="mt-4 text-lg text-muted-foreground max-w-2xl mx-auto animate-slide-down" style={{ animationDelay: '100ms' }}>
            Leveraging cutting-edge AI to revolutionize plant disease detection and treatment
          </p>
        </div>
      </section>
      
      {/* Technology Stack */}
      <section className="py-12 px-6">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-2xl md:text-3xl font-bold">Our Technology</h2>
            <p className="mt-2 text-muted-foreground">Powered by advanced machine learning and AI</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <FeatureCard
              icon={<Network className="w-6 h-6 text-primary" />}
              title="Convolutional Neural Networks"
              description="We utilize state-of-the-art CNN architectures to analyze plant images with high accuracy and identify patterns associated with various diseases."
              className="animate-fade-in"
              style={{ animationDelay: '0ms' }}
            />
            
            <FeatureCard
              icon={<Brain className="w-6 h-6 text-primary" />}
              title="Large Language Models"
              description="Our system leverages advanced LLMs to provide detailed treatment recommendations and care instructions tailored to the specific plant disease."
              className="animate-fade-in"
              style={{ animationDelay: '100ms' }}
            />
            
            <FeatureCard
              icon={<Database className="w-6 h-6 text-primary" />}
              title="Comprehensive Plant Database"
              description="Access to an extensive database of plant species, diseases, and treatment protocols ensures accurate and reliable guidance."
              className="animate-fade-in"
              style={{ animationDelay: '200ms' }}
            />
          </div>
        </div>
      </section>
      
      {/* How It Works */}
      <section className="py-12 px-6 bg-accent/40">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-2xl md:text-3xl font-bold">The Science Behind It</h2>
            <p className="mt-2 text-muted-foreground">Understanding our advanced AI pipeline</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
            <div className="space-y-8">
              <div className="relative pl-10">
                <div className="absolute left-0 top-0 w-6 h-6 rounded-full bg-primary flex items-center justify-center text-white font-medium">1</div>
                <h3 className="text-xl font-medium mb-2">Image Processing</h3>
                <p className="text-muted-foreground">
                  When you upload a plant image, our system preprocesses it through various techniques including normalization, augmentation, and segmentation to isolate the affected areas.
                </p>
              </div>
              
              <div className="relative pl-10">
                <div className="absolute left-0 top-0 w-6 h-6 rounded-full bg-primary flex items-center justify-center text-white font-medium">2</div>
                <h3 className="text-xl font-medium mb-2">CNN Classification</h3>
                <p className="text-muted-foreground">
                  Our CNN model analyzes the processed image, extracting features that indicate various plant diseases. The model has been trained on thousands of labeled plant disease images to ensure high accuracy.
                </p>
              </div>
              
              <div className="relative pl-10">
                <div className="absolute left-0 top-0 w-6 h-6 rounded-full bg-primary flex items-center justify-center text-white font-medium">3</div>
                <h3 className="text-xl font-medium mb-2">LLM Treatment Guidance</h3>
                <p className="text-muted-foreground">
                  Once the disease is identified, our LLM system generates detailed treatment recommendations, care guidelines, and preventive measures based on the latest agricultural research.
                </p>
              </div>
            </div>
            
            <div className="glass-card p-6 rounded-xl h-full flex items-center justify-center">
              {/* Placeholder for diagram/illustration */}
              <div className="w-full max-w-sm h-64 bg-secondary/50 rounded-lg flex items-center justify-center">
                <Microscope className="w-16 h-16 text-primary/30" />
              </div>
            </div>
          </div>
        </div>
      </section>
      
      {/* Team/Mission */}
      <section className="py-12 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-2xl md:text-3xl font-bold mb-4">Our Mission</h2>
          <p className="text-lg text-muted-foreground">
            At Plantopia, we're committed to democratizing access to plant disease diagnosis and treatment. By combining cutting-edge AI technology with expert agricultural knowledge, we aim to help hobbyist gardeners, farmers, and agricultural professionals identify and treat plant diseases quickly and effectively, reducing crop losses and promoting sustainable gardening and farming practices.
          </p>
        </div>
      </section>
      
      {/* Technologies Used */}
      <section className="py-12 px-6 bg-accent/40">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-2xl md:text-3xl font-bold">Built With</h2>
            <p className="mt-2 text-muted-foreground">Technologies powering our platform</p>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { name: "React", icon: <Code className="w-8 h-8" /> },
              { name: "TensorFlow", icon: <Brain className="w-8 h-8" /> },
              { name: "Django", icon: <Database className="w-8 h-8" /> },
              { name: "LLM AI", icon: <Image className="w-8 h-8" /> },
            ].map((tech, index) => (
              <div key={index} className="glass-card p-4 text-center rounded-xl">
                <div className="flex justify-center mb-2">
                  {tech.icon}
                </div>
                <h3 className="font-medium">{tech.name}</h3>
              </div>
            ))}
          </div>
        </div>
      </section>
      
      {/* Footer */}
      <footer className="py-6 px-6 border-t mt-auto">
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

export default About;
