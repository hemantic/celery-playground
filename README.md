# Celery tasks and primitives playground

This repo is a playground for testing different configurations of [Celery](https://docs.celeryq.dev/) tasks and [Celery primitives](https://docs.celeryq.dev/en/stable/userguide/canvas.html) (groups, chains,
chords, etc). 

## What's inside

This repo is shipped with:

* A number of tasks and primitives examples which can be rearranged in different ways (`src/tasks.py`)
* Dockerfile for dockerizing app
* Docker compose for running the whole infra (python, redis, postgresql, flower)

## Installation

`docker compose build` -> `docker compose up`

## Usage

After starting docker you can log in to worker container by `docker compose exec worker bash` and run `python3 run.py`
to start example tasks chain. If you want to run another task or reassamble tasks chains, feel free to modify 
`src/tasks.py` and import new chain/task to `src/run.py`.

You can then watch and troubleshoot your tasks in Flower (`http://localhost:5555`) – it is also shipped by Docker.

Generally every task receives a list with names of previousely executed tasks, adds its name to this list and returns
updated list as a result. So you can track task execution sequency in results fields of tasks in Flower.

## Notes

* In order to use [chord](https://docs.celeryq.dev/en/stable/userguide/canvas.html#chords) primitive, Celery result backend is required
* `chord` primitive generates a `celery.chord_unlock` task every second and it can be confusing at first. These tasks
  are generated even if `chord` primitive is not invoked directly
* It seems like `chord` primitive can't be converted to signature and must always be at the end of the chain (or be
  invoked as a separate task). I was unable to run any task after `chord` in any way (including task links).
