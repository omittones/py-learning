import asyncio
import deezer
from services.for_deezer import DeezerAuthenticator
from typing import List

APP_ID = '173261'
APP_SECRET = '4ba3efb12aaa0cc531e488d698404e9e'


def main():
    authenticator = DeezerAuthenticator(APP_ID, APP_SECRET)
    authenticator.authenticate()
    print(authenticator.access_token)

    client = deezer.Client(app_id=APP_ID, app_secret=APP_SECRET)
    client.access_token = authenticator.access_token
    client.follow_next_links = True
    u: deezer.User = client.get_user('me')
    for i in u.get_playlists():
        print(i.title)
        for t in i.get_tracks():
            print('    ',
                  f'{t.artist.name} - {t.title} (from {t.album.title})')


if __name__ == '__main__':
    main()
