from django.http import HttpResponse
from datetime import datetime

def index(request):
    timestamp = request.session.get('created_at')
    if not timestamp:
        request.session['created_at'] = str(datetime.now())
    return HttpResponse('<h1>Hello, world! Session ID is %s ,  %s</h1>' % (request.session.session_key, timestamp))