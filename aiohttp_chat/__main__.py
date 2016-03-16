import logging
import asyncio
import aioredis
import aiopg
from aiohttp import web, log
from collections import defaultdict

from aiohttp_chat import handlers

# POSTGRES DATABASE CONFIGURATION

db_config = {
    'database': 'chat',
    'user': 'django',
    'password': 'secr3t',
    'host': 'localhost'
}

# WebSockets CONTAINER (for room handling)

class BList(list):
    """
    [Broadcasting]list that broadcasts str messages for its embers.
    Exclusively for aiohttp WebSocketResponse instances.
    """
    def broadcast(self, message):
        log.ws_logger.info('Sending message to %d waiters', len(self))
        for waiter in self:
            try:
                waiter.send_str(message)
            except Exception:
                log.ws_logger.error('Error was happened during broadcasting: ',
                                    exc_info=True)


async def get_app():

    # Graceful shutdown actions

    async def close_redis(app):
        log.server_logger.info('Closing redis connection')
        app['redis'].close()


    async def close_db(app):
        log.server_logger.info('Closing postgres connection')
        app['db'].close()
        log.server_logger.info('Is postgres connection closed? {}'
                               .format(app['db'].closed))

    async def close_websockets(app):

        for channel in app['waiters'].values():
            for ws in channel:
                await ws.close(code=1000, message='Server shutdown')

    middlewares = []

    app = web.Application(middlewares=middlewares)

    router = app.router
    router.add_route('GET', '/chat/{channel}/{token}/',
                     handlers.websocket_handler)

    app['redis'] = await aioredis.create_redis(('localhost', 6379),
                                               db=1, encoding='utf-8')
    app['db'] = await aiopg.connect(**db_config)
    app['waiters'] = defaultdict(BList)

    app.on_shutdown.append(close_websockets)
    app.on_shutdown.append(close_redis)
    app.on_shutdown.append(close_db)

    return app

if __name__ == '__main__':
    debug = True
    if debug:
        logging.basicConfig(level='DEBUG')
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(get_app())
    web.run_app(app)
