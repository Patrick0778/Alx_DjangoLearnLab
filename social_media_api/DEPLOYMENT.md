# Deployment Guide for Social Media API

## Prerequisites

- Python 3.12+
- PostgreSQL database
- Heroku CLI (if deploying to Heroku)
- Git

## Local Setup for Production Testing

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create a `.env` file:

- Copy `.env.example` to `.env`
- Fill in your production values

3. Configure PostgreSQL:

- Create a database
- Update database credentials in `.env`

4. Collect static files:

```bash
python manage.py collectstatic --settings=social_media_api.settings_prod
```

5. Run migrations:

```bash
python manage.py migrate --settings=social_media_api.settings_prod
```

## Deploying to Heroku

1. Create a Heroku app:

```bash
heroku create your-app-name
```

2. Set environment variables:

```bash
heroku config:set DJANGO_SETTINGS_MODULE=social_media_api.settings_prod
heroku config:set DJANGO_SECRET_KEY=your_secret_key
heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
```

3. Add PostgreSQL:

```bash
heroku addons:create heroku-postgresql:hobby-dev
```

4. Deploy:

```bash
git push heroku main
```

5. Run migrations:

```bash
heroku run python manage.py migrate
```

## Production Checklist

- [ ] Set DEBUG=False in production settings
- [ ] Configure secure SSL/HTTPS
- [ ] Set up proper database backup
- [ ] Configure error logging
- [ ] Set up monitoring (e.g., Sentry)
- [ ] Configure proper CORS settings if needed
- [ ] Set up CI/CD pipeline

## Monitoring and Maintenance

1. Monitor application logs:

```bash
heroku logs --tail
```

2. Check application status:

```bash
heroku ps
```

3. Regular maintenance tasks:

- Update dependencies regularly
- Monitor database performance
- Review error logs
- Backup database regularly
- Update SSL certificates

## Troubleshooting

Common issues and solutions:

1. Static files not loading:

- Check STATIC_ROOT and STATIC_URL settings
- Run collectstatic again
- Verify whitenoise configuration

2. Database connection issues:

- Verify database credentials
- Check database URL configuration
- Ensure database service is running

3. 500 errors:

- Check error logs
- Verify environment variables
- Review recent changes

## Security Best Practices

1. Keep dependencies updated
2. Regularly rotate secret keys
3. Enable security middleware
4. Use HTTPS only
5. Implement rate limiting
6. Regular security audits
