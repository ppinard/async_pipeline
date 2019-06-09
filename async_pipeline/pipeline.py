""""""

# Standard library modules.
import asyncio
import itertools
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
            logger.debug('Running task "{}"', task.name)

            # Run task.
            try:
                list_outputdata = await loop.run_in_executor(self.executor, task.run, inputdata)
            except:
                logger.error('Task "{}" failed', task.name)
                raise

            logger.debug('Task "{}" succeeded with {} outputs', task.name, len(list_outputdata))

            # If no output, there is nothing left to do.
            if not list_outputdata:
                return []

            # Remaining tasks
            newtasks = tasks[i+1:]

            # If no remaining tasks, there is nothing left to do.
            if not newtasks:
                return list_outputdata

            # Run the remaining tasks.
            coroutines = [self._run(loop, newtasks, outputdata) for outputdata in list_outputdata]
            list_new_outputdata = await asyncio.gather(*coroutines)
            return list(itertools.chain.from_iterable(list_new_outputdata)) # Flatten

    async def run(self, inputdata):
        """
        Runs the *inputdata* through the pipeline.
        """
        loop = asyncio.get_running_loop()
        return await self._run(loop, self.tasks, inputdata)
