
import time
import threading
import logging
import asyncio

from floodgateio.configurations.client_config_async import ClientConfigAsync

logger = logging.getLogger('floodgateio')


class ClientConfigWithAutoUpdateAsync(ClientConfigAsync):
    
    refresh_interval_seconds = 60

    async def initialize_config_async(self, http_resource_fetcher):
        await super(ClientConfigWithAutoUpdateAsync, self).initialize_config_async(http_resource_fetcher)

        loop = asyncio.get_event_loop()
        loop.create_task(self.autorefresh_loop())
        
    async def autorefresh_loop(self):
        logging.info("Starting auto-refresh of feature flags every {} seconds".format(self.refresh_interval_seconds))
        while True:
            await asyncio.sleep(self.refresh_interval_seconds)
            try:
                await self.load_data_async()
            except (KeyboardInterrupt, SystemExit):  # pylint: disable=try-except-raise
                raise
            except Exception as e:  # pylint: disable=broad-except
                logger.error("Faild to load data [{0}] {1}".format(e.__class__.__name__, e))
