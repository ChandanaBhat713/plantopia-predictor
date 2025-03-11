
import React, { useState, useRef } from 'react';
import { cn } from "@/lib/utils";
import { Upload, Image as ImageIcon, X } from 'lucide-react';
import { toast } from "@/hooks/use-toast";

const ImageUploader = ({ onImageUpload, isLoading }) => {
  const [dragActive, setDragActive] = useState(false);
  const [preview, setPreview] = useState(null);
  const inputRef = useRef(null);
  
  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };
  
  const validateFile = (file) => {
    // Check file type
    if (!file.type.startsWith('image/')) {
      toast({
        title: "Invalid file type",
        description: "Please upload an image file (JPG, PNG, etc.)",
        variant: "destructive"
      });
      return false;
    }
    
    // Check file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
      toast({
        title: "File too large",
        description: "Please upload an image smaller than 5MB",
        variant: "destructive"
      });
      return false;
    }
    
    return true;
  };
  
  const processImage = (file) => {
    if (!validateFile(file)) return;
    
    // Create preview
    const reader = new FileReader();
    reader.onload = () => {
      setPreview(reader.result);
    };
    reader.readAsDataURL(file);
    
    // Pass to parent component
    onImageUpload(file);
  };
  
  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      processImage(e.dataTransfer.files[0]);
    }
  };
  
  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      processImage(e.target.files[0]);
    }
  };
  
  const removeImage = () => {
    setPreview(null);
    if (inputRef.current) {
      inputRef.current.value = "";
    }
    onImageUpload(null);
  };

  return (
    <div className="w-full max-w-2xl mx-auto transition-all duration-300">
      <div 
        className={cn(
          "image-drop-zone rounded-2xl border-2 p-1 transition-all duration-300",
          preview ? "border-transparent" : "border-dashed border-muted-foreground/30",
          dragActive && "active"
        )}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        {!preview ? (
          <div className="h-[400px] flex flex-col items-center justify-center text-center p-8 space-y-4 bg-secondary/50 rounded-xl">
            <div className="w-16 h-16 rounded-full bg-background flex items-center justify-center animate-pulse-subtle">
              <Upload className="w-8 h-8 text-primary" />
            </div>
            <div className="space-y-2 max-w-md">
              <h3 className="font-medium text-lg">Upload plant image</h3>
              <p className="text-sm text-muted-foreground">
                Drop your plant image here or click to browse.<br />
                Supports JPG, PNG, etc.
              </p>
            </div>
            <button 
              onClick={() => inputRef.current?.click()}
              disabled={isLoading}
              className="px-4 py-2 bg-primary text-primary-foreground rounded-full text-sm font-medium transition-all hover:opacity-90 disabled:opacity-50"
            >
              Select Image
            </button>
          </div>
        ) : (
          <div className="relative rounded-xl overflow-hidden group">
            <img 
              src={preview} 
              alt="Plant preview" 
              className="w-full h-[400px] object-contain bg-secondary/50 rounded-xl"
            />
            <div className="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-all flex items-center justify-center">
              <button 
                onClick={removeImage}
                disabled={isLoading}
                className="p-2 bg-white/80 rounded-full opacity-0 group-hover:opacity-100 transition-all hover:bg-white"
              >
                <X className="w-5 h-5 text-red-500" />
              </button>
            </div>
          </div>
        )}
      </div>
      
      <input
        ref={inputRef}
        type="file"
        className="hidden"
        accept="image/*"
        onChange={handleChange}
        disabled={isLoading}
      />
      
      {preview && (
        <p className="text-xs text-center mt-2 text-muted-foreground">
          {isLoading ? "Analyzing your plant..." : "Image ready for analysis"}
        </p>
      )}
    </div>
  );
};

export default ImageUploader;
