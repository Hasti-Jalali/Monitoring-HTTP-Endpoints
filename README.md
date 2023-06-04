# HTTP Endpoint Monitoring Service

This project is a Python-based HTTP endpoint monitoring service that tracks the response status codes of specified URLs at customizable time intervals. It sends HTTP requests to the provided endpoints, records the response status codes, and generates alerts if the error threshold is exceeded.

## Features

- Configurable time intervals for monitoring (e.g., 30 seconds, 1 minute, 5 minutes)
- Tracks and records response status codes of HTTP endpoints
- Customizable error threshold for each URL
- Generates alerts when the error threshold is surpassed
- Differentiates between successful (2xx) and unsuccessful (non-2xx) HTTP calls
