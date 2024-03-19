from time import time

from fastapi.logger import logger


def timeit(method):
    async def timed(*args, **kw):
        time_start = time()
        result = await method(*args, **kw)
        time_end = time()

        execution_time = round((time_end - time_start) * 1000, 2)
        logger.info(f'Execution finished in {execution_time} ms')

        return result

    return timed
