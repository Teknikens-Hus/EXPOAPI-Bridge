# Using Kubernetes deployment manifest
Use the provided example [deployment manifests](./expoapi-bridge-deployment/) as a starting point:

# [Deployment](./expoapi-bridge-deployment/deployment.yaml)
```yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: expoapi-bridge
  labels:
    app: expoapi-bridge
spec:
  replicas: 1
  strategy:
    type: RollingUpdate
  selector:
    matchLabels:
      app: expoapi-bridge
  template:
    metadata:
      labels:
        app: expoapi-bridge
    spec:
      containers:
        - image: ghcr.io/teknikens-hus/expoapi-bridge:latest
          name: expoapi-bridge
          ports:
            - name: webserver
              containerPort: 8080
          env:
            # This needs to be created separately, see README.md
            - name: TOKEN
              valueFrom:
                secretKeyRef:
                  name: expoapi-bridge
                  namespace: expoapi-bridge
                  key: token
            # This needs to be created separately, see README.md
            - name: ENDPOINT
              valueFrom:
                secretKeyRef:
                  name: expoapi-bridge
                  namespace: expoapi-bridge
                  key: endpoint
              # Fetch bookings 7 days forward
            - name: DAYS_FORWARD
              value: "7"
              # Default 0 days, only fetch today and forward
            - name: DAYS_BACKWARD
              value: "0"
              # Default to run every hour
            - name: CRON_SCHEDULE
              value: "0 * * * *"
              # Enable MQTT by setting this to true
            - name: MQTT_ENABLED
              value: "false"
              # Required if MQTT_ENABLED is true. Set to your broker IP
            - name: MQTT_HOST
              value: "0.0.0.0"
              # Default is 1883
            - name: MQTT_PORT
              value: "1883"
              # The base topic to publish to
            - name: MQTT_TOPIC
              value: "expoapi-bridge"
              # The username for authentication
            - name: MQTT_USERNAME
              valueFrom:
                secretKeyRef:
                  name: expoapi-bridge
                  namespace: expoapi-bridge
                  key: MQTT_USERNAME
              # The password for authentication
            - name: MQTT_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: expoapi-bridge
                  namespace: expoapi-bridge
                  key: MQTT_PASSWORD
              # Update to your timezone
            - name: TZ
              value: Europe/Stockholm
          # Adjust the resource limits as needed
          resources:
            requests:
              memory: "128Mi"
              cpu: "100m"
              ephemeral-storage: "200Mi"
            limits:
              memory: "256Mi"
              cpu: "200m"
              ephemeral-storage: "1Gi"
          # Make sure we run as non-root "app"
          securityContext:
            runAsUser: 1001
            runAsGroup: 2001
            fsGroup: 2001
```
## [Service](./expoapi-bridge-deployment/service.yaml)
This uses a LoadBalancer service type, you can change this to NodePort or ClusterIP if you are using a different setup.
```yaml
---
apiVersion: v1
kind: Service
metadata:
  name: expoapi-bridge
  labels:
    app: expoapi-bridge
spec:
  type: LoadBalancer
  loadBalancerIP: <your-ip>
  ports:
    - port: 8080
      targetPort: webserver
  selector:
    app: expoapi-bridge
```
## [Kustomization](./expoapi-bridge-deployment/kustomization.yaml)
```yaml
---
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
namespace: expoapi-bridge
metadata:
  name: kustomize-expoapi-bridge
resources:
- deployment.yaml
- service.yaml
- namespace.yaml
- secret.yaml
```

## [Namespace](./expoapi-bridge-deployment/namespace.yaml)
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: expoapi-bridge
```

## [Secret](./expoapi-bridge-deployment/secret.yaml)
Note: If you are using CD for kubernetes like [FluxCD](https://fluxcd.io/) you should add the secret using kubectl instead of applying the secret manifest file. This is to avoid storing sensitive data in git.
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: expoapi-bridge
type: Opaque
data:
  token: <base64-encoded-token>
  endpoint: <base64-encoded-endpoint>
```
Or if you are using MQTT:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: expoapi-bridge
type: Opaque
data:
  token: <base64-encoded-token>
  endpoint: <base64-encoded-endpoint>
  MQTT_USERNAME: <base64-encoded-mqtt-username>
  MQTT_PASSWORD: <base64-encoded-mqtt-password>
```

To apply the secret using kubectl:
```bash
kubectl create secret generic expoapi-bridge --namespace=expoapi-bridge --from-literal=token=<token> --from-literal=endpoint=<endpoint>
```
or if you are using MQTT:
```bash
kubectl create secret generic expoapi-bridge --namespace=expoapi-bridge --from-literal=token=<token> --from-literal=endpoint=<endpoint> --from-literal=MQTT_USERNAME=<mqtt-username> --from-literal=MQTT_PASSWORD=<mqtt-password>
```

**NOTE:** Also remove the secret.yaml from the kustomization.yaml file if you are using kubectl to create the secret.

## How to get a token:
You can generate a token as an admin in the EXPO Booking admin panel by logging in to the admin panel then: System -> Administrators -> Your user -> Edit -> Access Tokens -> Pick a name and press create.

## Optional environment variables:
- DAYS_FORWARD: The number of days forward you want to fetch bookings for. Default is 7.
- DAYS_BACKWARD: The number of days backward you want to fetch bookings for. Default is 0.
- CRON_SCHEDULE: The cron schedule for how often you want to fetch bookings. Default is every hour.
- TZ: The timezone you want to use. Default is Europe/Stockholm.
- MQTT_PORT: The port you want to use for MQTT. Default is 1883.
- MQTT_TOPIC: The topic you want to publish to. Default is "expoapi-bridge".