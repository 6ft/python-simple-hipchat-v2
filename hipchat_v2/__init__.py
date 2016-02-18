try:
    from urllib.parse import urljoin
    import urllib.request as urlrequest
except ImportError:
    from urlparse import urljoin
    import urllib2 as urlrequest
import json

API_URL_DEFAULT = 'https://www.hipchat.com/'
FORMAT_DEFAULT = 'json'

class HipChat(object):
    def __init__(self, token=None, url=API_URL_DEFAULT, format=FORMAT_DEFAULT):
        self.url = url
        self.token = token
        self.format = format
        self.opener = urlrequest.build_opener(urlrequest.HTTPSHandler())

    class RequestWithMethod(urlrequest.Request):
        def __init__(self, url, data=None, headers={}, origin_req_host=None, unverifiable=False, http_method=None):
            urlrequest.Request.__init__(self, url, data, headers, origin_req_host, unverifiable)
            if http_method:
                self.method = http_method

        def get_method(self):
            if self.method:
                return self.method
            return urlrequest.Request.get_method(self)

    def method(self, url, method='POST', headers={}, data=None, timeout=None):
        method_url = urljoin(self.url, url)
        req = self.RequestWithMethod(method_url, http_method=method, headers=headers, data=data)
        self.opener.open(req, None, timeout).read()

    def message_room(self, room_id='', message='', message_format='text', color='', notify=False, token='', message_from='me'):
        url = 'v2/room/{}/notification'.format(room_id)
        headers = {
              "content-type": "application/json",
              "authorization": "Bearer {}".format(token)
        }

        data = json.dumps({
          'message': message,
          'color': color,
          'message_format': message_format,
          'notify': notify,
          'from': message_from,
        })

        return self.method(url, headers=headers, data=data.encode('utf-8'))
