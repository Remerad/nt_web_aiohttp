import json
import bcrypt
from datetime import datetime
from aiohttp import web
from gino import Gino
from asyncpg.exceptions import UniqueViolationError

PG_DSN = 'postgres://postgres:postgres@127.0.0.1:5433/aiohttp_netology'
app = web.Application()
db = Gino()


class HTTPExeption(web.HTTPClientError):

    def __init__(self, *args, error='', **kwargs):
        kwargs['text'] = json.dumps({'errror': error})
        super().__init__(*args, **kwargs, content_type='application/json')


class BadRequest(HTTPExeption):
    status_code = 400


class NotFound(HTTPExeption):
    status_code = 404


class AdModel(db.Model):
    __tablename__ = 'advertisements'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String, nullable=False)
    registration_time = db.Column(db.DateTime, server_default='now()')
    owner = db.Column(db.String, nullable=False)
    _idx1 =db.Index('app_advertisements_title', 'title', unique=True)


class AdView(web.View):
    async def get(self):
        adv_id = int(self.request.match_info['ad_id'])
        adv = await AdModel.get(adv_id)
        if adv is None:
            raise NotFound(error='No adv with such title')
        return web.json_response({
            'id': adv.id,
            'title': adv.title,
            'description': adv.description,
            'registration_time': str(adv.registration_time),
            'owner': adv.owner
        })

    async def post(self):
        user_data = await self.request.json()
        try:
            new_ad = await AdModel.create(**user_data)
        except UniqueViolationError:
            raise BadRequest(error='AD already exist.')

        return web.json_response(
            {'id': new_ad.id,
             'title': new_ad.title,
             'description': new_ad.description,
             'registration_time': str(new_ad.registration_time),
             'owner': new_ad.owner
             }
        )

    async def delete(self):
        adv_id = int(self.request.match_info['ad_id'])
        adv = await AdModel.get(adv_id)
        if adv is None:
            raise NotFound(error='No adv with such title')
        await adv.delete()
        return web.json_response({
            'id': adv_id,
            'status': 'deleted'
        })


async def init_orm(app):
    await db.set_bind(PG_DSN)
    await db.gino.create_all()
    yield    #Всё, что до yield произойдет при запуске app, что после - при её завершении.
    await db.pop_bind().close()


app.router.add_route('GET', '/ad/{ad_id:\d+}', AdView)
app.router.add_route('POST', '/ad/', AdView)
app.router.add_route('DELETE', '/ad/{ad_id:\d+}', AdView)


app.cleanup_ctx.append(init_orm)

web.run_app(app=app)
