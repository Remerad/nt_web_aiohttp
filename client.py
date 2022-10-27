import asyncio
import aiohttp

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.post(
                'http://127.0.0.1:8080/test/',
                json={'json_key': 'json_value'},
                headers={'header_1': 'Value_1'},
                params={'param_1': 'Value_1'}
        ) as response:
            print(await response.json())

asyncio.run(main())