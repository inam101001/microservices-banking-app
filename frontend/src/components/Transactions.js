import React, { useEffect, useState } from "react";
import axios from "axios";

const API_URL = "http://127.0.0.1:8003/transactions";

function Transactions() {
  const [transactions, setTransactions] = useState([]);
  const [form, setForm] = useState({
    account_id: "",
    amount: "",
    type: "deposit",
    target_account_id: "",
  });

  const fetchTransactions = async () => {
    const res = await axios.get(API_URL);
    setTransactions(res.data);
  };

  useEffect(() => {
    fetchTransactions();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const transactionData = {
      account_id: parseInt(form.account_id),
      amount: parseFloat(form.amount),
      type: form.type,
      target_account_id: form.target_account_id ? parseInt(form.target_account_id) : null
    };
    await axios.post(API_URL, transactionData);
    setForm({ account_id: "", amount: "", type: "deposit", target_account_id: "" });
    fetchTransactions();
  };

  const handleDelete = async (id) => {
    if (window.confirm("Delete this transaction?")) {
      await axios.delete(`${API_URL}/${id}`);
      fetchTransactions();
    }
  };

  return (
    <div>
      <h2>Transactions</h2>
      <form onSubmit={handleSubmit}>
        <input
          placeholder="Account ID"
          value={form.account_id}
          onChange={(e) => setForm({ ...form, account_id: e.target.value })}
        />
        <input
          placeholder="Amount"
          value={form.amount}
          onChange={(e) => setForm({ ...form, amount: e.target.value })}
        />
        <select
          value={form.type}
          onChange={(e) => setForm({ ...form, type: e.target.value })}
        >
          <option value="deposit">Deposit</option>
          <option value="withdraw">Withdraw</option>
          <option value="transfer">Transfer</option>
        </select>
        {form.type === "transfer" && (
          <input
            placeholder="Target Account ID"
            value={form.target_account_id}
            onChange={(e) =>
              setForm({ ...form, target_account_id: e.target.value })
            }
          />
        )}
        <button type="submit">Add Transaction</button>
      </form>
      <ul>
        {transactions.map((t) => (
          <li key={t.id}>
            {t.type} – {t.amount} (Account {t.account_id}){" "}
            <button
              onClick={() => handleDelete(t.id)}
              style={{ backgroundColor: "#b00020" }}
            >
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Transactions;
