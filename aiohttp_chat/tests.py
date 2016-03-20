import asyncio
import aiopg

db_config = {
    'database': 'chat',
    'user': 'django',
    'password': 'secr3t',
    'host': 'localhost'
}
async def test():
    conn = await aiopg.connect(**db_config)
    async with conn.cursor() as cur:
        channel_id = 1
        message = 'Wubba lubba part 2!'
        token = '37e84ac8cb424ac7dc53a7918cc032d11af4442'

        sql = """SELECT u.id as id, u.username as username
                  FROM auth_user as u INNER JOIN authtoken_token as t
                  ON u.id = t.user_id WHERE t.key = %s"""
        await cur.execute(sql, parameters=(token,))
        user_id, username = await cur.fetchone()

        insert_s = """INSERT INTO chat_message
                       (text, channel_id, create_date, sender_id)
                       VALUES (%s, %s, now(), %s)
                       RETURNING text, create_date, channel_id, sender_id """
        await cur.execute(insert_s, parameters=(message, channel_id, user_id))

        text, timestamp, ch_id, u_id = await cur.fetchone()

        assert channel_id == ch_id
        assert user_id == u_id

        data = {'time': timestamp.isoformat(),
                'username': username, 'text': text}

        print(data)
    conn.close()
loop = asyncio.get_event_loop()
loop.run_until_complete(test())

# 37e84ac8cb424ac7dc53a7918cc032d11af4442d
# http://127.0.0.1:8080/1/37e84ac8cb424ac7dc53a7918cc032d11af4442d