import React, { useEffect, useState } from "react";
import axios from "axios";

const API_URL = "http://127.0.0.1:8002/accounts";

function Accounts() {
  const [accounts, setAccounts] = useState([]);
  const [form, setForm] = useState({
    user_id: '',
    account_type: 'checking',
    balance: 0,
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  const fetchAccounts = async () => {
    try {
      setLoading(true);
      const res = await axios.get(API_URL);
      setAccounts(res.data);
      setError('');
    } catch (error) {
      setError(
        `Failed to load accounts: ${
          error.response?.data?.detail || error.message
        }`,
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAccounts();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    // Basic validation
    if (!form.user_id || !form.account_type) {
      setError('User ID and Account Type are required');
      return;
    }

    if (isNaN(form.user_id) || parseInt(form.user_id) <= 0) {
      setError('User ID must be a positive number');
      return;
    }

    if (isNaN(form.balance) || parseFloat(form.balance) < 0) {
      setError('Balance must be a non-negative number');
      return;
    }

    try {
      setLoading(true);
      const accountData = {
        user_id: parseInt(form.user_id),
        account_type: form.account_type,
        balance: parseFloat(form.balance),
      };
      await axios.post(API_URL, accountData);
      setSuccess('Account created successfully!');
      setForm({ user_id: '', account_type: 'checking', balance: 0 });
      fetchAccounts();
    } catch (error) {
      const errorMessage = error.response?.data?.detail || error.message;
      setError(`Error creating account: ${errorMessage}`);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this account?')) {
      try {
        setLoading(true);
        await axios.delete(`${API_URL}/${id}`);
        setSuccess('Account deleted successfully!');
        fetchAccounts();
      } catch (error) {
        const errorMessage = error.response?.data?.detail || error.message;
        setError(`Error deleting account: ${errorMessage}`);
      } finally {
        setLoading(false);
      }
    }
  };

  return (
    <div>
      <h2>Accounts</h2>

      {error && (
        <div
          style={{
            color: 'red',
            marginBottom: '10px',
            padding: '10px',
            backgroundColor: '#ffe6e6',
            border: '1px solid red',
            borderRadius: '4px',
          }}
        >
          {error}
        </div>
      )}

      {success && (
        <div
          style={{
            color: 'green',
            marginBottom: '10px',
            padding: '10px',
            backgroundColor: '#e6ffe6',
            border: '1px solid green',
            borderRadius: '4px',
          }}
        >
          {success}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <input
          placeholder="User ID"
          type="number"
          value={form.user_id}
          onChange={(e) => setForm({ ...form, user_id: e.target.value })}
          disabled={loading}
          required
        />
        <select
          value={form.account_type}
          onChange={(e) => setForm({ ...form, account_type: e.target.value })}
          disabled={loading}
          required
        >
          <option value="checking">Checking</option>
          <option value="savings">Savings</option>
          <option value="business">Business</option>
        </select>
        <input
          placeholder="Initial Balance"
          type="number"
          step="0.01"
          min="0"
          value={form.balance}
          onChange={(e) => setForm({ ...form, balance: e.target.value })}
          disabled={loading}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Adding...' : 'Add Account'}
        </button>
      </form>

      {loading && accounts.length === 0 ? (
        <p>Loading accounts...</p>
      ) : (
        <div style={{ marginTop: '20px' }}>
          <table
            style={{
              width: '100%',
              borderCollapse: 'collapse',
              border: '1px solid #ddd',
            }}
          >
            <thead>
              <tr style={{ backgroundColor: '#f2f2f2', color: '#000000' }}>
                <th
                  style={{
                    border: '1px solid #ddd',
                    padding: '12px',
                    textAlign: 'left',
                  }}
                >
                  ID
                </th>
                <th
                  style={{
                    border: '1px solid #ddd',
                    padding: '12px',
                    textAlign: 'left',
                  }}
                >
                  User ID
                </th>
                <th
                  style={{
                    border: '1px solid #ddd',
                    padding: '12px',
                    textAlign: 'left',
                  }}
                >
                  Account Type
                </th>
                <th
                  style={{
                    border: '1px solid #ddd',
                    padding: '12px',
                    textAlign: 'left',
                  }}
                >
                  Balance
                </th>
                <th
                  style={{
                    border: '1px solid #ddd',
                    padding: '12px',
                    textAlign: 'left',
                  }}
                >
                  Actions
                </th>
              </tr>
            </thead>
            <tbody>
              {accounts.map((a) => (
                <tr key={a.id}>
                  <td style={{ border: '1px solid #ddd', padding: '12px' }}>
                    {a.id}
                  </td>
                  <td style={{ border: '1px solid #ddd', padding: '12px' }}>
                    {a.user_id}
                  </td>
                  <td style={{ border: '1px solid #ddd', padding: '12px' }}>
                    {a.account_type}
                  </td>
                  <td style={{ border: '1px solid #ddd', padding: '12px' }}>
                    ${a.balance.toFixed(2)}
                  </td>
                  <td style={{ border: '1px solid #ddd', padding: '12px' }}>
                    <button
                      onClick={() => handleDelete(a.id)}
                      style={{
                        backgroundColor: '#b00020',
                        color: 'white',
                        border: 'none',
                        padding: '8px 12px',
                        borderRadius: '4px',
                        cursor: 'pointer',
                      }}
                      disabled={loading}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default Accounts;
