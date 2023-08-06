import requests
import base64
import urllib
import time
import json
import os, sys

class RestClient(object):
    RC_TOKEN_FILE = "rc_tokens.txt"
    RC_AUTH_SERVER_URL = "https://platform.ringcentral.com/restapi/oauth/token"
    EV_SERVER_URL = "https://engage.ringcentral.com/voice/api/v1/"
    EV_LOGIN_SERVER_URL = "https://engage.ringcentral.com/api/auth/login/rc/accesstoken"

    LEGACY_SERVER_URL = "https://portal.vacd.biz/api/v1/"

    serverUrl = ""
    accessToken = None
    accountId = None
    clientId = ""
    clientSecret = ""
    mode = ""

    def __init__(self, clientId=None, clientSecret=None):
        if clientId == None or clientSecret == None:
            self.serverUrl = self.LEGACY_SERVER_URL
            self.mode = "Legacy"
        else:
            self.serverUrl = self.EV_SERVER_URL
            self.clientId = clientId
            self.clientSecret = clientSecret
            self.mode = "Engage"

    def getAccountId(self):
        return self.accountId

    def setAccessToken(self, accessToken, callback=None):
        self.accessToken = accessToken
        res = self.__readAccount()
        jsonObj = json.loads(res._content)
        self.accountId = jsonObj[0]['accountId']
        if callback is None:
            return jsonObj
        else:
            callback(res)

    def login(self, username, password, extensionNumber=None, callback=None):
        if self.mode == "Engage":
            accessToken = self.__rc_login(username, password, extensionNumber)
            url = self.EV_LOGIN_SERVER_URL
            body = "rcAccessToken=%s&rcTokenType=Bearer" % (accessToken)
            headers = {
              'Content-Type': 'application/x-www-form-urlencoded'
              }
            try:
                res = requests.post(url, headers=headers, data=body)
                if res.status_code == 200:
                    jsonObj = json.loads(res._content)
                    self.accessToken = jsonObj['accessToken']
                    self.accountId = jsonObj['agentDetails'][0]['accountId']
                    if callback is None:
                        return jsonObj
                    else:
                        callback(res)
                else:
                    raise ValueError(res._content)
            except Exception as e:
                raise ValueError(e)
        else:
            if self.accessToken != None:
                if callback is None:
                    return self.accessToken
                else:
                    callback(self.accessToken)
            else:
                res = self.__generateAuthToken(username, password)
                jsonObj = json.loads(res._content)
                if callback is None:
                    return jsonObj
                else:
                    callback(res)

    def __readAccount(self):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-Auth-Token': self.accessToken
            }
        try:
            url = self.serverUrl + "admin/accounts"
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                return res
            else:
                raise ValueError(res)
        except Exception as e:
            raise ValueError(e)

    def __generateAuthToken(self, username, password):
        url = self.serverUrl + "auth/login"
        body = "username=%s&password=%s" % (username, password)
        headers = {
          'Content-Type': 'application/x-www-form-urlencoded'
          }
        try:
            res = requests.post(url, headers=headers, data=body)
            if res.status_code == 200:
                jsonObj = json.loads(res._content)
                self.accountId = jsonObj['accounts'][0]['accountId']
                tokens = self.__readPermanentsToken(jsonObj["authToken"])
                jsonObj['permanentTokens'] = tokens
                return res
            else:
                raise ValueError(res)
        except Exception as e:
            raise ValueError(e)

    def __readPermanentsToken(self, authToken):
        url = self.serverUrl + "admin/token"
        headers = {
          'X-Auth-Token': authToken
          }
        try:
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                jsonObj = json.loads(res._content)
                if len(jsonObj):
                    self.accessToken = jsonObj[0]
                    return jsonObj
                else:
                    self.__generatePermanentToken(authToken)
            else:
                raise ValueError(response._content)
        except Exception as e:
            raise ValueError(e)

    def __generatePermanentToken(self, authToken):
        url = self.serverUrl + "admin/token"
        headers = {
          'X-Auth-Token': authToken
          }
        try:
            res = requests.post(url, headers=headers, data=None)
            if res.status_code == 200:
                self.accessToken = res._content
            else:
                raise ValueError(res)
        except Exception as e:
            raise ValueError(e)

    # Implement GET request
    def get(self, endpoint, params=None, callback=None):
        if self.accessToken == None:
            if callback is None:
                return "Login required!"
            else:
                callback("Login required!")

        if "~" in endpoint:
            endpoint = endpoint.replace("~", self.accountId)
        url = self.serverUrl + endpoint

        if params != None:
            url += "?"
            for key, value in params.items():
                url += "&%s=%s" % (key, value)
        if self.mode == "Engage":
            headers = {
                    'Accept': 'application/json',
                    'Authorization': 'Bearer ' + self.accessToken
                    }
        else:
            headers = {
                    'Accept': 'application/json',
                    'X-Auth-Token': self.accessToken
                    }
        try:
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                if callback is None:
                    return json.loads(res._content)
                else:
                    callback(res)
            else:
                raise ValueError(res)
        except Exception as e:
            raise ValueError(e)


    # Implement POST request
    def post(self, endpoint, params=None, callback=None):
        if self.accessToken == None:
            if callback is None:
                return "Login required!"
            else:
                callback("Login required!")

        if "~" in endpoint:
            endpoint = endpoint.replace("~", self.getAccountId())
        url = self.serverUrl + endpoint
        body = None
        if params != None:
            body = json.dumps(params)

        if self.mode == "Engage":
            headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + self.accessToken
                    }
        else:
            headers = {
                    'Content-Type': 'application/json',
                    'X-Auth-Token': self.accessToken
                }
        try:
            res = requests.post(url, headers=headers, data=body)
            if res.status_code == 200 or res.status_code == 201:
                if callback is None:
                    return json.loads(res._content)
                else:
                    callback(res)
            else:
                raise ValueError(res)
        except Exception as e:
            raise ValueError(e)

    # Implement DELETE request
    def delete(self, endpoint, params=None, callback=None):
        if self.accessToken == None:
            if callback is None:
                return "Login required!"
            else:
                callback("Login required!")

        if "~" in endpoint:
            endpoint = endpoint.replace("~", self.getAccountId())
        url = self.serverUrl + endpoint
        body = None
        if params != None:
            body = json.dumps(params)

        if self.mode == "Engage":
            headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + self.accessToken
                    }
        else:
            headers = {
                    'Content-Type': 'application/json',
                    'X-Auth-Token': self.accessToken
                }
        try:
            res = requests.delete(url, headers=headers, data=body)
            if res.status_code == 200 or res.status_code == 201:
                jsonObj = json.loads(res._content)
                if callback is None:
                    return jsonObj
                else:
                    callback(res)
            else:
                raise ValueError(res)
        except Exception as e:
            raise ValueError(e)

    # Implement PUT request
    def put(self, endpoint, params=None, callback=None):
        if self.accessToken == None:
            if callback is None:
                return "Login required!"
            else:
                callback("Login required!")

        if "~" in endpoint:
            endpoint = endpoint.replace("~", self.getAccountId())
        url = self.serverUrl + endpoint
        body = None
        if params != None:
            body = json.dumps(params)

        if self.mode == "Engage":
            headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + self.accessToken
                    }
        else:
            headers = {
                    'Content-Type': 'application/json',
                    'X-Auth-Token': self.accessToken
                }
        try:
            res = requests.put(url, headers=headers, data=body)
            if res.status_code == 200 or res.status_code == 201:
                jsonObj = json.loads(res._content)
                if callback is None:
                    return jsonObj
                else:
                    callback(res)
            else:
                raise ValueError(res)
        except Exception as e:
            raise ValueError(e)

    def __rc_login(self, username, password, extension=None):
        basic = "%s:%s" % (self.clientId, self.clientSecret)
        basic = base64.b64encode(basic.encode('utf-8')).decode('utf-8')
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json',
            'Authorization': 'Basic ' + basic,
            }
        body = {
            'grant_type': 'password',
            'username': username,
            'password': password
            }
        if extension != None:
            body['extension'] = extension

        if os.path.isfile(self.RC_TOKEN_FILE):
            file = open(self.RC_TOKEN_FILE, 'r')
            tokenObj = json.loads(file.read())
            file.close()
            expire_time = time.time() - tokenObj['timestamp']
            if expire_time < tokenObj['tokens']['expires_in']:
                return tokenObj['tokens']['access_token']
            else:
                if expire_time < tokenObj['tokens']['refresh_token_expires_in']:
                    body = {
                        'grant_type': 'refresh_token',
                        'refresh_token': tokenObj['tokens']['refresh_token']
                    }

        if sys.hexversion >= 0x3000000:
            body = urllib.parse.urlencode(body)
        else:
            body = urllib.urlencode(body)

        try:
            res = requests.post(self.RC_AUTH_SERVER_URL, headers=headers, data=body)
            if res.status_code == 200:
                jsonObj = json.loads(res._content)
                tokensObj = {
                    "tokens": jsonObj,
                    "timestamp": time.time()
                    }
                file = open(self.RC_TOKEN_FILE,'w')
                file.write(json.dumps(tokensObj))
                file.close()
                return jsonObj['access_token']
            else:
                raise ValueError(res._content)
        except Exception as e:
            raise ValueError(e)
