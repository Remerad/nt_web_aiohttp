from aiohttp import web


app = web.Application()


async def test(request: web.Request):
    json_data = await request.json()
    headers = request.headers
    qs = request.query
    return web.json_response(
        {'hello': 'world',
         'json': json_data,
         'headers': dict(headers),
         'qs': dict(qs)}
    )

app.router.add_route('POST', '/test/', test)
web.run_app(app=app)
