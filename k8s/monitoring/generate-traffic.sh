#!/bin/bash

# Script to generate traffic to our microservices
# This will create metrics data for Grafana dashboards

echo "🚀 Generating traffic to microservices..."
echo "This will create users, accounts, and transactions"
echo ""

BASE_URL="http://microbank.local"

# Function to make requests
make_request() {
    local method=$1
    local endpoint=$2
    local data=$3
    
    if [ "$method" = "POST" ]; then
        curl -s -X POST "$BASE_URL$endpoint" \
            -H "Content-Type: application/json" \
            -d "$data" > /dev/null
    else
        curl -s "$BASE_URL$endpoint" > /dev/null
    fi
}

echo "📊 Creating sample data..."

# Create users
for i in {1..5}; do
    echo "Creating user $i..."
    make_request POST "/api/users" '{
        "name": "User'$i'",
        "email": "user'$i'@example.com"
    }'
done

echo ""
echo "💰 Creating accounts..."

# Create accounts
for i in {1..5}; do
    echo "Creating account for user $i..."
    make_request POST "/api/accounts" '{
        "user_id": '$i',
        "account_type": "checking",
        "balance": 1000.00
    }'
done

echo ""
echo "💸 Creating transactions..."

# Create transactions
for i in {1..10}; do
    echo "Creating transaction $i..."
    
    # Random transaction type
    types=("deposit" "withdraw" "deposit" "withdraw" "deposit")
    type=${types[$RANDOM % ${#types[@]}]}
    amount=$((RANDOM % 100 + 10))
    account_id=$((RANDOM % 5 + 1))
    
    make_request POST "/api/transactions" '{
        "account_id": '$account_id',
        "type": "'$type'",
        "amount": '$amount'.00
    }'
    
    sleep 0.5
done

echo ""
echo "🔄 Generating continuous traffic..."
echo "Press Ctrl+C to stop"
echo ""

# Continuous traffic generation
counter=1
while true; do
    echo "Request batch $counter..."
    
    # GET requests to all services
    curl -s http://microbank.local/api/users > /dev/null &
    curl -s http://microbank.local/api/accounts > /dev/null &
    curl -s http://microbank.local/api/transactions > /dev/null &
    curl -s http://microbank.local/api/notifications > /dev/null &
    
    # Random individual resource
    user_id=$((RANDOM % 5 + 1))
    curl -s http://microbank.local/api/users/$user_id > /dev/null &
    
    account_id=$((RANDOM % 5 + 1))
    curl -s http://microbank.local/api/accounts/$account_id > /dev/null &
    
    # Occasional transaction
    if [ $((counter % 3)) -eq 0 ]; then
        amount=$((RANDOM % 50 + 10))
        account_id=$((RANDOM % 5 + 1))
        curl -s -X POST http://microbank.local/api/transactions \
            -H "Content-Type: application/json" \
            -d '{
                "account_id": '$account_id',
                "type": "deposit",
                "amount": '$amount'.00
            }' > /dev/null &
    fi
    
    counter=$((counter + 1))
    sleep 2
done