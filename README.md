# Microservices Banking Application

A modern banking application built with microservices architecture using FastAPI, React, Nginx Reverse Proxy, and RabbitMQ with comprehensive resilience testing.

## Architecture Overview

This application consists of:

- **User Service** (Port 8001) - Manages user accounts and profiles
- **Account Service** (Port 8002) - Handles bank account management
- **Transaction Service** (Port 8003) - Processes deposits, withdrawals, and transfers
- **Notification Service** (Port 8004) - Consumes events and sends notifications
- **Frontend** (Port 3000) - React-based user interface
- **Nginx Reverse Proxy** (Port 80) - API Gateway and load balancer
- **RabbitMQ** (Port 5672) - Message broker for event-driven communication

## Features

- ✅ User registration and management
- ✅ Bank account creation and management
- ✅ Transaction processing (deposits, withdrawals, transfers)
- ✅ Event-driven notifications via RabbitMQ
- ✅ Modern React frontend with table layouts
- ✅ RESTful API design
- ✅ SQLite database for each service
- ✅ CORS-enabled for frontend communication
- ✅ Reverse proxy for unified API access
- ✅ Asynchronous message processing
- ✅ Comprehensive error handling
- ✅ **RabbitMQ Resilience Testing** - Message persistence, queue durability, automatic reconnection
- ✅ **Service Failure Handling** - Graceful degradation when services are down
- ✅ **Real-time Monitoring** - RabbitMQ Management UI for queue monitoring

## Tech Stack

### Backend Services
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **SQLite** - Lightweight database
- **Pydantic** - Data validation and serialization
- **Uvicorn** - ASGI server
- **RabbitMQ** - Message broker for event-driven architecture
- **Pika** - Python RabbitMQ client

### Infrastructure
- **Nginx** - Reverse proxy and load balancer with CORS handling
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration

