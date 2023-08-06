"""
NodeQuery https://nodequery.com integration for your Python project.
"""
import json
import urllib.request

class NodeQuery:
    """This class is used to get information from NodeQuery."""
    BASE_URL = 'https://nodequery.com/api'

    def __init__(self, apikey):
        """Initialize"""
        self.apikey = apikey

    def accountStatus(self):
        """The account endpoint will return basic information like name, timezone, server limit, request count and rate limit. The timezone is given as an integer value of the UTC offset in hours."""
        fetchUrl = self.BASE_URL + '/account' + '?api_key=' + self.apikey
        try:
            req = urllib.request.urlopen(fetchUrl)
        except urllib.error.URLError as e:
            raise Exception(e.code)
        else:
            if req:
                jsonData = json.loads(req.read())
                if jsonData['status'] == 'OK':
                    return jsonData['data']
                else:
                    raise Exception(0)
            else:
                raise Exception(0)

    def listServers(self):
        """List all servers for the current account. The returned data will be sorted ascending by name and includes basic server and resource usage data. New and unavailable servers will be marked as inactive."""
        fetchUrl = self.BASE_URL + '/servers' + '?api_key=' + self.apikey
        try:
            req = urllib.request.urlopen(fetchUrl)
        except urllib.error.URLError as e:
            raise Exception(e.code)
        else:
            if req:
                jsonData = json.loads(req.read())
                if jsonData['status'] == 'OK':
                    return jsonData['data']
                else:
                    raise Exception(0)
            else:
                raise Exception(0)

    def serverDetails(self, server):
        """As soon as you provide a valid id to the servers endpoint you will receive detailed information about the server in your account. A new or unavailable server will be marked as inactive."""
        fetchUrl = self.BASE_URL + '/servers/' + server + '?api_key=' + self.apikey
        try:
            req = urllib.request.urlopen(fetchUrl)
        except urllib.error.URLError as e:
            raise Exception(e.code)
        else:
            if req:
                jsonData = json.loads(req.read())
                if jsonData['status'] == 'OK':
                    return jsonData['data']
                else:
                    raise Exception(0)
            else:
                raise Exception(0)

    def loads(self, loadtype, server):
        """The loads endpoint will always return all objects with information about each interval. If no data was found for an interval it will return 0 for every value. Possible selectors are currently hourly, daily and monthly. Starting August 1st, 2014 we will also offer a yearly load cache."""
        fetchUrl = self.BASE_URL + '/loads/' + loadtype + '/' + server + '?api_key=' + self.apikey
        try:
            req = urllib.request.urlopen(fetchUrl)
        except urllib.error.URLError as e:
            raise Exception(e.code)
        else:
            if req:
                jsonData = json.loads(req.read())
                if jsonData['status'] == 'OK':
                    return jsonData['data']
                else:
                    raise Exception(0)
            else:
                raise Exception(0)
