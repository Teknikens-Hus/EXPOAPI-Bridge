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
      TZ: "Europe/Stockholm"
    restart: unless-stopped
```
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

## Required
You can specify your *ENDPOINT* and *TOKEN* in an .env file in the same directory as the docker-compose file:
```bash
TOKEN: "Your token"
ENDPOINT: "https://yourbooking.endpoint.se/api/v2/graphql"
```
These will then be referenced by the compose file.

You can genrerate a token as an admin in the EXPO Booking admin panel by logging in to the admin panel then: System -> Administrators -> Your user -> Edit -> Access Tokens -> Pick a name and press create.

## Optional:
- DAYS_FORWARD: The number of days forward you want to fetch bookings for. Default is 7.
- DAYS_BACKWARD: The number of days backward you want to fetch bookings for. Default is 0.
- CRON_SCHEDULE: The cron schedule for how often you want to fetch bookings. Default is every hour.
