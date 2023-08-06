from twitch.twitch import Twitch

import unittest

client = "bbmlrbeosiodax7ol9gf9cb19cn9i7"
secret = "ldqlvzn4h80cvd35pn1fevccgnqlwj"


class TestFileIOMethods(unittest.TestCase):

    async def test_open_session(self):
        async with Twitch(client, secret):
            return

    async def test_user(self):
        async with Twitch(client, secret) as session:
            await session.user('MagicaFreak')

    async def test_stream(self):
        async with Twitch(client, secret) as session:
            await session.stream('Naveyn')

    async def test_game(self):
        async with Twitch(client, secret) as session:
            await session.game('Minecraft')

    async def test_top_games(self):
        async with Twitch(client, secret) as session:
            await session.top_games()

    async def test_tags(self):
        async with Twitch(client, secret) as session:
            await session.user(['1d3d4f9c-be88-44f3-8e80-3b0779308c64', 'e659959d-392f-44c5-83a5-fb959cdbaccc'])


if __name__ == '__main__':
    unittest.main()
