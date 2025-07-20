#!/bin/bash

set -e

echo "Applying Prometheus manifests..."
kubectl apply -f k8s/prometheus-deployment.yaml
kubectl apply -f k8s/prometheus-service.yaml

echo "Waiting for Prometheus pod to be ready..."
kubectl wait --for=condition=ready pod -l app=prometheus --timeout=120s

echo "Port-forwarding Prometheus to localhost:9090..."
kubectl port-forward service/prometheus 9090:9090