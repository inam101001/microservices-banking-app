import React, { useEffect, useState } from "react";
import axios from "axios";

const API_URL = "http://127.0.0.1:8002/accounts";

function Accounts() {
  const [accounts, setAccounts] = useState([]);
  const [form, setForm] = useState({ user_id: "", account_type: "", balance: 0 });

  const fetchAccounts = async () => {
    const res = await axios.get(API_URL);
    setAccounts(res.data);
  };

  useEffect(() => {
    fetchAccounts();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const accountData = {
      user_id: parseInt(form.user_id),
      account_type: form.account_type,
      balance: parseFloat(form.balance)
    };
    await axios.post(API_URL, accountData);
    setForm({ user_id: "", account_type: "", balance: 0 });
    fetchAccounts();
  };

  const handleDelete = async (id) => {
    if (window.confirm("Are you sure you want to delete this account?")) {
      await axios.delete(`${API_URL}/${id}`);
      fetchAccounts();
    }
  };

  return (
    <div>
      <h2>Accounts</h2>
      <form onSubmit={handleSubmit}>
        <input
          placeholder="User ID"
          value={form.user_id}
          onChange={(e) => setForm({ ...form, user_id: e.target.value })}
        />
        <input
          placeholder="Account Type"
          value={form.account_type}
          onChange={(e) => setForm({ ...form, account_type: e.target.value })}
        />
        <input
          placeholder="Balance"
          value={form.balance}
          onChange={(e) => setForm({ ...form, balance: e.target.value })}
        />
        <button type="submit">Add Account</button>
      </form>
      <ul>
        {accounts.map((a) => (
          <li key={a.id}>
            User {a.user_id} – {a.account_type} – Balance: {a.balance}{" "}
            <button
              onClick={() => handleDelete(a.id)}
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

export default Accounts;
