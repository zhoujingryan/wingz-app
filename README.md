# Wingz Ride API

## Overview
This is an assignment project for the Wingz Ride API.
It provides a RESTful Ride List API with simple JWT authentication.

## Tech Stack
- **Django** / **Django REST Framework** / **GeoDjango**
- **PostgreSQL** with **PostGIS** extension
- **djangorestframework-simplejwt** for simple JWT authentication
- **django-filter** for drf filtering
- **drf-yasg** for API documentation
- **django-pytest** / **pytest-cov**

## Development
### Requirements
- Python 3.10+
- Django 4.2

### Project Setup
Setup project virtual environment by using `venv`:
```bash
    python3 -m venv env
    source env/bin/activate
```
or `virtualenv`.
```bash
    pyenv virtualenv 3.10 ride-venv
    pyenv local ride-venv
```
Install both dev and test dependencies:
```bash
    pip install -r requirements-dev.txt
    pip install -r requirements-test.txt
```
Make sure you have a Postgres database instance with PostGIS extension up and running.
```bash
    docker run --name postgis -p 5432:5432 -e POSTGRES_PASSWORD=123456 -d postgis/postgis:16-3.4
```
GeoDjango also requires certain setup in development environment
Follow the instructions in the official documentation, see: [GeoDjango Installation](https://docs.djangoproject.com/en/5.1/ref/contrib/gis/install/)

Copy and update your local settings file of your project:
```bash
    cp wingz/settings/local.example.py wingz/settings/local.py
    export DJANGO_SETTINGS_MODULE=wingz.settings.local
```
Running development server:
```bash
    python manage.py runserver
```
Migrating database:
```bash
    python manage.py makemigrations   # create migration files
    python manage.py migrate          # apply migrations
```
Creating first admin user in your local environment:
```bash
    python manage.py runscript create_user --script-args admin@wingz.com admin123 admin
```
Initializing the database with some test data:
```bash
    # init 100 random users
    python manage.py runscript init_user_data --script-args 100
    # init 1000 random ride data
    python manage.py runscript init_ride_data --script-args 1000
```
You can now get user JWT access token:
```bash
    curl -X 'POST' \
      'http://127.0.0.1:8000/api/v1/sso/login/' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{
      "email": "admin@wingz.com",
      "password": "admin123"
      }'
```
And now we are done! You can use access token you got to Ride API.
```bash
    curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/riding/rides/?gps_location=1%2C20&ordering=distance_to_pickup&distance_within=20' \
  -H 'accept: application/json' \
  -H 'Authorization: JWT {Access-Token}'
```
### API Docs
When the server is up and running, you can access the API docs at `http://localhost:8000/api/docs/`

### Testing

You need `pytest` and `pytest-django`, then:

```bash
    make test         # run tests
    make cov          # run coverage tests
    make cov-html     # generate coverage report
```

### Code Style checking
Make sure to run tests and code style checks before submitting code.

```bash
    make style
```

Additionally, it is highly recommended to install `pre-commit` hooks when developing:
```bash
    pip install pre-commit
    pre-commit install
```
To manually run precommit hooks:
```bash
    make check
```

*Not recommended：`git commit --no-verify` will bypass the checks for this commit.*


### Dependency Management

Install `pip-tools`
```bash
    pip install pip-tools
```

Run:
```bash
    pip-compile                             # update requirements.txt
    pip-compile --upgrade                   # upgrade all packages
    pip-compile --upgrade-package django    # upgrade a pacakge
```

## Deploy


## Performance
After further consideration, I decided to use GeoDjango and PostGIS for managing our data:
GeoDjango is a Django extension that allows us to manage and query geographic data with ease.
PostGIS is a PostgreSQL extension which is very powerful when dealing with geographic data.

### Performance Optimizations:

1. minimize the number of queries in ride list api, the Ride List API consists of 3 queries:
   - DRF will first fetch the total count based on the filtering conditions.
   - Use `select_related` to fetch driver and rider data in the paginated Ride query.
   - Use `prefetch_related` to fetch ride events in the last 24 hours, Django ORM will fire another query based on the paginated ride results.
2. make sure the database indexes are properly set up:
   - We are dealing with geographic data, so we have to use GeoDjango and PostGIS in order to use spatial indexes.
   - `pickup_pos = PointField()` will automatically create a spatial index on the `pickup_pos` field.
   - For other ordering and filtering field, we should also create certain indexes by using `db_index=True`.
   - Use PostGIS `dwithin` query to narrow down the query range will speed up the query.

### Bonus
For reporting purposes, the raw SQL query statement is as follows:
```sql
   SELECT
       full_name,
       ride_date,
       COUNT(*) AS ride_count
   FROM (
       SELECT
           driver.id_user,
           CONCAT(driver.first_name, ' ', driver.last_name) AS full_name,
           TO_CHAR(dropoff.created_at, 'YYYY-MM') AS ride_date,
           (dropoff.created_at - pickup.created_at) AS ride_duration
       FROM
           riding_ride_event AS dropoff
       LEFT JOIN
           riding_ride AS ride ON dropoff.id_ride = ride.id_ride
       LEFT JOIN
           riding_ride_event AS pickup ON pickup.id_ride = ride.id_ride AND pickup.description = 'Status changed to pickup'
       LEFT JOIN
           sso_user AS driver ON driver.id_user = ride.id_driver
       WHERE
           dropoff.created_at >= '2024-01-01'
           AND dropoff.description = 'Status changed to dropoff'
   ) AS ride_data
   WHERE
       ride_duration > INTERVAL '1 hour'
   GROUP BY
       full_name, ride_date
   ORDER BY
       ride_date ASC;
```
The main idea of this query is to first use a subquery to filter out all rides that contain both pickup event and dropoff event.
And then group the results by driver and month, and count the number of rides per driver per month based on the subquery.

Example results:

| full_name      | ride_date | ride_count |
|:---------------| :---: | ---: |
| Aaron Lee      | 2024-01 | 6 |
| Aaron Ferguson | 2024-01 | 4 |
| Aaron Glover   | 2024-01 | 6 |
| Aaron Jones    | 2024-01 | 11 |
| Aaron Montes   | 2024-01 | 5 |

## Wrap up
Although this project is a small assignment project, but I still spend a lot of time on it, especially on testing the performance optimizing the queries. The
tech stacks and the workflow I used are also my goto choices in my everyday work. I hope this project can well demonstrate my skills and knowledge in Django
web development. Thank you for reading!
