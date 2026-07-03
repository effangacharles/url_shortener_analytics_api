# URL Shortener API

A Django-based URL shortening service with a REST API and basic click analytics. It allows users to create short links, redirect them to their original destinations, and view simple traffic statistics.

## Features

- Create short URLs from long URLs
- Redirect short links to their original destinations
- Track basic click analytics by browser, device, and referrer
- Expose API endpoints for URL creation and analytics
- Provide Swagger/OpenAPI documentation

## Tech Stack

- Django
- Django REST Framework
- SQLite

## Project Structure

- shortener/: URL creation, shortening logic, and redirect handling
- analytics/: Click analytics storage and reporting
- url_shortener/: Django project settings and root URL configuration

## Installation

1. Clone the repository
2. Create and activate a virtual environment
   ```bash
   python -m venv env
   env\Scripts\activate
   ```
3. Install dependencies
   ```bash
   pip install django, djangorestframework ,drf-yasg
   ```
4. Apply database migrations
   ```bash
   python manage.py migrate
   ```
5. Start the development server
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Create a short URL

- Method: POST
- Endpoint: /shortener/create_urls/
- Example request:
  ```json
  {
    "long_url": "https://google.com"
  }
  ```

- Example response:
  ```json
  {
    "id": 1,
    "long_url": "https://google.com",
    "short_code": "abc123",
    "short_url": "http://127.0.0.1:8000/abc123/",
    "created_at": "2026-07-04T00:00:00Z"
  }
  ```

### Redirect to a long URL

- Method: GET
- Endpoint: /<short_code>/

### Get analytics for a short URL

- Method: GET
- Endpoint: /analytics/urls/<short_code>/


## Example Usage

1. Create a URL:
   ```bash
   curl -X POST http://127.0.0.1:8000/shortener/create_urls/ \
     -H "Content-Type: application/json" \
     -d '{"long_url": "https://example.com"}'
   ```
2. Use the returned short URL to redirect to the original destination.
3. View analytics using the analytics endpoint.

