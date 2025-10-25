import React from "react";
import Users from "./components/Users";
import Accounts from "./components/Accounts";
import Transactions from "./components/Transactions";
import Notifications from "./components/Notifications";

function App() {
  return (
    <div style={{ maxWidth: "900px", margin: "0 auto", padding: "20px" }}>
      <header>Microservices Banking App</header>

      <div className="card">
        <Users />
      </div>

      <div className="card">
        <Accounts />
      </div>

      <div className="card">
        <Transactions />
      </div>

      <Notifications />
    </div>
  );
}

export default App;
