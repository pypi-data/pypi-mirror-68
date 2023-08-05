
from typing import Any, Tuple, Optional
import logging
from floodgateio.version import __version__

logger = logging.getLogger('floodgateio')


class HttpResourceFetcher:

    @staticmethod
    def build_headers(etag):
        headers = {
            'X-FloodGate-SDK-Agent': 'floodgateio-python',
            'X-FloodGate-SDK-Version': __version__,
        }
        if etag:
            headers['ETag'] = etag
        return headers

    @staticmethod
    def process_response(url, status_code, result_text, result_etag):
        result = None
        logger.info("Fetched flags {0} HTTP {1} ({2} bytes)".format(
            url, status_code, len(result_text or '')))

        if status_code == 304:  # not modified
            logger.info("CDN is not modified")
         
        elif status_code == 404:  # not found
            logger.info("Check your SDK Key")

        elif 200 <= status_code < 300:
            result = result_text
            logger.info("ETag = {}".format(result_etag))

        else:
            logger.error("Received unsuccessful response HTTP {0} from {1} {2}".format(
                status_code, url, result))

        return result, result_etag
