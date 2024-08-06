## Using Docker Compose
Use the provided example `docker-compose.yaml` file as a starting point:

```yaml
services:
  expoapi-bridge:
    image: ghcr.io/teknikens-hus/expoapi-bridge:latest
    ports:
      - "8080:8080"
    environment:
      TOKEN: ${TOKEN}
      ENDPOINT: ${ENDPOINT}
      DAYS_FORWARD: "7"
      DAYS_BACKWARD: "0"
      CRON_SCHEDULE: "0 * * * *"
      MQTT_ENABLED: "true"
      MQTT_HOST: ${MQTT_HOST}
      MQTT_PORT: ${MQTT_PORT}
      MQTT_USERNAME: ${MQTT_USERNAME}
      MQTT_PASSWORD: ${MQTT_PASSWORD}
      MQTT_TOPIC: "expoapi-bridge"
      TZ: "Europe/Stockholm"
    restart: unless-stopped
```
Minimal example:
```yaml
services:
  expoapi-bridge:
    image: ghcr.io/teknikens-hus/expoapi-bridge:latest
    ports:
      - "8080:8080"
    environment:
      TOKEN: ${TOKEN}
      ENDPOINT: ${ENDPOINT}
    restart: unless-stopped
```
Then run:
```bash
docker-compose up -d
```
## Using Docker command:
```bash
docker run -d \
  --name expoapi-bridge \
  -p 8080:8080 \
  -e TOKEN=${TOKEN} \
  -e ENDPOINT=${ENDPOINT} \
  -e DAYS_FORWARD="7" \
  -e DAYS_BACKWARD="0" \
  -e CRON_SCHEDULE="0 * * * *" \
  -e TZ="Europe/Stockholm" \
  --restart unless-stopped \
  ghcr.io/teknikens-hus/expoapi-bridge:latest
```
## MQTT
Enable MQTT by setting the `MQTT_ENABLED` environment variable to `true` and setting the required MQTT environment variables. The data is published to `${MQTT_TOPIC}/current_bookings`.

## Required
You can specify your *ENDPOINT* and *TOKEN* in an .env file in the same directory as the docker-compose file:
```bash
TOKEN: "Your token"
ENDPOINT: "https://yourbooking.endpoint.se/api/v2/graphql"
```
If you're using MQTT these are also required:
```bash
MQTT_HOST: "your-broker-ip"
MQTT_USERNAME: "your-username"
MQTT_PASSWORD: "your-password
```

These will then be referenced by the compose file.

## How to get a token:
You can generate a token as an admin in the EXPO Booking admin panel by logging in to the admin panel then: System -> Administrators -> Your user -> Edit -> Access Tokens -> Pick a name and press create.

## Optional environment variables:
- DAYS_FORWARD: The number of days forward you want to fetch bookings for. Default is 7.
- DAYS_BACKWARD: The number of days backward you want to fetch bookings for. Default is 0.
- CRON_SCHEDULE: The cron schedule for how often you want to fetch bookings. Default is every hour.
- TZ: The timezone you want to use. Default is Europe/Stockholm.
- MQTT_PORT: The port you want to use for MQTT. Default is 1883.
- MQTT_TOPIC: The topic you want to publish to. Default is "expoapi-bridge".
