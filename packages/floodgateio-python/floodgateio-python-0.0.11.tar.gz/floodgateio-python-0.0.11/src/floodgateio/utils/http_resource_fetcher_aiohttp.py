
from typing import Any, Tuple, Optional
import logging
import aiohttp
from floodgateio.version import __version__
from floodgateio.utils.http_resource_fetcher import HttpResourceFetcher

logger = logging.getLogger('floodgateio')


class HttpResourceFetcherAioHttp(HttpResourceFetcher):

    async def fetch_async(self, url, sdk_key, etag=None):  # pylint: disable=unused-argument,no-self-use        
        status_code = None
        result_etag = None
        result_text = None
        headers = HttpResourceFetcherAioHttp.build_headers(etag)

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                status_code = response.status
                result_etag = response.headers.get('etag')
                result_text = await response.text()
        
        result, result_etag = HttpResourceFetcherAioHttp.process_response(url, status_code, result_text, result_etag)             
        return result, result_etag
