import React, { useEffect, useState } from "react";
import axios from "axios";

const API_URL = "http://127.0.0.1:8004/notifications";

function Notifications() {
  const [notifications, setNotifications] = useState([]);

  const fetchNotifications = async () => {
    const res = await axios.get(API_URL);
    setNotifications(res.data);
  };

  useEffect(() => {
    fetchNotifications();
    const interval = setInterval(fetchNotifications, 3000); // auto-refresh
    return () => clearInterval(interval);
  }, []);

  const handleDelete = async (id) => {
    if (window.confirm("Delete this notification?")) {
      await axios.delete(`${API_URL}/${id}`);
      fetchNotifications();
    }
  };

  return (
    <div>
      <h2>Notifications</h2>
      <ul>
        {notifications.map((n) => (
          <li key={n.id}>
            {n.message}{" "}
            <button
              onClick={() => handleDelete(n.id)}
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

export default Notifications;
