import React, { useEffect, useState } from "react";
import axios from "axios";

const API_URL = 'http://localhost/api/users';

function Users() {
  const [users, setUsers] = useState([]);
  const [form, setForm] = useState({ name: "", email: "", phone: "" });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  const fetchUsers = async () => {
    try {
      setLoading(true);
      const res = await axios.get(API_URL);
      setUsers(res.data);
      setError('');
    } catch (error) {
      setError(
        `Failed to load users: ${
          error.response?.data?.detail || error.message
        }`,
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    // Basic validation
    if (!form.name.trim() || !form.email.trim() || !form.phone.trim()) {
      setError('All fields are required');
      return;
    }

    try {
      setLoading(true);
      const response = await axios.post(API_URL, form);
      setSuccess('User created successfully!');
      setForm({ name: '', email: '', phone: '' });
      fetchUsers();
    } catch (error) {
      const errorMessage = error.response?.data?.detail || error.message;
      setError(`Error creating user: ${errorMessage}`);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this user?')) {
      try {
        setLoading(true);
        await axios.delete(`${API_URL}/${id}`);
        setSuccess('User deleted successfully!');
        fetchUsers();
      } catch (error) {
        const errorMessage = error.response?.data?.detail || error.message;
        setError(`Error deleting user: ${errorMessage}`);
      } finally {
        setLoading(false);
      }
    }
  };

  return (
    <div>
      <h2>Users</h2>

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
          placeholder="Name"
          value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
          disabled={loading}
          required
        />
        <input
          placeholder="Email"
          type="email"
          value={form.email}
          onChange={(e) => setForm({ ...form, email: e.target.value })}
          disabled={loading}
          required
        />
        <input
          placeholder="Phone"
          value={form.phone}
          onChange={(e) => setForm({ ...form, phone: e.target.value })}
          disabled={loading}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Adding...' : 'Add User'}
        </button>
      </form>

      {loading && users.length === 0 ? (
        <p>Loading users...</p>
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
                  Name
                </th>
                <th
                  style={{
                    border: '1px solid #ddd',
                    padding: '12px',
                    textAlign: 'left',
                  }}
                >
                  Email
                </th>
                <th
                  style={{
                    border: '1px solid #ddd',
                    padding: '12px',
                    textAlign: 'left',
                  }}
                >
                  Phone
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
              {users.map((u) => (
                <tr key={u.id}>
                  <td style={{ border: '1px solid #ddd', padding: '12px' }}>
                    {u.id}
                  </td>
                  <td style={{ border: '1px solid #ddd', padding: '12px' }}>
                    {u.name}
                  </td>
                  <td style={{ border: '1px solid #ddd', padding: '12px' }}>
                    {u.email}
                  </td>
                  <td style={{ border: '1px solid #ddd', padding: '12px' }}>
                    {u.phone}
                  </td>
                  <td style={{ border: '1px solid #ddd', padding: '12px' }}>
                    <button
                      onClick={() => handleDelete(u.id)}
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

export default Users;
