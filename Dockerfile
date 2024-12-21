FROM python:3.11-slim

ARG PORT=5000
ARG BUILD_ID=unknown
ARG VERSION=unknown
ENV PORT=$PORT
ENV BUILD_ID=$BUILD_ID
ENV VERSION=$VERSION
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the source code to the container
COPY . .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Run the application
RUN chmod +x entrypoint.sh
EXPOSE $PORT
ENTRYPOINT ["/app/entrypoint.sh"]
