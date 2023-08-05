
import time
import threading
import logging

from floodgateio.configurations.client_config_sync import ClientConfigSync

logger = logging.getLogger('floodgateio')


class ClientConfigWithAutoUpdate(ClientConfigSync):
    
    thread = None
    refresh_interval_seconds = 60

    def initialize_config(self, http_resource_fetcher):
        super(ClientConfigWithAutoUpdate, self).initialize_config(http_resource_fetcher)

        self.thread = threading.Thread(target=self.autorefresh_worker, daemon=True, name=__name__)
        self.thread.start()

    def autorefresh_worker(self):
        logging.info("Starting auto-refresh of feature flags every {} seconds".format(self.refresh_interval_seconds))
        while True:
            time.sleep(self.refresh_interval_seconds)
            try:
                self.load_data()
            except (KeyboardInterrupt, SystemExit):  # pylint: disable=try-except-raise
                raise
            except Exception as e:  # pylint: disable=broad-except
                logger.error("Faild to load data [{0}] {1}".format(e.__class__.__name__, e))
