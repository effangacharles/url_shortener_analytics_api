# URL Shortener & Analytics

A Django project that provides a REST API for shortening URLs, a redirect endpoint, and click analytics tracking. It Includes a lightweight demo UI and Swagger/OpenAPI docs for quick inspection.

## Key Features

- Create short URLs via a JSON API
- Redirect short codes to their original long URLs
- Track clicks (browser, device type, referrer)
- View aggregated analytics via API or demo pages

## Quick Setup

1. Create and activate a Python virtualenv
```bash
python -m venv env
env\Scripts\activate
```
2. Install required packages
```bash
pip install django djangorestframework ,drf-yasg
```
3. Apply migrations and run the server
```bash
python manage.py migrate
python manage.py runserver
```

Open the demo at: http://127.0.0.1:8000/

## Routes / Endpoints

- POST `/shortener/create_urls/` — Create a short URL (HTML input `{ "long_url": "https://..." }`).
- POST `/<short_code>/` — Redirect to the original URL and record a click.
- GET `/analytics/urls/<short_code>/` — Analytics JSON for a short code (total clicks, browser/device types, timestamp and referer breakdown).
- Demo pages:  (home: `/shortener/home/` for generating short links),  (full Analytics report `shortener/analytics-report/`), 
- Swagger UI: `/swagger/` — OpenAPI interactive documentaion
- Admin: `/admin/` — Django admin to inspect `URL` and `ClickAnalytics` records.

Request → Response Cycle (detailed)

1) Create URL (API)
- Client: POST `/shortener/create_urls/` with `{"long_url": "https://google.com"}`.
- `shortener.serializers.URLSerializer` validates the input and prepares the model data.
- `shortener.models.URL`: a `pre_save` signal (`auto_generate_short_code`) runs `shortener.utils.create_unique_slug()` to generate `short_code` if missing.
- On save, serializer returns JSON containing `short_code` and a `short_url` built from the request.

2) Redirect (user clicks short URL)
- Client: POST `/{short_code}/`.
- `shortener.views.URLRedirectView` finds the `URL` object (404 if not found), parses headers (`User-Agent`, `Referer`) to extract `browser`, `device_type`, and `referrer`.
- A `ClickAnalytics` record is created with this metadata and timestamp.
- View responds with a redirect (HTTP 302) to the `long_url`.

3) Analytics API
- `analytics.views.URLAnalyticsAPIView` aggregates `ClickAnalytics` rows for the given `short_code` and returns a JSON summary: `total_clicks`, `metrics` (browsers/devices), plus `short_code` and `long_url`.

4) Demo / Reports (HTML)
- Views `AnalyticsDashboardView` and `AnalyticsReportView` prepare context for templates (`templates/analytics_dashboard.html`, `templates/analytics_report.html`).
- The templates render aggregated `link_counts` (click totals per long URL), full click lists, and summary statistics. Static Files (CSS/JS) are in `static/`.

Models / Serializers / Views mapping

- Models:
  - `shortener.models.URL` — fields: `long_url`, `short_code`, `created_at`.
  - `analytics.models.ClickAnalytics` — fields: `url` (FK), `clicked_at`, `browser`, `device_type`, `referrer`.
- Serializer:
  - `shortener.serializers.URLSerializer` — validates `long_url` and provides `short_url` in responses.
- Views:
  - `shortener.views.URLCreateAPIView` — API endpoint creating `URL` instances.
  - `shortener.views.URLRedirectView` — looks up `URL`, logs `ClickAnalytics`, and redirects.
  - `analytics.views.URLAnalyticsAPIView` — returns aggregated analytics JSON.
  - `analytics.views.AnalyticsDashboardView` / `shortener.views.AnalyticsReportView` — render HTML dashboards.

Development notes

- Swagger UI assets are available in development when `DEBUG=True`. The OpenAPI config is in `url_shortener/urls.py` (edit `openapi.Info` there to change title/description/contact).
- Admin can be used to manually inspect or delete analytics data. The public demo deliberately does not expose a global "clear analytics" button.

Example curl
```bash
# create a short url
curl -X POST http://127.0.0.1:8000/shortener/create_urls/ \
  -H 'Content-Type: application/json' \
  -d '{"long_url":"https://google.com"}'

# hit the short URL (redirect)
curl -v http://127.0.0.1:8000/abc123/

# get analytics
curl http://127.0.0.1:8000/analytics/urls/abc123/
```


