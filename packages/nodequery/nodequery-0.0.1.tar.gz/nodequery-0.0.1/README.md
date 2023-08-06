# NodeQuery Integration for Python
[NodeQuery](https://nodequery.com) integration for your Python project.

# Installation
To get the latest stable release from [PyPi](https://pypi.org/project/nodequery/)

```bash
	$ pip install nodequery
```

# Usage

Basic Usage with Python:
```python
    >>> from nodequery.nodequery import NodeQuery
    >>> apikey = 'XXXXXXXXXXXXXXXXXXXXXXXX'
    >>> nq = NodeQuery()
    >>> accountStatus = nq.accountStatus(apikey)
    >>> print(accountStatus.data)
    {'name': 'Jeff Rescignano', 'timezone': -4, 'server_limit': 10, 'api': {'requests': 6, 'rate_limit': 180}}
```

Advanced Usage with Python:
```python
    >>> from nodequery.nodequery import NodeQuery
    >>> apikey = 'XXXXXXXXXXXXXXXXXXXXXXXX'
    >>> nq = NodeQuery()
    >>> accountStatus = nq.accountStatus(apikey)
    >>> if accountStatus.httpCode == 200:
    >>> 	print(accountStatus.data)
    >>> else:
    >>> 	print('Error fetching account status: HTTP Code ' + str(accountStatus.httpCode))
```

# Available Endpoints
```python
    >>> from nodequery.nodequery import NodeQuery
    >>> apikey = 'XXXXXXXXXXXXXXXXXXXXXXXX'
    >>> serverId = 'XXXXX'
    >>> loadType = 'hourly'
    >>> nq = NodeQuery()
    >>> nq.accountStatus(apikey)
    >>> nq.listServers(apikey)
    >>> nq.serverDetails(apikey, serverId)
    >>> nq.loads(apikey, loadType, serverId)
```
Each of these endpoint responses are reflect and documented by [NodeQuery's API](https://nodequery.com/help/developer-api)

# NQResponse Class
For each call, an NQResponse class if returned. This class is to help handle errors. nodequery has no built-in error handlers and instead gives you the data in order to make an informed decision when handling the error. The NQResponse class contains two members, `httpCode` and `data`. The `httpCode` always returns the HTTP code of the response from the NodeQuery API, unless we did not recieve a valid response. If no valid response was recieved, `httpCode` will be `0`. Each of the HTTP error codes that pertain to the [NodeQuery API](https://nodequery.com/help/developer-api) are documented in the HTTP Codes Section. As for the `data` member, this reflects the `data` member directly from the [NodeQuery API](https://nodequery.com/help/developer-api).

# HTTP Codes
The following are the HTTP Code responses directly from [NodeQuery's API Documentation](https://nodequery.com/help/developer-api).
| Code            | Description                                     |
| --------------- |-------------------------------------------------|
| 200             | Request was successful                          |
| 400             | Object not found (Invalid serverId or loadType) |
| 401             | Authentication failed (Invalid API Key)         |
| 429             | Rate limit exceeded                             |
| 503             | Maintenance in progress                         |
| Other 500 Level | Something went completely wrong                 |

# History
0.0.1
- Initial commit
- Added basic functionality of the NodeQuery API


# About the API
The full API is documented here: https://nodequery.com/help/developer-api
