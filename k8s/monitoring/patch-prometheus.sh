#!/bin/bash

# Simple script to manually add scrape configs to Prometheus
# This edits the ConfigMap directly

echo "🔧 Patching Prometheus to scrape microservices..."
echo ""

# Create a patch file
cat > /tmp/prometheus-patch.yaml << 'EOF'
data:
  prometheus.yml: |
    global:
      scrape_interval: 1m
      scrape_timeout: 10s
      evaluation_interval: 1m
    scrape_configs:
    - job_name: prometheus
      static_configs:
      - targets:
        - localhost:9090
    
    # Our microservices
    - job_name: 'user-service'
      static_configs:
      - targets: ['user-service.microservices.svc.cluster.local:8001']
        labels:
          service: 'user-service'
      metrics_path: '/metrics'
      scrape_interval: 15s

    - job_name: 'account-service'
      static_configs:
      - targets: ['account-service.microservices.svc.cluster.local:8002']
        labels:
          service: 'account-service'
      metrics_path: '/metrics'
      scrape_interval: 15s

    - job_name: 'transaction-service'
      static_configs:
      - targets: ['transaction-service.microservices.svc.cluster.local:8003']
        labels:
          service: 'transaction-service'
      metrics_path: '/metrics'
      scrape_interval: 15s

    - job_name: 'notification-service'
      static_configs:
      - targets: ['notification-service.microservices.svc.cluster.local:8004']
        labels:
          service: 'notification-service'
      metrics_path: '/metrics'
      scrape_interval: 15s
EOF

echo "📝 Applying patch to Prometheus ConfigMap..."
kubectl patch configmap prometheus-server -n monitoring --patch-file /tmp/prometheus-patch.yaml

echo ""
echo "♻️  Restarting Prometheus..."
kubectl delete pods -n monitoring -l app.kubernetes.io/name=prometheus,component=server

echo ""
echo "⏳ Waiting for Prometheus to restart..."
sleep 10
kubectl wait --for=condition=ready pod -n monitoring -l app.kubernetes.io/name=prometheus,component=server --timeout=120s

echo ""
echo "✅ Done! Prometheus is configured."
echo ""
echo "To verify, run:"
echo "  kubectl port-forward -n monitoring svc/prometheus-server 9090:80"
echo "  Then visit: http://localhost:9090/targets"