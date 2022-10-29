import asyncio
import aiohttp

async  def main():

    async with aiohttp.ClientSession() as session:
        async with session.delete('http://127.0.0.1:8080/ad/1') as response:
            print(await response.text())

    # async with aiohttp.ClientSession() as session:
    #     async with session.get('http://127.0.0.1:8080/ad/2') as response:
    #         print (await response.json())

    # async with aiohttp.ClientSession() as session:
    #     async with session.post(
    #             'http://127.0.0.1:8080/ad/',
    #             json={'id': 2,
    #                   'title': 'Продам гараж 2',
    #                   'description': 'Кирпичный, с ямой и гнилым полом',
    #                   'owner': 'Вася'},
    #     )as response:
    #         print(await response.text())


asyncio.run(main())