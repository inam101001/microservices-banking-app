import axios from "axios";

const USER_SERVICE_URL = "http://127.0.0.1:8001";

export const createUser = async (user) => {
  const response = await axios.post(`${USER_SERVICE_URL}/users`, user);
  return response.data;
};

export const getUsers = async () => {
  const response = await axios.get(`${USER_SERVICE_URL}/users`);
  return response.data;
};
