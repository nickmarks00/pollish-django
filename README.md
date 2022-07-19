# Pollish
> Pollish is a social media app centred around polls and communities.
## Architecture
### Deployment
The Django server is currently deployed via Heroku, and uses a `PostgreSQL` instance as the application database. In future, we intend to migrate this across to Google Cloud Platform.
### Tools/Engines
The application uses:
- Celery to perform background tasks
- Locust to perform performance and scalability testing
- Gunicorn to serve the application remotely
