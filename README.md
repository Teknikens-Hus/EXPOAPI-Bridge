# EXPOAPI-Bridge
Fetches booking from EXPO Bookings using their API and publishes the results using a webserver on port 8080.

## EXPO Bookings API
[EXPO BOOKING](https://www.expobooking.info/) uses GraphQL API to fetch bookings.
This project uses that API to fetch bookings and publish the results using a webserver on port 8080. This data can then be parsed locally by other services. Eg to display bookings in a calendar.

## How to run
Currently amd64 and x86_64 are supported with their each image.

Use the example docker-compose as a reference to run the project.
```yaml
version: '3.8'

services:
  expoapi-bridge:
    image: temp:latest
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
You can specify your *ENDPOINT* and *TOKEN* in an .env file in the same directory as the docker-compose file:
```bash
TOKEN: "Your token"
ENDPOINT: "https://yourbooking.endpoint.se/api/v2/graphql"
```
You can genrerate a token as an admin in the EXPO Booking admin panel by logging in to the admin panel then: System -> Administrators -> Your user -> Edit -> Access Tokens -> Pick a name and press create.

## Optional:
You can also specify how many days forward and backward you want to fetch bookings for. The default is 7 days forward and 0 days backward.
You can also specify a cron schedule for how often you want to fetch bookings. The default is every hour.

# Dependencies
The project uses:
 - [Supercronic](https://github.com/aptible/supercronic) for cron scheduling inside the container.
 - Python to get the data and run the web server.
 - Docker and docker-compose to run the project.