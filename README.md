# Microservices Banking Application

A modern banking application built with microservices architecture using FastAPI and React.

## Architecture Overview

This application consists of four microservices:

- **User Service** (Port 8001) - Manages user accounts and profiles
- **Account Service** (Port 8002) - Handles bank account management
- **Transaction Service** (Port 8003) - Processes deposits, withdrawals, and transfers
- **Notification Service** (Port 8004) - Sends notifications for transactions
- **Frontend** (Port 3000) - React-based user interface

## Features

- ✅ User registration and management
- ✅ Bank account creation and management
- ✅ Transaction processing (deposits, withdrawals, transfers)
- ✅ Real-time notifications
- ✅ Modern React frontend
- ✅ RESTful API design
- ✅ SQLite database for each service
- ✅ CORS-enabled for frontend communication

## Tech Stack

### Backend Services
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **SQLite** - Lightweight database
- **Pydantic** - Data validation and serialization
- **Uvicorn** - ASGI server

### Frontend
- **React** - JavaScript library for building user interfaces
- **Axios** - HTTP client for API communication
- **CSS** - Styling

## Project Structure

```
microservices-banking-app/
├── user_service/          # User management service
│   ├── app/
│   │   ├── main.py        # FastAPI application
│   │   ├── models.py      # Database models
│   │   ├── schemas.py     # Pydantic schemas
│   │   ├── crud.py        # Database operations
│   │   └── database.py    # Database configuration
│   ├── db/
│   │   └── users.db       # SQLite database
│   └── requirements.txt   # Python dependencies
├── account_service/       # Account management service
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── crud.py
│   │   └── database.py
│   ├── db/
│   │   └── accounts.db
│   └── requirements.txt
├── transaction_service/    # Transaction processing service
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── crud.py
│   │   └── database.py
│   ├── db/
│   │   └── transactions.db
│   └── requirements.txt
├── notification_service/   # Notification service
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── crud.py
│   │   └── database.py
│   ├── db/
│   │   └── notifications.db
│   └── requirements.txt
└── frontend/              # React frontend
    ├── src/
    │   ├── components/    # React components
    │   └── services/      # API service functions
    ├── package.json
    └── package-lock.json
```

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-github-repo-url>
   cd microservices-banking-app
   ```

2. **Set up Backend Services**

   For each service (user_service, account_service, transaction_service, notification_service):
   
   ```bash
   cd user_service
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up Frontend**
   ```bash
   cd frontend
   npm install
   ```

### Running the Application

1. **Start Backend Services**

   Open separate terminal windows for each service:

   ```bash
   # Terminal 1 - User Service
   cd user_service
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload

   # Terminal 2 - Account Service
   cd account_service
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload

   # Terminal 3 - Transaction Service
   cd transaction_service
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8003 --reload

   # Terminal 4 - Notification Service
   cd notification_service
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8004 --reload
   ```

2. **Start Frontend**
   ```bash
   cd frontend
   npm start
   ```

3. **Access the Application**
   - Frontend: http://localhost:3000
   - User Service API: http://localhost:8001
   - Account Service API: http://localhost:8002
   - Transaction Service API: http://localhost:8003
   - Notification Service API: http://localhost:8004

## API Endpoints

### User Service (Port 8001)
- `GET /` - Service status
- `POST /users` - Create user
- `GET /users` - Get all users
- `GET /users/{user_id}` - Get user by ID
- `DELETE /users/{user_id}` - Delete user

### Account Service (Port 8002)
- `GET /` - Service status
- `POST /accounts` - Create account
- `GET /accounts` - Get all accounts
- `GET /accounts/{account_id}` - Get account by ID
- `DELETE /accounts/{account_id}` - Delete account

### Transaction Service (Port 8003)
- `GET /` - Service status
- `POST /transactions` - Create transaction
- `GET /transactions` - Get all transactions
- `GET /transactions/{transaction_id}` - Get transaction by ID
- `DELETE /transactions/{transaction_id}` - Delete transaction

### Notification Service (Port 8004)
- `GET /` - Service status
- `POST /notifications` - Create notification
- `GET /notifications` - Get all notifications
- `GET /notifications/{notification_id}` - Get notification by ID
- `DELETE /notifications/{notification_id}` - Delete notification

## Usage

1. **Create a User**: Use the Users tab to add new users with name, email, and phone
2. **Create an Account**: Use the Accounts tab to create bank accounts for users
3. **Process Transactions**: Use the Transactions tab to perform deposits, withdrawals, or transfers
4. **View Notifications**: Check the Notifications tab to see transaction alerts

## Development

### Adding New Features

1. **Backend**: Add new endpoints in the respective service's `main.py`
2. **Frontend**: Create new components in `frontend/src/components/`
3. **Database**: Update models in `models.py` and run migrations

### Database Schema

Each service maintains its own SQLite database with the following tables:

- **Users**: id, name, email, phone
- **Accounts**: id, user_id, account_type, balance
- **Transactions**: id, account_id, type, amount, target_account_id, timestamp
- **Notifications**: id, user_id, message, timestamp

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Future Enhancements

- [ ] Authentication and authorization
- [ ] Docker containerization
- [ ] Kubernetes deployment
- [ ] Message queuing with Redis/RabbitMQ
- [ ] Database migration to PostgreSQL
- [ ] API rate limiting
- [ ] Comprehensive logging
- [ ] Unit and integration tests
- [ ] CI/CD pipeline
