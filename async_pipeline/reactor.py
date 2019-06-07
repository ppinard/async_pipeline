""""""

# Standard library modules.
import asyncio
from concurrent.futures.thread import ThreadPoolExecutor

# Third party modules.
from loguru import logger

# Local modules.

# Globals and constants variables.

class Reactor:

    def __init__(self, reactions, max_workers=1):
        self.reactions = tuple(reactions)
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    async def _process(self, loop, reactions, reagent):
        for i, reaction in enumerate(reactions):
            logger.info('Running reaction {}', reaction.name)

            products = await loop.run_in_executor(self.executor, reaction.process, reagent)
            logger.info('Reaction {} created {} products', reaction.name, len(products))

            if not products:
                return []

            newreactions = reactions[i+1:]
            if not newreactions:
                return products

            for product in products:
                return await self._process(loop, newreactions, product)

    async def process(self, reagent):
        loop = asyncio.get_running_loop()
        return await self._process(loop, self.reactions, reagent)