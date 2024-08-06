# EXPOAPI-Bridge
Fetches booking from EXPO Bookings using their API and publishes the results using a webserver on port 8080.

## EXPO Bookings API
[EXPO BOOKING](https://www.expobooking.info/) uses GraphQL API to fetch bookings.
This project uses that API to fetch bookings and publish the results using a webserver on port 8080. This data can then be parsed locally by other services. Eg to display bookings in a calendar.

## Installation
Currently amd64 and arm64 are supported.

### Docker / docker-compose:
[![Docker Icon](https://skillicons.dev/icons?i=docker&theme=light)](./Examples/Docker/README.md)

### Kubernetes Deployment:
[![Kube Icon](https://skillicons.dev/icons?i=kubernetes&theme=light)](./Examples/Kubernetes/README.md)

# Dependencies
The project uses:
 - [Supercronic](https://github.com/aptible/supercronic) for cron scheduling inside the container.
 - Python to get the data and run the web server.
 - Docker and docker-compose to run the project.