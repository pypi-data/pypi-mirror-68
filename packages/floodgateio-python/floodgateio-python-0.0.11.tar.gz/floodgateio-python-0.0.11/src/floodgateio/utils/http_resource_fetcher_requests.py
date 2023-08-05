
from typing import Any, Tuple, Optional
import logging
import requests
from floodgateio.version import __version__
from floodgateio.utils.http_resource_fetcher import HttpResourceFetcher

logger = logging.getLogger('floodgateio')


class HttpResourceFetcherRequests(HttpResourceFetcher):

    def fetch(self, url, sdk_key, etag=None):  # pylint: disable=unused-argument,no-self-use
        # type: (str, str, str) -> Tuple[Optional[str], Optional[str]]
        result = None
        result_etag = None

        headers = HttpResourceFetcher.build_headers(etag)

        response = requests.get(url, headers=headers)
        status_code = response.status_code
        result_etag = response.headers.get('etag')
        result_text = response.text

        result, result_etag = HttpResourceFetcher.process_response(url, status_code, result_text, result_etag)
        return result, result_etag
