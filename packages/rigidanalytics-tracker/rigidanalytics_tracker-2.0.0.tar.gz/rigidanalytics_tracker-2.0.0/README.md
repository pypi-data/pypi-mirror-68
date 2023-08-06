# Tracker

Tracker is a python package, that can be integrated into

- any django project as middleware;

- any flask project as extension.

It asynchronously intercepts requests and sends metric data to our
RigidAnalytics Backend (see
https://github.com/reustleco/rigidanalytics).

## Installation

### From PyPI

```
pip install rigidanalytics-tracker
```

### From git repository

```
git clone git@github.com:reustleco/rigidanalytics-tracker.git
cd rigidanalytics-tracker
pipenv install
pipenv shell
```

## Configuration

Below the following environment variables are in use: `RA_PROJECT_ID`,
`RA_PROJECT_TOKEN` and `RA_BACKEND_ENDPOINT`.

In order to get project ID and token you need to have access to the
admin pages on [RigidAnalytics
Backend](https://github.com/reustleco/rigidanalytics). `RA_BACKEND_ENDPOINT`
is the base URL to the Backend. If it is not provided then the default
URL (i.e. https://rigidanalytics.com) is used instead.

### Django integration

- Add `rigidanalytics_tracker.middleware.Analytics` middleware to the
`MIDDLEWARE` (after all django middlewares).

- Add the following dict that configures Tracker:

```
RIGID_ANALYTICS = {
    'PROJECT_ID': os.environ['RA_PROJECT_ID'],
    'PROJECT_TOKEN': os.environ['RA_PROJECT_TOKEN'],
    'DEBUG_DISABLE_ANALYTICS': False,
    'BACKEND_ENDPOINT': os.environ.get('RA_BACKEND_ENDPOINT', ''),
}
```

See [an example django integration](#test-django-integration) about
how everything configured there.

### Flask integration

```
from rigidanalytics_tracker.flask import Tracker

flask_app.config['RIGID_ANALYTICS'] = {
    'PROJECT_ID': os.environ['RA_PROJECT_ID'],
    'PROJECT_TOKEN': os.environ['RA_PROJECT_TOKEN'],
    'DEBUG_DISABLE_ANALYTICS': False,
    'BACKEND_ENDPOINT': os.environ.get('RA_BACKEND_ENDPOINT', ''),
}
tracker = Tracker()
tracker.init_app(flask_app)
```

See [an example flask integration](#test-flask-integration) about how
everything configured there.

## Automated tests

The automated tests are implemented by means of `tox`. In order to run
the tests execute the following command:

```
tox
```

## Test the tracker

Create an virtual environment:

```
cd tests/integrations/
pipenv install --dev
pipenv shell
```

Run event handler:

```
dotenv -f .env.example run ./event_handler.py
```

In the applications the tracker is configured to send the events to
the event handler. Once an event is captured it is printed to console.

### Test django integration

```
dotenv -f .env.example run ./django_app/manage.py migrate
dotenv -f .env.example run ./django_app/manage.py runserver
```

Open home page and then check console (with the event handler) for an
event.

### Test flask integration

```
dotenv -f .env.example run python ./flask_app/app.py
```

Open home page and then check console (with the event handler) for an
event.

### Test with the existing backend

Create `.env`:

```
cp .env.example .env
```

Get a project ID and project token from the existing RigidAnalytics
backend and put them into the `RA_PROJECT_ID` and `RA_PROJECT_TOKEN`
respectively. Put backend URL into the `RA_BACKEND_ENDPOINT`.

Start flask application:

```
dotenv run python ./flask_app/app.py
```

Open home page and then check backend admin for a new event.
