from celery import Celery, chain, group, chord
import os
import logging


logger = logging.getLogger(__name__)


celery = Celery(__name__, backend=os.getenv("DATABASE_URL"), broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"))


@celery.task()
def single_first(param: list):
    logger.info("Task first started")
    logger.info(f"Param is {param}")

    param.append("Single first task finished")

    return param


@celery.task()
def single_second(param: list):
    logger.info("Task second started")
    logger.info(f"Param is {param}")

    param.append("Single second task finished")

    return param


@celery.task()
def single_third(param: list):
    logger.info("Task third started")
    logger.info(f"Param is {param}")

    param.append("Single third task finished")

    return param


@celery.task()
def parallel_first(param: list):
    logger.info("Parallel first started")
    logger.info(f"Param is {param}")

    param.append("Parallel first task finished")

    return param


@celery.task()
def parallel_second(param: list):
    logger.info("Parallel second started")
    logger.info(f"Param is {param}")

    param.append("Parallel second task finished")

    return param


@celery.task()
def parallel_third(param: list):
    logger.info("Parallel third started")
    logger.info(f"Param is {param}")

    param.append("Parallel third task finished")

    return param


@celery.task()
def sum_all(tasks):
    return len(tasks)


@celery.task()
def wrapper(result):
    return result


@celery.task()
def prepared_simple_chain(param):
    return chain(
        single_first.s(param),
        single_second.s(),
        single_third.s(),
    )


@celery.task()
def prepared_chain_with_group_in_the_end(param):
    return chain(
        single_first.s(param),
        single_second.s(),
        prepared_group.s(),
    )


@celery.task()
def prepared_group(param):
    return group(
        parallel_first.s(param),
        parallel_second.s(param),
        parallel_third.s(param),
    )


def prepared_task_list(param):
    return [
        parallel_first.s(param),
        parallel_second.s(param),
        parallel_third.s(param),
    ]


@celery.task()
def prepared_chord(param):
    return chord([
        parallel_first.s(param),
        parallel_second.s(param),
        parallel_third.s(param),
    ])(sum_all.s())


@celery.task()
def prepared_chord_with_group_as_body(param):
    return chord(prepared_task_list(param))(sum_all.s())


@celery.task()
def chain_list_and_chord(param):
    return chain(
        single_first.s(param),
        single_second.s(),
        single_third.s(),
        # prepared_group.s().link(sum_all.s()),
        prepared_chord.s(),
        # chord([
        #     parallel_first.s(),
        #     parallel_second.s(),
        #     parallel_third.s(),
        # ])(sum_all.s()).s()
    )
