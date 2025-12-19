# Monitoring Setup Guide

This directory contains all monitoring-related configurations for the microservices banking app.

## 📁 Files

- `setup-prometheus-scraping.sh` - Configures Prometheus to scrape our services
- `access-monitoring.sh` - Helper script to access Prometheus and Grafana UIs
- `prometheus-scrape-config.yaml` - Manual scrape configuration (reference)
- `README.md` - This file

## 🚀 Quick Start

### Step 1: Configure Prometheus Scraping

Run the setup script to configure Prometheus to scrape all 4 microservices:

```bash
cd k8s/monitoring
chmod +x setup-prometheus-scraping.sh
./setup-prometheus-scraping.sh
```

This script will:
- Backup the current Prometheus config
- Add scrape configs for all 4 services
- Restart Prometheus to apply changes

### Step 2: Verify Prometheus is Scraping

```bash
# Port forward to Prometheus
kubectl port-forward -n monitoring svc/prometheus-server 9090:80

# Visit http://localhost:9090/targets in your browser
# You should see 4 services (user, account, transaction, notification) with state "UP"
```

### Step 3: Access Grafana

```bash
# Port forward to Grafana
kubectl port-forward -n monitoring svc/grafana 3000:80

# Visit http://localhost:3000
# Login: admin / admin
```

### Step 4: Configure Grafana Data Source

1. Go to Configuration > Data Sources
2. Click "Add data source"
3. Select "Prometheus"
4. Set URL: `http://prometheus-server.monitoring.svc.cluster.local:80`
5. Click "Save & Test"

### Step 5: Import Dashboards

Import pre-built dashboards or create custom ones to visualize:
- Request rates
- Response times
- Error rates
- Resource usage (CPU, memory)

## 📊 Prometheus Queries

Example queries to try in Prometheus:

```promql
# Total HTTP requests by service
http_requests_total

# Request rate (requests per second)
rate(http_requests_total[5m])

# Average request duration
rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m])

# Requests by status code
http_requests_total{status="2xx"}
http_requests_total{status="4xx"}
http_requests_total{status="5xx"}
```

## 🔍 Troubleshooting

### Prometheus not scraping services

Check if services are reachable:
```bash
kubectl exec -n monitoring deployment/prometheus-server -- wget -O- http://user-service.microservices.svc.cluster.local:8001/metrics
```

### Check Prometheus logs
```bash
kubectl logs -n monitoring deployment/prometheus-server -c prometheus-server
```

### Check Grafana logs
```bash
kubectl logs -n monitoring deployment/grafana
```

## 📚 Next Steps

1. Create custom Grafana dashboards
2. Set up alerting rules in Prometheus
3. Configure alert notifications (email, Slack, etc.)
4. Add business metrics dashboards (transactions, accounts, etc.)