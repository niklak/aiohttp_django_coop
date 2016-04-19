import json
from aiohttp import web, log
import logging


async def get_user_by_token(cur, token):
    sql = """SELECT u.id, u.username
          FROM auth_user as u INNER JOIN authtoken_token as t
          ON u.id = t.user_id WHERE t.key = %s"""
    await cur.execute(sql, parameters=(token,))
    return await cur.fetchone()


async def perform_message(cur, channel_id, user, text):

    user_id, username = user

    insert_s = """INSERT INTO chat_message
                   (text, channel_id, create_date, sender_id)
                   VALUES (%s, %s, now(), %s)
                   RETURNING create_date"""
    await cur.execute(insert_s, parameters=(text, channel_id, user_id))

    timestamp, = await cur.fetchone()
    data = {'create_date': timestamp.isoformat(),
            'sender': username, 'text': text}
    return json.dumps(data)


async def websocket_handler(request):

    db = request.app['db']
    token = request.match_info.get('token')

    ws = web.WebSocketResponse(autoclose=False)
    await ws.prepare(request)

    async with db.cursor() as cur:
        user = await get_user_by_token(cur, token)

    try:
        user_id, username = user
    except TypeError:
        log.ws_logger.error('Probably bad token is the reason why'
                            ' you get None instead tuple.', exc_info=True)
        await ws.close()
        return ws

    channel = request.match_info.get('channel')
    channel_id = int(channel)
    channel_users = 'channels:{}:users'.format(channel)

    channel_waiters = request.app['waiters'][channel]
    channel_waiters.append(ws)

    r = request.app['redis']

    try:
        count = int(await r.zcard(channel_users))

        await r.zadd(channel_users, count+1, username)
        users = await r.zrange(channel_users)
        channel_waiters.broadcast(json.dumps({'user_list': users}))

        async for msg in ws:
            log.ws_logger.info('MSG: {}'.format(msg))

            if msg.tp == web.MsgType.text:
                async with db.cursor() as cur:
                    data = await perform_message(cur, channel_id,
                                                 user, msg.data)
                channel_waiters.broadcast(data)
            elif msg.tp == web.MsgType.error:
                logging.error('connection closed with exception {}'
                              .format(ws.exception()))
    except:
        log.ws_logger.error('ERROR has been happened', exc_info=True)
    finally:
        # 2. Send message to all who remained at the channel with new user list
        if ws in channel_waiters:
            await ws.close()
            log.ws_logger.info('Is WebSocket closed?: {}'.format(ws.closed))
            channel_waiters.remove(ws)

        await r.zrem(channel_users, username)
        users = await r.zrange(channel_users)

        channel_waiters.broadcast(json.dumps({'user_list': users}))

    return ws
