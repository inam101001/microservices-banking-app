import axios from "axios";

const NOTIFICATION_SERVICE_URL = "http://127.0.0.1:8004";

export const getNotifications = async () => {
  const response = await axios.get(`${NOTIFICATION_SERVICE_URL}/notifications`);
  return response.data;
};

export const createNotification = async (notification) => {
  const response = await axios.post(`${NOTIFICATION_SERVICE_URL}/notifications`, notification);
  return response.data;
};
