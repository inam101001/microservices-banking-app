#!/bin/bash

# ArgoCD Installation Script for Microservices Banking App
# This script installs ArgoCD and configures it for GitOps deployment

set -e

echo "🚀 Installing ArgoCD for Microservices Banking App"
echo "=================================================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Create ArgoCD namespace
echo -e "${BLUE}Step 1: Creating argocd namespace...${NC}"
kubectl create namespace argocd --dry-run=client -o yaml | kubectl apply -f -
echo -e "${GREEN}✓ Namespace created${NC}"
echo ""

# Step 2: Install ArgoCD
echo -e "${BLUE}Step 2: Installing ArgoCD...${NC}"
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
echo -e "${GREEN}✓ ArgoCD installed${NC}"
echo ""

# Step 3: Wait for ArgoCD to be ready
echo -e "${BLUE}Step 3: Waiting for ArgoCD pods to be ready...${NC}"
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=argocd-server -n argocd --timeout=300s
echo -e "${GREEN}✓ ArgoCD is ready${NC}"
echo ""

# Step 4: Get initial admin password
echo -e "${BLUE}Step 4: Retrieving initial admin password...${NC}"
ARGOCD_PASSWORD=$(kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d)
echo -e "${GREEN}✓ Password retrieved${NC}"
echo ""

# Step 5: Install ArgoCD CLI (optional but recommended)
echo -e "${BLUE}Step 5: Checking for ArgoCD CLI...${NC}"
if ! command -v argocd &> /dev/null; then
    echo -e "${YELLOW}ArgoCD CLI not found. Installing...${NC}"
    
    # Detect OS
    OS=$(uname -s | tr '[:upper:]' '[:lower:]')
    ARCH=$(uname -m)
    
    if [ "$ARCH" = "x86_64" ]; then
        ARCH="amd64"
    elif [ "$ARCH" = "aarch64" ]; then
        ARCH="arm64"
    fi
    
    # Download and install
    curl -sSL -o /tmp/argocd https://github.com/argoproj/argo-cd/releases/latest/download/argocd-${OS}-${ARCH}
    sudo install -m 555 /tmp/argocd /usr/local/bin/argocd
    rm /tmp/argocd
    
    echo -e "${GREEN}✓ ArgoCD CLI installed${NC}"
else
    echo -e "${GREEN}✓ ArgoCD CLI already installed${NC}"
fi
echo ""

# Step 6: Configure port-forward (in background)
echo -e "${BLUE}Step 6: Setting up port forwarding...${NC}"
# Kill any existing port-forward
pkill -f "kubectl port-forward.*argocd-server" || true
sleep 2

# Start port-forward in background
nohup kubectl port-forward svc/argocd-server -n argocd 8080:443 > /tmp/argocd-port-forward.log 2>&1 &
PORTFORWARD_PID=$!
sleep 3

echo -e "${GREEN}✓ Port forwarding started (PID: $PORTFORWARD_PID)${NC}"
echo ""

# Step 7: Login to ArgoCD CLI
echo -e "${BLUE}Step 7: Logging in to ArgoCD CLI...${NC}"
argocd login localhost:8080 --username admin --password "$ARGOCD_PASSWORD" --insecure
echo -e "${GREEN}✓ Logged in to ArgoCD CLI${NC}"
echo ""

# Step 8: Display access information
echo ""
echo "=================================================="
echo -e "${GREEN}✓ ArgoCD Installation Complete!${NC}"
echo "=================================================="
echo ""
echo -e "${BLUE}Access Information:${NC}"
echo "  URL:      https://localhost:8080"
echo "  Username: admin"
echo "  Password: $ARGOCD_PASSWORD"
echo ""
echo -e "${YELLOW}⚠️  Save this password! The secret will be deleted after first login.${NC}"
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo "  1. Open https://localhost:8080 in your browser"
echo "  2. Login with the credentials above"
echo "  3. Apply ArgoCD application manifests:"
echo "     kubectl apply -f argocd/applications/"
echo ""
echo -e "${BLUE}Useful Commands:${NC}"
echo "  # List all applications"
echo "  argocd app list"
echo ""
echo "  # Get application status"
echo "  argocd app get <app-name>"
echo ""
echo "  # Sync application manually"
echo "  argocd app sync <app-name>"
echo ""
echo "  # View application logs"
echo "  argocd app logs <app-name>"
echo ""
echo "  # Stop port forwarding"
echo "  pkill -f 'kubectl port-forward.*argocd-server'"
echo ""
echo "=================================================="

# Save password to file for later reference
echo "$ARGOCD_PASSWORD" > /tmp/argocd-initial-password.txt
chmod 600 /tmp/argocd-initial-password.txt
echo -e "${BLUE}Password also saved to: /tmp/argocd-initial-password.txt${NC}"
echo ""