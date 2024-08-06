# Use an official Alpine runtime as a parent image
FROM alpine:latest

USER root

# Install dependencies
RUN apk update \
    && apk upgrade \
    && apk --no-cache add libcap python3 py3-pip tzdata curl dos2unix

# Determine the architecture and set the appropriate URL and SHA1SUM
RUN ARCH=$(uname -m) && \
    if [ "$ARCH" = "x86_64" ]; then \
        SUPERCRONIC_URL=https://github.com/aptible/supercronic/releases/download/v0.2.30/supercronic-linux-amd64; \
        SUPERCRONIC_SHA1SUM=9f27ad28c5c57cd133325b2a66bba69ba2235799; \
        SUPERCRONIC=supercronic-linux-amd64; \
    elif [ "$ARCH" = "aarch64" ]; then \
        SUPERCRONIC_URL=https://github.com/aptible/supercronic/releases/download/v0.2.30/supercronic-linux-arm64; \
        SUPERCRONIC_SHA1SUM=d5e02aa760b3d434bc7b991777aa89ef4a503e49; \
        SUPERCRONIC=supercronic-linux-arm64; \
    else \
        echo "Unsupported architecture: $ARCH"; exit 1; \
    fi && \
    curl -fsSLO "$SUPERCRONIC_URL" && \
    echo "${SUPERCRONIC_SHA1SUM} ${SUPERCRONIC}" | sha1sum -c - && \
    chmod +x "$SUPERCRONIC" && \
    mv "${SUPERCRONIC}" /usr/local/bin/supercronic

ENV supercronic /usr/local/bin/supercronic

# Install Python dependencies
RUN python3 -m venv /home/app/expoapi-bridge/venv \
&& . /home/app/expoapi-bridge/venv/bin/activate \
&& pip install --upgrade pip \
&& pip install requests \
&& pip install PyYAML \
&& pip install paho-mqtt==2.1

# Add local user so we don't run as root
RUN addgroup -g 2001 app \
    && adduser -u 1001 -G app -D app

# Create the program directory
RUN mkdir -p /home/app/expoapi-bridge

# Copy the program files
COPY --chown=app:app ./expoapi-bridge /home/app/expoapi-bridge

# Run dos2unix to fix windows line endings issue with entrypoint not being found
RUN dos2unix /home/app/expoapi-bridge/entrypoint.sh

# Set permissions for the user's home directory and crond
RUN chown app:app /home/app/expoapi-bridge

# Make the entrypoint script executable
RUN chmod +x /home/app/expoapi-bridge/entrypoint.sh

# Set the user and working directory
USER app
WORKDIR /home/app/expoapi-bridge

# Expose port 8080 for the web server
EXPOSE 8080

# Command to update the crontab, start cron and the web server
ENTRYPOINT ["/home/app/expoapi-bridge/entrypoint.sh"]
#ENTRYPOINT ["tail", "-f", "/dev/null"]