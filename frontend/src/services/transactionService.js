import axios from "axios";

const TRANSACTION_SERVICE_URL = "http://127.0.0.1:8003";

export const createTransaction = async (transaction) => {
  const response = await axios.post(`${TRANSACTION_SERVICE_URL}/transactions`, transaction);
  return response.data;
};

export const getTransactions = async (account_id = null) => {
  const url = account_id
    ? `${TRANSACTION_SERVICE_URL}/transactions?account_id=${account_id}`
    : `${TRANSACTION_SERVICE_URL}/transactions`;
  const response = await axios.get(url);
  return response.data;
};
