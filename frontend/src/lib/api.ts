import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const uploadPDF = async (file: File, fileType: string) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('file_type', fileType);
  
  try {
    console.log(`📤 Uploading ${fileType}: ${file.name}`);
    const response = await api.post('/api/upload/pdf', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    console.log(`✓ Upload successful:`, response.data);
    return response.data;
  } catch (error: any) {
    console.error('❌ Upload error:', error.response?.data || error.message);
    throw error;
  }
};

export const extractTopicsFromJSON = async (jsonPaths: string[]) => {
  try {
    console.log(`🤖 Extracting topics from ${jsonPaths.length} JSON files`);
    const response = await api.post('/api/upload/extract-topics-from-json', jsonPaths);
    console.log(`✓ Topics extracted:`, response.data);
    return response.data;
  } catch (error: any) {
    console.error('❌ Topic extraction error:', error.response?.data || error.message);
    throw error;
  }
};

export const extractTopics = async (text: string, subject: string) => {
  try {
    const response = await api.post('/api/upload/extract-topics', { text, subject });
    return response.data;
  } catch (error: any) {
    console.error('Extract topics error:', error.response?.data || error.message);
    throw error;
  }
};

export const listExtractedFiles = async () => {
  try {
    const response = await api.get('/api/upload/list-extracted-files');
    return response.data;
  } catch (error: any) {
    console.error('List files error:', error.response?.data || error.message);
    throw error;
  }
};

export const createStudyPlan = async (data: any) => {
  try {
    const response = await api.post('/api/study-plan/create', data);
    return response.data;
  } catch (error: any) {
    console.error('Create study plan error:', error.response?.data || error.message);
    throw error;
  }
};

export const generatePlan = async (planId: number, topics: any[]) => {
  try {
    const response = await api.post(`/api/study-plan/${planId}/generate-plan`, { topics });
    return response.data;
  } catch (error: any) {
    console.error('Generate plan error:', error.response?.data || error.message);
    throw error;
  }
};

export const getDashboard = async (planId: number) => {
  try {
    const response = await api.get(`/api/study-plan/${planId}/dashboard`);
    return response.data;
  } catch (error: any) {
    console.error('Get dashboard error:', error.response?.data || error.message);
    throw error;
  }
};

export const getLesson = async (topicId: number) => {
  try {
    const response = await api.get(`/api/lessons/${topicId}`);
    return response.data;
  } catch (error: any) {
    console.error('Get lesson error:', error.response?.data || error.message);
    throw error;
  }
};

export const markSessionComplete = async (sessionId: number) => {
  try {
    const response = await api.post(`/api/lessons/${sessionId}/complete`);
    return response.data;
  } catch (error: any) {
    console.error('Mark session complete error:', error.response?.data || error.message);
    throw error;
  }
};

export default api;
