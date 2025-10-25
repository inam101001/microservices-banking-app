@echo off
echo 🏦 Setting up Banking Microservices Application...

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed. Please install Docker first.
    exit /b 1
)

docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    exit /b 1
)

REM Start RabbitMQ and Nginx
echo 🐰 Starting RabbitMQ and Nginx...
docker-compose up -d

REM Wait for RabbitMQ to be ready
echo ⏳ Waiting for RabbitMQ to be ready...
timeout /t 10 /nobreak >nul

REM Check if RabbitMQ is running
docker ps | findstr banking_rabbitmq >nul
if %errorlevel% neq 0 (
    echo ❌ Failed to start RabbitMQ
    exit /b 1
)

echo ✅ RabbitMQ and Nginx are running!
echo.
echo 📋 Next steps:
echo 1. Install Python dependencies for each service:
echo    cd user_service ^&^& pip install -r requirements.txt
echo    cd account_service ^&^& pip install -r requirements.txt
echo    cd transaction_service ^&^& pip install -r requirements.txt
echo    cd notification_service ^&^& pip install -r requirements.txt
echo.
echo 2. Start the microservices:
echo    cd user_service ^&^& python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
echo    cd account_service ^&^& python -m uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload
echo    cd transaction_service ^&^& python -m uvicorn app.main:app --host 0.0.0.0 --port 8003 --reload
echo    cd notification_service ^&^& python -m uvicorn app.main:app --host 0.0.0.0 --port 8004 --reload
echo.
echo 3. Start the frontend:
echo    cd frontend ^&^& npm start
echo.
echo 🌐 Access points:
echo    Frontend: http://localhost:3000
echo    API Gateway: http://localhost/api/users
echo    RabbitMQ Management: http://localhost:15672 (admin/admin123)
echo.
echo 🎉 Setup complete!
pause
