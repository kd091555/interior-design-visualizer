# Kubernetes deployment

Build and push the image, then replace the image in `app.yaml`. Create secrets
without committing them:

```bash
kubectl create secret generic interior-secrets \
  --from-literal=OPENAI_API_KEY='...' \
  --from-literal=APP_SECRET_KEY='...' \
  --from-literal=APP_USERNAME='admin' \
  --from-literal=APP_PASSWORD='...' \
  --from-literal=S3_ACCESS_KEY_ID='minioadmin' \
  --from-literal=S3_SECRET_ACCESS_KEY='...' \
  --from-literal=MINIO_ROOT_USER='minioadmin' \
  --from-literal=MINIO_ROOT_PASSWORD='...'
kubectl apply -k k8s
```

The included Redis and MinIO deployments are convenient single-node defaults,
not highly available production services. Replace them with managed or clustered
services when availability matters. Add an ingress appropriate to your cluster.
