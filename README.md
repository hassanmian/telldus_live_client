# Telldus Live Client
Python Wrapper for Telldus Live


## Usage

```
from client import TelldusLiveClient

public_key = 'PUBLIC KEY'
private_key = 'PRIVATE KEY'
token = 'TOKEN'
token_secret = 'TOKEN SECRET'
tlc = TelldusLiveClient(
    public_key=public_key, private_key=private_key,
    token=token, token_secret=token_secret
)

device_list = tlc.get_device_list()
for device in device_list:
    print device['name'], device['id'], tlc.tellstick_state_to_string(device['state'])

tlc.update_device_state(**DEVICE_ID**, tlc.TELLSTICK_TURNON)
```
