import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8080' // Replace with your backend server URL
});

export default api;
