import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const predictChurn = async (customerData) => {
  try {
    const response = await api.post('/predict', customerData);
    return { success: true, data: response.data };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.detail || 'Prediction failed',
    };
  }
};

export const getModelInfo = async () => {
  try {
    const response = await api.get('/model/info');
    return { success: true, data: response.data };
  } catch (error) {
    return { success: false, error: 'Failed to fetch model info' };
  }
};

export const healthCheck = async () => {
  try {
    const response = await api.get('/health');
    return { success: true, data: response.data };
  } catch (error) {
    return { success: false, error: 'API is down' };
  }
};

export default api;