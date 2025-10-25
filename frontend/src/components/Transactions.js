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
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  const fetchTransactions = async () => {
    try {
      setLoading(true);
      const res = await axios.get(API_URL);
      setTransactions(res.data);
      setError('');
    } catch (error) {
      setError(
        `Failed to load transactions: ${
          error.response?.data?.detail || error.message
        }`,
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTransactions();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    // Basic validation
    if (!form.account_id || !form.amount) {
      setError('Account ID and Amount are required');
      return;
    }

    if (isNaN(form.account_id) || parseInt(form.account_id) <= 0) {
      setError('Account ID must be a positive number');
      return;
    }

    if (isNaN(form.amount) || parseFloat(form.amount) <= 0) {
      setError('Amount must be a positive number');
      return;
    }

    if (
      form.type === 'transfer' &&
      (!form.target_account_id ||
        isNaN(form.target_account_id) ||
        parseInt(form.target_account_id) <= 0)
    ) {
      setError(
        'Target Account ID is required for transfers and must be a positive number',
      );
      return;
    }

    try {
      setLoading(true);
      const transactionData = {
        account_id: parseInt(form.account_id),
        amount: parseFloat(form.amount),
        type: form.type,
        target_account_id: form.target_account_id
          ? parseInt(form.target_account_id)
          : null,
      };

      await axios.post(API_URL, transactionData);
      setSuccess(
        `${
          form.type.charAt(0).toUpperCase() + form.type.slice(1)
        } transaction completed successfully!`,
      );
      setForm({
        account_id: '',
        amount: '',
        type: 'deposit',
        target_account_id: '',
      });
      fetchTransactions();
    } catch (error) {
      const errorMessage = error.response?.data?.detail || error.message;
      setError(`Transaction failed: ${errorMessage}`);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this transaction?')) {
      try {
        setLoading(true);
        await axios.delete(`${API_URL}/${id}`);
        setSuccess('Transaction deleted successfully!');
        fetchTransactions();
      } catch (error) {
        const errorMessage = error.response?.data?.detail || error.message;
        setError(`Error deleting transaction: ${errorMessage}`);
      } finally {
        setLoading(false);
      }
    }
  };

  return (
    <div>
      <h2>Transactions</h2>

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
          placeholder="Account ID"
          type="number"
          value={form.account_id}
          onChange={(e) => setForm({ ...form, account_id: e.target.value })}
          disabled={loading}
          required
        />
        <input
          placeholder="Amount"
          type="number"
          step="0.01"
          min="0.01"
          value={form.amount}
          onChange={(e) => setForm({ ...form, amount: e.target.value })}
          disabled={loading}
          required
        />
        <select
          value={form.type}
          onChange={(e) => setForm({ ...form, type: e.target.value })}
          disabled={loading}
          required
        >
          <option value="deposit">Deposit</option>
          <option value="withdraw">Withdraw</option>
          <option value="transfer">Transfer</option>
        </select>
        {form.type === 'transfer' && (
          <input
            placeholder="Target Account ID"
            type="number"
            value={form.target_account_id}
            onChange={(e) =>
              setForm({ ...form, target_account_id: e.target.value })
            }
            disabled={loading}
            required
          />
        )}
        <button type="submit" disabled={loading}>
          {loading ? 'Processing...' : 'Process Transaction'}
        </button>
      </form>

      {loading && transactions.length === 0 ? (
        <p>Loading transactions...</p>
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
                  Type
                </th>
                <th
                  style={{
                    border: '1px solid #ddd',
                    padding: '12px',
                    textAlign: 'left',
                  }}
                >
                  Amount
                </th>
                <th
                  style={{
                    border: '1px solid #ddd',
                    padding: '12px',
                    textAlign: 'left',
                  }}
                >
                  Account ID
                </th>
                <th
                  style={{
                    border: '1px solid #ddd',
                    padding: '12px',
                    textAlign: 'left',
                  }}
                >
                  Target Account
                </th>
                <th
                  style={{
                    border: '1px solid #ddd',
                    padding: '12px',
                    textAlign: 'left',
                  }}
                >
                  Timestamp
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
              {transactions.map((t) => (
                <tr key={t.id}>
                  <td style={{ border: '1px solid #ddd', padding: '12px' }}>
                    {t.id}
                  </td>
                  <td style={{ border: '1px solid #ddd', padding: '12px' }}>
                    <strong>
                      {t.type.charAt(0).toUpperCase() + t.type.slice(1)}
                    </strong>
                  </td>
                  <td style={{ border: '1px solid #ddd', padding: '12px' }}>
                    ${t.amount.toFixed(2)}
                  </td>
                  <td style={{ border: '1px solid #ddd', padding: '12px' }}>
                    {t.account_id}
                  </td>
                  <td style={{ border: '1px solid #ddd', padding: '12px' }}>
                    {t.target_account_id ? t.target_account_id : '-'}
                  </td>
                  <td style={{ border: '1px solid #ddd', padding: '12px' }}>
                    {new Date(t.timestamp).toLocaleString()}
                  </td>
                  <td style={{ border: '1px solid #ddd', padding: '12px' }}>
                    <button
                      onClick={() => handleDelete(t.id)}
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

export default Transactions;
