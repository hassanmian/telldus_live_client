import httplib, urllib, json
from oauth import oauth

class TelldusLiveClient(object):
    PUBLIC_KEY = None
    PRIVATE_KEY = None
    TOKEN = None
    TOKEN_SECRET = None

    TELLSTICK_TURNON = 1
    TELLSTICK_TURNOFF = 2
    TELLSTICK_BELL = 4
    TELLSTICK_DIM = 16
    TELLSTICK_UP = 128
    TELLSTICK_DOWN = 256

    SUPPORTED_METHODS = TELLSTICK_TURNON | TELLSTICK_TURNOFF | TELLSTICK_BELL | TELLSTICK_DIM | TELLSTICK_UP | TELLSTICK_DOWN;

    def __init__(self, public_key, private_key, token, token_secret):
        self.PUBLIC_KEY = public_key
        self.PRIVATE_KEY = private_key
        self.TOKEN = token
        self.TOKEN_SECRET = token_secret

    def get_device_list(self):
        response = self.do_request('devices/list', {'supportedMethods': self.SUPPORTED_METHODS})
        return response['device']

    def get_device_state(self, device_id):
        response = self.do_request('device/info', {'id': device_id, 'supportedMethods': self.SUPPORTED_METHODS})
        return int(response['state'])

    def update_device_state(self, device_id, tellstick_state, _value=None):
        response = self.do_request('device/command', {'id': device_id, 'method': tellstick_state, 'value': _value})
        return response

    def toggle_device_state(self, device_id):
        state = self.get_device_state(device_id)

        if state == self.TELLSTICK_TURNON:
            self.update_device_state(device_id=device_id, tellstick_state=self.TELLSTICK_TURNOFF)
        elif state == self.TELLSTICK_TURNOFF:
            self.update_device_state(device_id=device_id, tellstick_state=self.TELLSTICK_TURNON)

    def get_phones(self):
        response = self.do_request('user/listPhones', {})
        return response['phone']

    def send_push(self, phone_id, message):
        response = self.do_request('user/sendPushTest', {'phoneId': phone_id, 'message': message})
        return response



    def do_request(self, method, params):
        consumer = oauth.OAuthConsumer(self.PUBLIC_KEY, self.PRIVATE_KEY)
        token = oauth.OAuthToken(self.TOKEN, self.TOKEN_SECRET)
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(
            consumer, token=token, http_method='GET',
            http_url='http://api.telldus.com/json/{}'.format(method),
            parameters=params
        )
        oauth_request.sign_request(oauth.OAuthSignatureMethod_HMAC_SHA1(), consumer, token)
        headers = oauth_request.to_header()
        headers['Content-Type'] = 'application/x-www-form-urlencoded'

        conn = httplib.HTTPConnection('api.telldus.com')
        url_encoded_params = urllib.urlencode(params)
        _uri = '/json/{}?{}'.format(method, url_encoded_params)
        conn.request('GET', _uri, headers=headers)
        response = conn.getresponse()
        return json.load(response)

    def tellstick_state_to_string(self, _code):
        if _code == self.TELLSTICK_TURNON:
            state = 'ON'
        elif _code == self.TELLSTICK_TURNOFF:
            state = 'OFF'
        elif _code == self.TELLSTICK_DIM:
            state = 'DIMMED'
        elif _code == self.TELLSTICK_UP:
            state = 'UP'
        elif _code == self.TELLSTICK_DOWN:
            state = 'DOWN'
        else:
            state = 'Unknown state'
        return state

    def string_to_tellstick_state(self, _string):
        if _string == 'ON':
            state = self.TELLSTICK_TURNON
        elif _string == 'OFF':
            state = self.TELLSTICK_TURNOFF
        elif _string == 'DIMMED':
            state = self.TELLSTICK_DIM
        elif _string == 'UP':
            state = self.TELLSTICK_UP
        elif _string == 'DOWN':
            state = self.TELLSTICK_DOWN
        else:
            state = None
        return state
