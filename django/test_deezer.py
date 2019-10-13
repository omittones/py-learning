import asyncio
import deezer
from services.for_deezer import DeezerAuthenticator

APP_ID = '173261'
APP_SECRET = '4ba3efb12aaa0cc531e488d698404e9e'


def main():
    authenticator = DeezerAuthenticator(APP_ID, APP_SECRET)
    authenticator.authenticate()
    print(authenticator.access_token)

    client = deezer.Client(
        app_id='173261', app_secret='4ba3efb12aaa0cc531e488d698404e9e')
    client.access_token = authenticator.access_token
    u = client.get_user('me')

    print(u)


if __name__ == '__main__':
    main()
