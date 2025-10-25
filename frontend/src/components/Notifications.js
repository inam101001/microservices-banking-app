import React, { useEffect, useState } from "react";
import axios from "axios";

const API_URL = "http://127.0.0.1:8004/notifications";

function Notifications() {
  const [notifications, setNotifications] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const fetchNotifications = async () => {
    try {
      setLoading(true);
      const res = await axios.get(API_URL);
      setNotifications(res.data);
      setError('');
    } catch (error) {
      setError(
        `Failed to load notifications: ${
          error.response?.data?.detail || error.message
        }`,
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchNotifications();
    const interval = setInterval(fetchNotifications, 5000); // auto-refresh every 5 seconds
    return () => clearInterval(interval);
  }, []);

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this notification?')) {
      try {
        setLoading(true);
        await axios.delete(`${API_URL}/${id}`);
        fetchNotifications();
      } catch (error) {
        const errorMessage = error.response?.data?.detail || error.message;
        setError(`Error deleting notification: ${errorMessage}`);
      } finally {
        setLoading(false);
      }
    }
  };

  return (
    <div>
      <h2>Notifications</h2>

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

      {loading && notifications.length === 0 ? (
        <p>Loading notifications...</p>
      ) : notifications.length === 0 ? (
        <p>No notifications yet.</p>
      ) : (
        <div style={{ marginTop: '20px' }}>
          {notifications.map((n) => (
            <div
              key={n.id}
              style={{
                marginBottom: '15px',
                padding: '15px',
                backgroundColor: '#2c2c2c',
                color: '#ffffff',
                border: '1px solid #444',
                borderRadius: '8px',
                boxShadow: '0 2px 4px rgba(0,0,0,0.3)',
              }}
            >
              <div
                style={{
                  fontWeight: 'bold',
                  marginBottom: '8px',
                  color: '#4CAF50',
                }}
              >
                User {n.user_id}
              </div>
              <div style={{ marginBottom: '8px', fontSize: '16px' }}>
                {n.message}
              </div>
              <div
                style={{
                  color: '#ccc',
                  fontSize: '14px',
                  marginBottom: '10px',
                }}
              >
                {new Date(n.timestamp).toLocaleString()}
              </div>
              <button
                onClick={() => handleDelete(n.id)}
                style={{
                  backgroundColor: '#b00020',
                  color: 'white',
                  border: 'none',
                  padding: '8px 12px',
                  borderRadius: '4px',
                  cursor: 'pointer',
                  fontSize: '14px',
                }}
                disabled={loading}
              >
                Delete
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Notifications;
