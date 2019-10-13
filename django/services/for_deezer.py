import http
import http.client
import http.server
import json
import threading
import webbrowser
from socketserver import BaseServer, TCPServer


class DeezerAuthenticator(http.server.HTTPServer):

    class Finished(Exception):
        pass

    class Handler(http.server.BaseHTTPRequestHandler):

        def parse_request(self):
            ok = super().parse_request()
            if ok:
                self.query_string = self.parse_querystring()
            return ok

        def parse_querystring(self):
            x = self.path.index('?')
            qs = self.path[x+1:] if x > -1 else None
            if qs is not None:
                raw = [i.split('=') for i in qs.split('&')]
                return {i[0]: i[1] for i in raw}
            return {}

        def do_GET(self):
            self.send_response(200, 'Done!')
            self.end_headers()
            if self.path.startswith('/receive_code'):
                self.server.access_code = self.query_string.get('code', None)
                if self.server.access_code is None:
                    reason = self.query_string.get('error_reason', 'Unknown')
                    self.log_error(f'Could not authenticate, reason: {reason}')

    def __init__(self, app_id, app_secret):
        self.url = ('localhost', 8000)
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_code = None
        self.access_token = None
        self.engine = None
        super().__init__(self.url, DeezerAuthenticator.Handler)

    def authenticate(self):
        self._serve_in_thread()
        get_token = f'https://connect.deezer.com/oauth/auth.php?app_id={self.app_id}&redirect_uri=http://{self.url[0]}:{self.url[1]}/receive_code&perms=basic_access,email,offline_access'
        print('Opening:', get_token)
        webbrowser.open_new_tab(get_token)
        try:
            while (self.engine.is_alive()):
                self.engine.join(0.5)
            if self.access_code is not None:
                self.access_token = self._get_access_token()

        except KeyboardInterrupt:
            print('Aborting...')
            self.shutdown()

    def _get_access_token(self):
        path = f'/oauth/access_token.php?app_id={self.app_id}&secret={self.app_secret}&code={self.access_code}&output=json'
        conn = http.client.HTTPSConnection("connect.deezer.com", port=443)
        try:
            conn.request("GET", path)
            r = conn.getresponse()
            if r.status == 200:
                token = json.loads(r.read())
                return token.get('access_token', None)
            return None
        finally:
            conn.close()

    def _serve_in_thread(self):
        self.engine = threading.Thread(target=self.serve_forever)
        self.engine.start()

    def _handle_request_noblock(self):
        if self.access_code is None:
            super()._handle_request_noblock()
        else:
            raise DeezerAuthenticator.Finished()

    def serve_forever(self, poll_interval=0.5):
        print('Running server...')
        try:
            super().serve_forever(poll_interval=poll_interval)
        except DeezerAuthenticator.Finished:
            pass