### Frontend
- **React** - JavaScript library for building user interfaces
- **Axios** - HTTP client for API communication
- **CSS** - Styling with table layouts

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
│   ├── venv/              # Python virtual environment
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
│   ├── venv/              # Python virtual environment
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
│   ├── rabbitmq_utils.py  # RabbitMQ utilities (copied from root)
│   ├── venv/              # Python virtual environment
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
│   ├── rabbitmq_utils.py  # RabbitMQ utilities (copied from root)
│   ├── venv/              # Python virtual environment
│   └── requirements.txt
├── frontend/              # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   └── services/      # API service functions
│   ├── package.json
│   └── package-lock.json
├── rabbitmq_utils.py     # Shared RabbitMQ utilities
├── nginx.conf            # Nginx configuration with CORS
├── docker-compose.yml    # Docker services configuration
├── setup.sh             # Linux/Mac setup script
├── setup.bat            # Windows setup script
└── README.md            # This file
```

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn
- Docker and Docker Compose

### Quick Setup

1. **Clone the repository**
   ```bash
   git clone <your-github-repo-url>
   cd microservices-banking-app
   ```

2. **Run the setup script**
   ```bash
   # On Linux/Mac
   chmod +x setup.sh
   ./setup.sh
   
   # On Windows
   setup.bat
   ```

3. **Install Python dependencies**
   ```bash
   cd user_service && source venv/bin/activate && pip install -r requirements.txt && cd ..
   cd account_service && source venv/bin/activate && pip install -r requirements.txt && cd ..
   cd transaction_service && source venv/bin/activate && pip install -r requirements.txt && cd ..
   cd notification_service && source venv/bin/activate && pip install -r requirements.txt && cd ..
   ```

4. **Install Frontend dependencies**
   ```bash
   cd frontend && npm install && cd ..
   ```

### Running the Application

1. **Start Infrastructure Services**
   ```bash
   docker-compose up -d
   ```

2. **Start Backend Services**

   Open separate terminal windows for each service:

   ```bash
   # Terminal 1 - User Service
   cd user_service
   source venv/bin/activate
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload

   # Terminal 2 - Account Service
   cd account_service
   source venv/bin/activate
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload

   # Terminal 3 - Transaction Service
   cd transaction_service
   source venv/bin/activate
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8003 --reload

   # Terminal 4 - Notification Service
   cd notification_service
   source venv/bin/activate
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8004 --reload
   ```

3. **Start Frontend**
   ```bash
   cd frontend
   npm start
   ```

4. **Access the Application**
   - Frontend: http://localhost:3000
   - API Gateway: http://localhost/api/users
   - RabbitMQ Management: http://localhost:15672 (admin/admin123)

## API Endpoints

### Via Reverse Proxy (Recommended)
- `GET /api/users` - Get all users
- `POST /api/users` - Create user
- `GET /api/users/{user_id}` - Get user by ID
- `DELETE /api/users/{user_id}` - Delete user

- `GET /api/accounts` - Get all accounts
- `POST /api/accounts` - Create account
- `GET /api/accounts/{account_id}` - Get account by ID
- `PUT /api/accounts/{account_id}` - Update account balance
- `DELETE /api/accounts/{account_id}` - Delete account

- `GET /api/transactions` - Get all transactions
- `POST /api/transactions` - Create transaction
- `GET /api/transactions/{transaction_id}` - Get transaction by ID
- `DELETE /api/transactions/{transaction_id}` - Delete transaction

- `GET /api/notifications` - Get all notifications
- `POST /api/notifications` - Create notification
- `GET /api/notifications/{notification_id}` - Get notification by ID
- `DELETE /api/notifications/{notification_id}` - Delete notification

### Direct Service Access
- User Service: http://localhost:8001
- Account Service: http://localhost:8002
- Transaction Service: http://localhost:8003
- Notification Service: http://localhost:8004

## Usage

1. **Create a User**: Use the Users tab to add new users with name, email, and phone
2. **Create an Account**: Use the Accounts tab to create bank accounts for users
3. **Process Transactions**: Use the Transactions tab to perform deposits, withdrawals, or transfers
4. **View Notifications**: Check the Notifications tab to see transaction alerts

## RabbitMQ Resilience Testing

The application includes comprehensive resilience testing capabilities:

### Test Scenarios

1. **Consumer Service Failure (Notification Service Down)**
   - Messages are queued in RabbitMQ when the consumer is down
   - No message loss occurs
   - Messages are automatically processed when the service restarts

2. **Publisher Service Failure (Transaction Service Down)**
   - System returns 502 Bad Gateway when service is unavailable
   - Service recovers normally after restart

3. **RabbitMQ Broker Failure**
   - Core business logic continues to work
   - Transactions are processed and stored in database
   - Notifications are queued and processed when RabbitMQ restarts

### Monitoring

- **RabbitMQ Management UI**: http://localhost:15672 (admin/admin123)
- **Real-time Queue Monitoring**: Monitor message flow, queue health, and consumer status
- **Message Persistence**: Messages survive broker restarts
- **Automatic Reconnection**: Services automatically reconnect when RabbitMQ comes back online

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

### Key Configuration Changes

1. **CORS Handling**: Centralized in Nginx configuration to prevent duplicate headers
2. **Nginx Network Mode**: Uses `host` network mode for proper service communication
3. **RabbitMQ Utilities**: Copied to transaction and notification services for proper imports
4. **Database Directories**: Created `db/` directories in each service for SQLite databases

## Troubleshooting

### Common Issues

1. **Service Connection Refused**: Ensure all services are running and ports are available
2. **CORS Errors**: Check Nginx configuration and ensure CORS headers are properly set
3. **RabbitMQ Connection Issues**: Verify RabbitMQ container is running and accessible
4. **Database Errors**: Ensure `db/` directories exist in each service

### Logs and Monitoring

- **Service Logs**: Check individual service terminal outputs
- **Nginx Logs**: `docker logs banking_nginx`
- **RabbitMQ Logs**: `docker logs banking_rabbitmq`
- **RabbitMQ Management**: http://localhost:15672 for queue monitoring

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Future Enhancements

- [x] Message queuing with RabbitMQ
- [x] Docker containerization
- [x] Comprehensive logging
- [x] Service resilience testing
- [ ] Authentication and authorization
- [ ] Kubernetes deployment
- [ ] Database migration to PostgreSQL
- [ ] API rate limiting
- [ ] Unit and integration tests
- [ ] CI/CD pipeline