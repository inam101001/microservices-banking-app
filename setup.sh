#!/bin/bash

# Banking App Setup Script
echo "🏦 Setting up Banking Microservices Application..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Start RabbitMQ and Nginx
echo "🐰 Starting RabbitMQ and Nginx..."
docker-compose up -d

# Wait for RabbitMQ to be ready
echo "⏳ Waiting for RabbitMQ to be ready..."
sleep 10

# Check if RabbitMQ is running
if ! docker ps | grep -q banking_rabbitmq; then
    echo "❌ Failed to start RabbitMQ"
    exit 1
fi

echo "✅ RabbitMQ and Nginx are running!"
echo ""
echo "📋 Next steps:"
echo "1. Install Python dependencies for each service:"
echo "   cd user_service && pip install -r requirements.txt"
echo "   cd account_service && pip install -r requirements.txt"
echo "   cd transaction_service && pip install -r requirements.txt"
echo "   cd notification_service && pip install -r requirements.txt"
echo ""
echo "2. Start the microservices:"
echo "   cd user_service && python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload"
echo "   cd account_service && python -m uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload"
echo "   cd transaction_service && python -m uvicorn app.main:app --host 0.0.0.0 --port 8003 --reload"
echo "   cd notification_service && python -m uvicorn app.main:app --host 0.0.0.0 --port 8004 --reload"
echo ""
echo "3. Start the frontend:"
echo "   cd frontend && npm start"
echo ""
echo "🌐 Access points:"
echo "   Frontend: http://localhost:3000"
echo "   API Gateway: http://localhost/api/users"
echo "   RabbitMQ Management: http://localhost:15672 (admin/admin123)"
echo ""
echo "🎉 Setup complete!"
