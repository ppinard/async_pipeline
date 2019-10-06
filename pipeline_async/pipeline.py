""""""

__all__ = ['Pipeline']

# Standard library modules.
import asyncio

# Third party modules.
from loguru import logger
import tqdm

# Local modules.

# Globals and constants variables.

class Pipeline:

    def __init__(self, tasks, stop_on_failure=False):
        self.tasks = tuple(tasks)
        self.stop_on_failure = stop_on_failure

    async def run(self, progress=True):
        """
        Runs the *inputdata* through the pipeline.
        """
        success_tasks = []

        it = enumerate(self.tasks)
        if progress:
            it = tqdm.tqdm(it, total=len(self.tasks))

        for i, task in it:
            task_name = task.name
            if progress:
                it.set_description(task_name)

            logger.debug('Running task #{}: {}', i, task_name)

            # Run task.
            try:
                success = await task.run(progress=progress)
            except:
                logger.exception('Task #{} failed: {}', i, task_name)
                success = False

                if self.stop_on_failure:
                    raise

            if success:
                success_tasks.append(task)
                logger.debug('Task #{} succeeded: {}', i, task_name)
            else:
                logger.debug('Task #{} skipped: {}', i, task_name)

        return success_tasks
