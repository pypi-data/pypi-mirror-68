# Engage Voice SDK Wrapper for Python.

----
## Overview
EngageVoice SDK Wrapper for Python is a utility class, which helps you easily integrate your Python project with RingCentral Engage Voice Services.

Code your Python app with PyCharm. Get it from https://www.jetbrains.com/pycharm/download

----
## Add Engage Voice SDK Wrapper to a Python project
1. Download the EngageVoice SDK Wrapper for Python.
2. Unzip and copy the whole engagevoice_sdk_wrapper folder to your project folder.

*OR*

1. To install the latest version directly from this github repo:
```
pip install git+https://github.com/pacovu/engagevoice-sdk-wrapper-python

pip install engagevoice-sdk-wrapper
```

----
## API References
**Constructor**
```
RestClient(clientId, clientSecret, mode)
```

*Description:*
* Creates and initializes an EngageVoice object.

*Parameters:*
* clientId: Set the `clientId` of a RingCentral app to enable login with RingCentral user credentials.
* clientSecret: Set the `clientSecret` of a RingCentral app to enable login with RingCentral user credentials.
* mode: Set the mode to login Engage Voice. For legacy server, use "Legacy".

*Example code:*
```
from engagevoice.sdk_wrapper import *

# Access legacy server
ev = RestClient()

# Access migrated server
ev = RestClient(RC_APP_CLIENT_ID, RC_APP_CLIENT_SECRET)
```
----
**Function login**
    login(username, password, extensionNumber)

*Description:*
* Login using a user's credential. If the mode was set "Engage", the username and password must be the valid username and password of a RingCentral Office user.

*Parameters:*
* username: username of a user in Legacy service or in RingCentral Office service.
* password: password of a user in Legacy service or in RingCentral Office service.
* extensionNumber: the extension number if `username` is a RingCentral company main number.

*Response:*


*Example code:*
```
# Login with RingCentral Office user credentials.

ev = RestClient(RC_APP_CLIENT_ID, RC_APP_CLIENT_SECRET))
try:
    resp = ev.login(RC_USERNAME, RC_PASSWORD, RC_EXTENSION_NUMBER)
    print (resp)
except Exception as e:
    print (e)


# Login with Legacy user credentials

ev = EngageVoice()
try:
    resp = ev.login(LEGACY_USERNAME, LEGACY_PASSWORD)
    print (resp)
except Exception as e:
    print (e)


```

**Function get**
```
get(endpoint, params)

get(endpoint, params, callback)
```
*Description:*
* Send an HTTP GET request to Engage Voice server.

*Parameters:*
* endpoint: Engage Voice API endpoint.
* params: a dictionary dict() containing key/value pair parameters to be sent to an Engage Voice API, where the keys are the query parameters of the API.
* callback: if specified, response is returned to callback function.

*Response:*
API response in JSON object

*Example code:*
```
# Read account info.

endpoint = "admin/accounts"
try:
    resp = ev.get(endpoint, None)
    print (resp)
except Exception as e:
    print (e)

```

**Function post**
```
post(endpoint, params)

post(endpoint, params, callback)
```
*Description:*
* Sends an HTTP POST request to Engage Voice server.

*Parameters:*
* endpoint: Engage Voice API
* params: a dictionary dict() containing key/value pair parameters to be sent to an Engage Voice API, where the keys are the body parameters of the API.
* callback: if specified, response is returned to callback function.

*Response:*
API response in JSON object

*Example code:*

```
# Search for campaign leads.

endpoint = "admin/accounts/~/campaignLeads/leadSearch"
params = { 'firstName': "Larry" }
try:
    resp = ev.post(endpoint, params)
    print (resp)
except Exception as e:
    print (e)

```
## License
Licensed under the MIT License.
