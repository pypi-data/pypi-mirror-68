
import logging
from floodgateio.floodgate_client_async import FloodGateClientAsync

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

features = FloodGateClientAsync.initialize_from_key_autoupdate("2bd051da88585d91dd6eae445f6db915975d48d387d6205d2a52692dde75")


from aiohttp import web

async def handle(request):
    feature_flag = features.get_value("welcome-greeting-v3", False)
    if feature_flag:
        text = 'Hello, New World!'
    else:    
        text = 'Hello, World!'
    return web.Response(text=text)

app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/{name}', handle)])


if __name__ == '__main__':
    web.run_app(app, host='127.0.0.1', port=5000)
