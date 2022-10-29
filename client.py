import asyncio
import aiohttp

async  def main():
    # async with aiohttp.ClientSession() as session:
    #     async with session.get('http://127.0.0.1:8080/user/80') as response:
    #         print (await response.json())

    async with aiohttp.ClientSession() as session:
        async with session.post(
                'http://127.0.0.1:8080/user/',
                json={'username': 'user_3',
                      'password': '1234'},

        )as response:
            print(await response.text())


asyncio.run(main())