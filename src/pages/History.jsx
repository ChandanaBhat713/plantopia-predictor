
import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import HistoryItem from '../components/HistoryItem';
import Loading from '../components/Loading';
import apiService from '../services/api';
import { toast } from "@/hooks/use-toast";
import { ClipboardList, Search, X } from 'lucide-react';

const History = () => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  
  // Mock data for development - remove in production
  const mockHistory = [
    {
      id: '1',
      disease: 'Tomato Late Blight',
      imageUrl: 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Tomato_late_blight.jpg/800px-Tomato_late_blight.jpg',
      timestamp: new Date('2023-06-15T14:32:00').toISOString(),
    },
    {
      id: '2',
      disease: 'Rose Black Spot',
      imageUrl: 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Black_spot_%28rose_disease%29.jpg/800px-Black_spot_%28rose_disease%29.jpg',
      timestamp: new Date('2023-06-10T09:17:00').toISOString(),
    },
    {
      id: '3',
      disease: 'Apple Cedar Rust',
      imageUrl: 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f7/Cedar_apple_rust_on_apple_leaf.jpg/800px-Cedar_apple_rust_on_apple_leaf.jpg',
      timestamp: new Date('2023-06-01T16:45:00').toISOString(),
    },
  ];
  
  const fetchHistory = async () => {
    setLoading(true);
    
    try {
      // For production, replace this with actual API call
      // const data = await apiService.getScanHistory();
      
      // Simulating API delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Mock response
      setHistory(mockHistory);
    } catch (error) {
      console.error("Error fetching history:", error);
      toast({
        title: "Error loading history",
        description: error.message || "Please try again later",
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  };
  
  useEffect(() => {
    fetchHistory();
  }, []);
  
  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
  };
  
  const handleClearSearch = () => {
    setSearchTerm('');
  };
  
  const filteredHistory = history.filter(item => 
    item.disease.toLowerCase().includes(searchTerm.toLowerCase())
  );
  
  const handleItemClick = (item) => {
    // Navigate to detail view or show modal
    console.log("Clicked item:", item);
    // For now, we'll just show a toast
    toast({
      title: item.disease,
      description: `Scanned on ${new Date(item.timestamp).toLocaleString()}`,
    });
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      
      <div className="pt-28 pb-20 px-6">
        <div className="max-w-3xl mx-auto">
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between mb-8">
            <div>
              <h1 className="text-3xl font-bold">Scan History</h1>
              <p className="text-muted-foreground mt-1">Review your previous plant analyses</p>
            </div>
            
            <div className="relative w-full md:w-auto mt-4 md:mt-0">
              <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                <Search className="w-4 h-4 text-muted-foreground" />
              </div>
              <input
                type="text"
                className="pl-10 pr-10 py-2 border border-border bg-background rounded-lg w-full md:w-64"
                placeholder="Search diagnoses..."
                value={searchTerm}
                onChange={handleSearch}
              />
              {searchTerm && (
                <button 
                  className="absolute inset-y-0 right-0 flex items-center pr-3"
                  onClick={handleClearSearch}
                >
                  <X className="w-4 h-4 text-muted-foreground hover:text-foreground" />
                </button>
              )}
            </div>
          </div>
          
          {loading ? (
            <Loading text="Loading history..." />
          ) : (
            <>
              {filteredHistory.length > 0 ? (
                <div className="space-y-4 animate-fade-in">
                  {filteredHistory.map((item) => (
                    <HistoryItem 
                      key={item.id} 
                      scan={item} 
                      onClick={() => handleItemClick(item)}
                    />
                  ))}
                </div>
              ) : (
                <div className="text-center py-12 animate-fade-in">
                  <ClipboardList className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
                  
                  {searchTerm ? (
                    <>
                      <h3 className="text-lg font-medium">No matching results</h3>
                      <p className="text-muted-foreground mt-1">Try a different search term</p>
                    </>
                  ) : (
                    <>
                      <h3 className="text-lg font-medium">No history yet</h3>
                      <p className="text-muted-foreground mt-1">Your scan history will appear here</p>
                    </>
                  )}
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default History;
