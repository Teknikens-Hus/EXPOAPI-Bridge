# EXPOAPI-Bridge
Fetches booking from EXPO Bookings using their API and publishes the results using a webserver on port 8080.

## EXPO Bookings API
[EXPO BOOKING](https://www.expobooking.info/) uses GraphQL API to fetch bookings.
This project uses that API to fetch bookings and publish the results using a webserver on port 8080. This data can then be parsed locally by other services. Eg to display bookings in a calendar.

## How to run
Currently amd64 and x86_64 are supported with their each image.

Docker / docker-compose
[See Docker example](https://github.com/Teknikens-Hus/EXPOAPI-Bridge/blob/main/Examples/Docker/README.md)


# Dependencies
The project uses:
 - [Supercronic](https://github.com/aptible/supercronic) for cron scheduling inside the container.
 - Python to get the data and run the web server.
 - Docker and docker-compose to run the project.