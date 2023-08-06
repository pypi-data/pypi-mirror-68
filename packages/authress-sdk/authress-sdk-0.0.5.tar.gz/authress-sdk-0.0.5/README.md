# authress-sdk
Authress SDK for Python.

[![NuGet version](https://badge.fury.io/py/authress-sdk.svg)](https://badge.fury.io/py/authress-sdk) [![Build Status](https://travis-ci.com/authress/authress-sdk.py.svg?branch=master)](https://travis-ci.com/authress/authress-sdk.py)


## Usage

```sh
pip install authress-sdk
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git`)

Then import the package:
```python
import authress_sdk
```

## Getting Started

```python
from __future__ import print_function
import time
import authress_sdk
from authress_sdk.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = authress_sdk.AccessRecordsApi(authress_sdk.ApiClient(configuration))
body = authress_sdk.ClaimRequest() # ClaimRequest |

try:
    # Claim a resource by an allowed user
    api_response = api_instance.v1_claims_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccessRecordsApi->v1_claims_post: %s\n" % e)


# create an instance of the API class
api_instance = authress_sdk.AccessRecordsApi(authress_sdk.ApiClient(configuration))

try:
    # Get all account records.
    api_response = api_instance.v1_records_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccessRecordsApi->v1_records_get: %s\n" % e)


# create an instance of the API class
api_instance = authress_sdk.AccessRecordsApi(authress_sdk.ApiClient(configuration))
body = authress_sdk.AccessRecord() # AccessRecord |

try:
    # Create a new access record
    api_response = api_instance.v1_records_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccessRecordsApi->v1_records_post: %s\n" % e)


# create an instance of the API class
api_instance = authress_sdk.AccessRecordsApi(authress_sdk.ApiClient(configuration))
record_id = 'record_id_example' # str | The identifier of the access record.

try:
    # Deletes an access record.
    api_instance.v1_records_record_id_delete(record_id)
except ApiException as e:
    print("Exception when calling AccessRecordsApi->v1_records_record_id_delete: %s\n" % e)


# create an instance of the API class
api_instance = authress_sdk.AccessRecordsApi(authress_sdk.ApiClient(configuration))
record_id = 'record_id_example' # str | The identifier of the access record.

try:
    # Get an access record for the account.
    api_response = api_instance.v1_records_record_id_get(record_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccessRecordsApi->v1_records_record_id_get: %s\n" % e)


# create an instance of the API class
api_instance = authress_sdk.AccessRecordsApi(authress_sdk.ApiClient(configuration))
body = authress_sdk.AccessRecord() # AccessRecord |
record_id = 'record_id_example' # str | The identifier of the access record.

try:
    # Update an access record.
    api_response = api_instance.v1_records_record_id_put(body, record_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccessRecordsApi->v1_records_record_id_put: %s\n" % e)
```