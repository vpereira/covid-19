# covid-19 dashboard (software and infrastructure)

This project was kind of a pet project to help a fellow scientist to setup
a flask application, pandas backed.

The idea was in a kind of bootcamp to talk about:

- Flask, Jinja2, and how to serve json
- Bootstrap 
- Jquery and SPA
- Python tests, classes
- Devops and how to deploy with docker and docker-compose


TODO:

 - plug the memcache to flask

```

+-------------+       +------------+         +--------------+     +--------------+
|             |       |            |         |              |     |              |
|    nginx    +-------+  gunicorn  +---------+  flask app   +-----+   memcache   |
|             |       |            |         |              |     |              |
+-------------+       +------------+         +--------------+     +--------------+

```

## Environments setup

please install `docker` and `docker-compose`.

## Quick start

### build and up

```sh
$ docker-compose build
$ docker-compose up -d
```
