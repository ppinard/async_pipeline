""""""

# Standard library modules.
import asyncio
from concurrent.futures.thread import ThreadPoolExecutor

# Third party modules.
from loguru import logger

# Local modules.

# Globals and constants variables.

class Pipeline:

    def __init__(self, tasks, max_workers=1):
        self.tasks = tuple(tasks)
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    async def _run(self, loop, tasks, inputdata):
        for i, task in enumerate(tasks):
            logger.info('Running task "{}"', task.name)

            try:
                if asyncio.iscoroutinefunction(task.run):
                    list_outputdata = await task.run(inputdata)
                else:
                    list_outputdata = await loop.run_in_executor(self.executor, task.run, inputdata)
            except:
                logger.exception('Task "{}" failed', task.name)
                raise

            logger.info('Task "{}" succeeded with {} outputs', task.name, len(list_outputdata))

            if not list_outputdata:
                return []

            newtasks = tasks[i+1:]
            if not newtasks:
                return list_outputdata

            for outputdata in list_outputdata:
                return await self._run(loop, newtasks, outputdata)

    async def run(self, inputdata):
        loop = asyncio.get_running_loop()
        return await self._run(loop, self.tasks, inputdata)