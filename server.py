import json
import bcrypt
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


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    _idx1 =db.Index('app_users_username', 'username', unique=True)


class UserView(web.View):
    async def get(self):
        user_id = int(self.request.match_info['user_id'])
        user = await UserModel.get(user_id)
        if user is None:
            raise NotFound(error= 'user does not exist')
        return web.json_response({
            'id': user.id,
            'username': user.username
        })

    async def post(self):
        user_data = await self.request.json()
        user_data['password'] = bcrypt.hashpw(
            user_data['password'].encode(),
            bcrypt.gensalt()
                ).decode()
        try:
            new_user = await UserModel.create(**user_data)
            # new_user = await UserModel.create(username=user_data['username'],
            #                                   password=user_data['password'])
        except UniqueViolationError:
            raise BadRequest(error='user already exist.')

            # raise web.HTTPBadRequest(text=json.dumps({'error': 'user already exist.'}),
            #                          content_type='application/json')
            # return web.json_response(
            #     {'error': 'user already exist.'}
            # )

        return web.json_response(
            {'user_id': new_user.id,
             'ph': new_user.password}
        )


async def init_orm(app):
    print('Придложение стартовало')
    await db.set_bind(PG_DSN)
    await db.gino.create_all()
    yield    #Всё, что до yield произойдет при запуске app, что после - при её завершении.
    await db.pop_bind().close()
    print('Придложение закрывается')

async def test(request):

    return web.json_response(
        {'hello': 'world'}
    )

app.router.add_route('POST', '/test/', test)
app.router.add_route('GET', '/user/{user_id:\d+}', UserView)
app.router.add_route('POST', '/user/', UserView)

app.cleanup_ctx.append(init_orm)

web.run_app(app=app)
