from aiohttp import web
import json

async def index(request):
    response_obj = { 'url' : 'success' }
    return web.Response(text=json.dumps(response_obj))

async def url_shorteners(request):
    try:
        url = request.query['url']
        print("Shorteners url: " , url)
        response_obj = { 'status' : 'success' }
        return web.Response(text=json.dumps(response_obj), status=200)

    except Exception as e:
        response_obj = { 'status' : 'failed', 'reason': str(e) }
        return web.Response(text=json.dumps(response_obj), status=500)

app = web.Application()
app.router.add_get('/', index)
app.router.add_post('/', url_shorteners)


if __name__ == '__main__':
    web.run_app(app)
