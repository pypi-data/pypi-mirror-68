# NodeQuery Integration for Python
[NodeQuery](https://nodequery.com) integration for your Python project.

# Installation
To get the latest stable release from [PyPi](https://pypi.org/project/nodequery/)

```bash
	$ pip install nodequery
```

# Usage

Basic Usage:
```python
    >>> from nodequery import NodeQuery
    >>> apikey = 'XXXXXXXXXXXXXXXXXXXXXXXX'
    >>> nq = NodeQuery(apikey)
    >>> accountStatus = nq.accountStatus()
    >>> print(accountStatus)
    {'name': 'Jeff Rescignano', 'timezone': -4, 'server_limit': 10, 'api': {'requests': 6, 'rate_limit': 180}}
```

Advanced Error Handling (See Error Handling):
```python
    >>> from nodequery import NodeQuery
    >>> apikey = 'XXXXXXXXXXXXXXXXXXXXXXXX'
    >>> nq = NodeQuery(apikey)
    >>> try:
    >>> 	accountStatus = nq.accountStatus()
    >>> 	print(accountStatus)
    >>> except Exception as error:
    >>> 	print(error)
```

# Available Endpoints
```python
    >>> from nodequery import NodeQuery
    >>> apikey = 'XXXXXXXXXXXXXXXXXXXXXXXX'
    >>> serverId = 'XXXXX'
    >>> loadType = 'hourly'
    >>> nq = NodeQuery(apikey)
    >>> nq.accountStatus()
    >>> nq.listServers()
    >>> nq.serverDetails(serverId)
    >>> nq.loads(loadType, serverId)
```
Each of these endpoint responses are reflect and documented by [NodeQuery's API](https://nodequery.com/help/developer-api)

# Error Handling
When an exception is triggered, the variable returned is the HTTP error code that occured during the API call (see HTTP Codes). If no valid response was recieved, the error code will be `0`. Each of the HTTP error codes that pertain to the [NodeQuery API](https://nodequery.com/help/developer-api) are documented in the HTTP Codes Section.

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
0.0.2
- Updated the error handling method
0.0.3
- Added API Key to class init


# About the API
The full API is documented here: https://nodequery.com/help/developer-api
