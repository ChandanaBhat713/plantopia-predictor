
import axios from 'axios';

// Base URL for API - update with your FastAPI backend URL
const API_URL = process.env.NODE_ENV === 'production' 
  ? 'https://your-production-api.com/api' 
  : 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  }
});

// Add a request interceptor for handling authentication if needed
api.interceptors.request.use(
  (config) => {
    // You could add auth token here if needed
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add a response interceptor for global error handling
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

// API service functions
const apiService = {
  // Analyze plant image
  analyzePlant: async (imageFile) => {
    const formData = new FormData();
    formData.append('image', imageFile);
    
    try {
      const response = await api.post('/predict', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      console.error('Error analyzing plant:', error);
      throw error;
    }
  },
  
  // Get treatment for a specific disease
  getTreatment: async (disease) => {
    try {
      const response = await api.get(`/treatment/${encodeURIComponent(disease)}`);
      return response.data;
    } catch (error) {
      console.error('Error getting treatment:', error);
      throw error;
    }
  },
  
  // Get plant information
  getPlantInfo: async (plantName) => {
    try {
      const response = await api.get(`/plant-info/${encodeURIComponent(plantName)}`);
      return response.data;
    } catch (error) {
      console.error('Error getting plant info:', error);
      throw error;
    }
  },
  
  // Get scan history
  getScanHistory: async () => {
    try {
      const response = await api.get('/history');
      return response.data;
    } catch (error) {
      console.error('Error getting scan history:', error);
      throw error;
    }
  },
  
  // Get a specific scan by ID
  getScanById: async (scanId) => {
    try {
      const response = await api.get(`/history/${scanId}`);
      return response.data;
    } catch (error) {
      console.error('Error getting scan:', error);
      throw error;
    }
  },
};

export default apiService;
