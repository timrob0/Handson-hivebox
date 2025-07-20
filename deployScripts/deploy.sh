#!/bin/bash

set -e

CLUSTER_NAME=kind

echo "Building Docker image..."
docker build -t hivebox:latest .

echo "Loading image into KIND cluster..."
kind load docker-image hivebox:latest --name $CLUSTER_NAME

echo "Applying Kubernetes manifests..."
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml 2>/dev/null || echo "No ingress.yaml found or applied."

echo "Forcing rollout restart to ensure new image is used..."
kubectl rollout restart deployment/hivebox-app

echo "Waiting for pod to be ready..."
kubectl wait --for=condition=ready pod -l app=hivebox --timeout=120s

echo "Port-forwarding service to localhost:8000..."
kubectl port-forward service/hivebox-service 8000:80