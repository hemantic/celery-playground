from celery import Celery, chain, group, chord
import os
import logging


logger = logging.getLogger(__name__)


celery = Celery(__name__, backend=os.getenv("DATABASE_URL"), broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"))


@celery.task()
def single_first(param: list) -> list:
    """
    Example task to be invoked in chain.
    """
    logger.info("Task first started")
    logger.info(f"Param is {param}")

    param.append("Single first task finished")

    return param


@celery.task()
def single_second(param: list) -> list:
    """
    Example task to be invoked in chain.
    """
    logger.info("Task second started")
    logger.info(f"Param is {param}")

    param.append("Single second task finished")

    return param


@celery.task()
def single_third(param: list) -> list:
    """
    Example task to be invoked in chain.
    """
    logger.info("Task third started")
    logger.info(f"Param is {param}")

    param.append("Single third task finished")

    return param


@celery.task()
def parallel_first(param: list) -> list:
    """
    Example task to be invoked in group or chord.
    """
    logger.info("Parallel first started")
    logger.info(f"Param is {param}")

    param.append("Parallel first task finished")

    return param


@celery.task()
def parallel_second(param: list) -> list:
    """
    Example task to be invoked in group or chord.
    """
    logger.info("Parallel second started")
    logger.info(f"Param is {param}")

    param.append("Parallel second task finished")

    return param


@celery.task()
def parallel_third(param: list) -> list:
    """
    Example task to be invoked in group or chord.
    """
    logger.info("Parallel third started")
    logger.info(f"Param is {param}")

    param.append("Parallel third task finished")

    return param


@celery.task()
def sum_all(tasks: list) -> int:
    """
    Reduce task to be invoked as a callback after group or chord. Gets the number of previously executed tasks.
    """
    return len(tasks)


@celery.task()
def wrapper(result):
    """
    LOL IDK
    """
    return result


@celery.task()
def prepared_simple_chain(param: list):
    """
    Simple chain. Needs to be converted to signature outside.
    """
    return chain(
        single_first.s(param),
        single_second.s(),
        single_third.s(),
    )


@celery.task()
def prepared_chain_with_group_in_the_end(param: list):
    """
    Chain with group in the end. Should be automatically converted to chord according to Celery docs. Seems like can't
    be converted to signature.
    """
    return chain(
        single_first.s(param),
        single_second.s(),
        prepared_group.s(),
    )


@celery.task()
def prepared_group(param):
    """
    Simple group with 3 parallel tasks.
    """
    return group(
        parallel_first.s(param),
        parallel_second.s(param),
        parallel_third.s(param),
    )


def prepared_task_list(param: list) -> list:
    """
    An example list of 3 separate parallel tasks, can be used in group or chord.
    """
    return [
        parallel_first.s(param),
        parallel_second.s(param),
        parallel_third.s(param),
    ]


@celery.task()
def prepared_chord(param: list):
    """
    Fully prepared chord with 3 parallel tasks and a callback.
    """
    return chord([
        parallel_first.s(param),
        parallel_second.s(param),
        parallel_third.s(param),
    ])(sum_all.s())


@celery.task()
def prepared_chord_with_group_as_body(param: list):
    """
    Chord prepared another way.
    """
    return chord(prepared_task_list(param))(sum_all.s())


@celery.task()
def chain_list_and_chord(param: list):
    """
    All the magic starts here. Russkoe pole experimentov.
    """
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
