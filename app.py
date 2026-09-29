import os
import requests
from flask import Flask, request, Response, abort

app = Flask(__name__)
SERVICES = {name: os.environ.get(name.upper() + '_URL', 'http://' + name + ':8080')
            for name in ('accounts', 'catalog', 'bundles', 'connectors', 'navigation', 'render')}

@app.get('/health')
def health():
    return {'status': 'ready'}

@app.route('/api/<service>/<path:path>', methods=['GET', 'POST'])
def dispatch(service, path):
    if service not in SERVICES or (service == 'accounts' and path == 'session'):
        abort(404)
    bearer = request.headers.get('Authorization', '')
    if not bearer.startswith('Bearer '):
        abort(401)
    session = requests.post(SERVICES['accounts'] + '/session',
        json={'token': bearer[7:]},
        headers={'X-Service-Key': os.environ['SERVICE_KEY']}, timeout=5)
    if session.status_code != 200:
        abort(401)
    actor = session.json()
    forwarded = {'X-User-Id': actor['user'], 'X-Tenant-Id': actor['tenant']}
    for name, value in request.headers.items():
        if name.lower().startswith('x-') and name.lower() != 'x-service-key':
            forwarded[name] = value
    forwarded['X-Service-Key'] = os.environ['SERVICE_KEY']
    forwarded['Content-Type'] = request.content_type or 'application/octet-stream'
    upstream = requests.request(request.method, SERVICES[service] + '/' + path,
        params=request.args, data=request.get_data(), headers=forwarded,
        timeout=15, allow_redirects=False)
    response_headers = {k: v for k, v in upstream.headers.items()
                        if k.lower() in ('content-type', 'location')}
    return Response(upstream.content, status=upstream.status_code, headers=response_headers)
