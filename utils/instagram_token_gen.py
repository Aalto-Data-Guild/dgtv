# See authorization procedure at https://developers.facebook.com/docs/instagram-basic-display-api/getting-started
import os
import dotenv
import requests

dotenv.load_dotenv('../.env')

APP_ID = os.getenv('INSTAGRAM_APP_ID')
REDIRECT_URI = os.getenv('INSTAGRAM_REDIRECT_URI')
APP_SECRET = os.getenv('INSTAGRAM_APP_SECRET')


def intro():
    print(
        """Add the user in the instagram basic display as an instagram tester.
Accept the response at Edit Profile > Apps and Websites > Tester Invites.
Do not log out before the next step.""")


def authenticate() -> str:
    link = "https://api.instagram.com/oauth/authorize?" + \
           f"client_id={APP_ID}&redirect_uri={REDIRECT_URI}&" + \
           "scope=user_profile,user_media&response_type=code"
    print('Access', link)

    access_code = input(f'\nCopy the code (everything after {REDIRECT_URI}?code=) in the console\n')
    return access_code


def code_to_token(code: str):
    payload = {
        'client_id': APP_ID,
        'client_secret': APP_SECRET,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI,
        'code': code
    }
    session = requests.Session()
    r = session.post('https://api.instagram.com/oauth/access_token', data=payload, timeout=3)

    if not r.ok:
        raise SystemExit('Could not retrieve the token: ' + r.json()['error_message']
                         if 'application/json' in r.headers.get('Content-Type', '') else r.content.decode())
    return r.json()['access_token']


def main():
    intro()
    access_code = authenticate()
    token = code_to_token(access_code)
    print('Your token is:', token)


if __name__ == '__main__':
    main()
