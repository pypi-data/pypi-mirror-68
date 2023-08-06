# NOTE :   This repo is planned to be sunset by May 31st 2020,  new SDK is available at https://pypi.org/manage/project/ibm-cloud-security-advisor/releases/






# ibm_security_advisor_findings_api_sdk

This repository contains the released Python client SDK for IBM Cloud Security Advisor Findings API . Check out our [API
documentation](https://cloud.ibm.com/apidocs/security-advisor/findings) for more details.

## Notice

Support for Python versions 2.x and versions <= 3.4 is deprecated and will be officially dropped in the next major release, which is expected to be end of December, 2019. Refer https://github.com/IBM/python-sdk-core 

## Overview


The  ibm_security_advisor_findings_api_sdk Python SDK allows developers to programmatically interact with the ibm cloud security advisor findings api

## Prerequisites

[ibm-cloud-onboarding]: https://cloud.ibm.com/registration?target=%2Fdeveloper%2Fwatson&

* An [IBM Cloud][ibm-cloud-onboarding] account.
* An IAM API key to allow the SDK to access your account. Create one [here](https://cloud.ibm.com/iam/apikeys).
* An installation of Python >=3.5 on your local machine.

## Installation

To install, use `pip` or `easy_install`:

```bash
pip install --upgrade "ibm-cloud-security-advisor-findingsapi-sdk>=2.0.0"
```

or

```bash
easy_install --upgrade " ibm-cloud-security-advisor-findingsapi-sdk>=2.0.0"
```

## Authentication

 ibm_security_advisor_findings_api_sdk uses token-based [Identity and Access Management (IAM) authentication](https://cloud.ibm.com/docs/iam?topic=iam-getstarted).

IAM authentication uses a service API key to get an access token that is passed with the call.
Access tokens are valid for a limited amount of time and must be regenerated.

To provide credentials to the SDK, you supply either an IAM service **API key** or an **access token**:

- Use the API key to have the SDK manage the lifecycle of the access token. The SDK requests an access token, ensures that the access token is valid, and refreshes it if necessary.
- Use the access token if you want to manage the lifecycle yourself. For details, see [Authenticating with IAM tokens](https://cloud.ibm.com/docs/services/watson/getting-started-iam.html).


### Supplying the IAM API key:


```python
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
authenticator = IAMAuthenticator('apikey')
ibm_security_advisor_findings_api_sdk_service =  ibm_security_advisor_findings_api_sdk(authenticator=authenticator)
```

### Generating bearer tokens using the IAM API key:

```python
from  ibm_security_advisor_findings_api_sdk import IAMAuthenticator
# In your API endpoint use this to generate new bearer tokens
iam_token_manager = IAMAuthenticator('<apikey>')
token = iam_token_manager.get_token()
```

### Supplying the access token:

```python
from ibm_security_advisor_findings_api_sdk import FindingsApiV1 
from ibm_cloud_sdk_core.authenticators import BearerTokenAuthenticator
# in the constructor, assuming control of managing the token
authenticator = BearerTokenAuthenticator('your token')
ibm_security_advisor_findings_api_sdk_service =  FindingsApiV1(authenticator=authenticator)
```

## Using the SDK

The  ibm_security_advisor_findings_api_sdk Python SDK supports only synchronous (blocking) execution of service methods. The return value from all service methods is a DetailedResponse object. Use this SDK to perform the basic  ibm_security_advisor_findings_api_sdk creation operation as follows, with the installation and initialization instructions from above:

```python
from ibm_security_advisor_findings_api_sdk import FindingsApiV1 
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
authenticator = IAMAuthenticator('your apikey')
ibm_security_advisor_findings_api_sdk_data =  FindingsApiV1(authenticator=authenticator)
response =  ibm_security_advisor_findings_api_sdk_data.<Method here<>>
print(response)
```

This would give an output of `DetailedResponse` from which you can use the `get_result()`, `get_headers()`, and `get_status_code()` to return the result, headers, and status code respectively.

### Sending request headers

Custom headers can be passed in any request in the form of a `dict` as:

```python
headers = {
'Custom-Header': 'custom_value'
}
```

For example, to send a header called `Custom-Header` to a call in  ibm_security_advisor_findings_api_sdk, pass the headers parameter as:

```python
from ibm_security_advisor_findings_api_sdk import FindingsApiV1 
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
authenticator = IAMAuthenticator('your apikey')
ibm_security_advisor_findings_api_sdk_service =  FindingsApiV1(authenticator=authenticator)
response = ibm_security_advisor_findings_api_sdk_service.<<METHOD HERE>>(headers={'Custom-Header': 'custom_value'}).get_result()
```

### Error Handling

The  ibm_security_advisor_findings_api_sdk Python SDK generates an exception for any unsuccessful method invocation.
If the method receives an error response from an API call to the service, it will generate an
`ApiException` with the following fields.

| NAME | DESCRIPTION |
| ----- | ----------- |
| code | The HTTP response code that is returned. |
| message	| A message that describes the error. |
| info	| A dictionary of additional information about the error. |

`ApiException` can be handled this way.

```python
from ibm_cloud_sdk_core.api_exception import ApiException
try:
    response = ibm_security_advisor_findings_api_sdk.create_note(
        account_id="<<Account ID here>>",
        **data
        )
except ApiException as err:
    try:
        # err.code  gives status code
        excep_resp = err.http_response.json()
        print(excep_resp)
    except:
        print(err)
```
excep_resp would be-
```json
{
  "detail": "Document already exists: abc/providers/sdktest/notes/sdk_note_id1",
  "instance": "abc/providers/sdktest/notes/sdk_note_id1",
  "status": 409,
  "title": "Conflict",
  "type": "about:blank"
}
```

### Error log level
By default, error log level is disabled, so user will not see any error/exception logged by `logger.error` and `logger.exception` but will see other error/exception.
To enable it, user can pass `enable_error_log=True` .
```python
ibm_security_advisor_findings_api_sdk =FindingsApiV1(authenticator=authenticator,enable_error_log=True)
```


## Sample Code

Example | http method  
------------ | ------------- 
[***post_graph***](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/samples/post_graph.py) | POST /v1/{account_id}/graph 
[***list_providers***](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/samples/list_providers.py) | GET /v1/{account_id}/providers
[***create_finding***](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/samples/create_finding.py) | POST /v1/{account_id}/providers/{provider_id}/notes
[***create_card***](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/samples/create_card.py) | POST /v1/{account_id}/providers/{provider_id}/notes
[***create_note_with_kpi***](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/samples/create_note_with_kpi.py) | POST /v1/{account_id}/providers/{provider_id}/notes
[***create_note_with_reporter***](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/samples/create_note_with_reporter.py) | POST /v1/{account_id}/providers/{provider_id}/notes
[***create_note_with_section***](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/samples/create_note_with_section.py) | POST /v1/{account_id}/providers/{provider_id}/notes
[***list_notes***](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/samples/list_notes.py) | GET /v1/{account_id}/providers/{provider_id}/notes
[***delete_note***](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/samples/delete_note.py) | DELETE /v1/{account_id}/providers/{provider_id}/notes/{note_id}
[***create_occurrence***](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/samples/create_occurrence.py) | POST /v1/{account_id}/providers/{provider_id}/occurrences
[***create_occurrence_with_context***](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/samples/create_occurrence_with_context.py) | POST /v1/{account_id}/providers/{provider_id}/occurrences
[***create_occurrence_with_kpi***](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/samples/create_occurrence_with_kpi.py) | POST /v1/{account_id}/providers/{provider_id}/occurrences
[***list_occurrences***](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/samples/list_occurrences.py) | GET /v1/{account_id}/providers/{provider_id}/occurrences
[***delete_occurrence***](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/samples/delete_occurrence.py) | DELETE /v1/{account_id}/providers/{provider_id}/occurrences/{occurrence_id}
[***list_note_occurrences***](https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python/blob/master/samples/list_note_occurrences.py) | GET /v1/{account_id}/providers/{provider_id}/notes/{note_id}/occurrences




## Documentation
See [Findings API doc](https://ibm-cloud-security.github.io/security-advisor-findings-sdk-python/docs/findings_api_v1.html#FindingsApiV1).

## Integration test
To run pytest, create virtual env and then run. Otherwise you might see below error

issue - https://github.com/pytest-dev/pytest/issues/2287
```
Traceback:
test/integration/test_note.py:26: in <module>
    from ibm_security_advisor_findings_api_sdk import FindingsApiV1
   ModuleNotFoundError: No module named 'ibm_security_advisor_findings_api_sdk'
```
1. Install dev modules.
    ```bash
    python3 -m venv env  #(for python3)
    source env/bin/activate
    cd security-advisor-findings-sdk-python
    pip install -r requirements-dev.txt
    ```
2. Prereq variables, either by exporting all the variables directly or provide in file-
*Make sure `API_KEY` has enough permission to perform findings api operations.*
    - export env vars 
    ```bash
        export API_KEY=<YOUR_API_KEY>
        export ACCOUNT_ID=<YOUR_ACCOUNT_ID>
        export FINDING_API_ENDPOINT=<FINDING_API_ENDPOINT>
        #optional. Use it for dev/preprod iam endpoint
        export IAM_ENDPOINT= <IAM_ENDPOINT>
    ```
    - provide in `/integration/input/cred/ibm-credentials.env` file or export your own `.env` credential file with full path including filename.
    ```bash
        export IBM_CREDENTIALS_FILE= <file_path>
    ```
1. To run test-


```bash
python -m pytest test/integration --html=report.html --json-report --json-report-summary

```
Once run is completed, html report and .report.json will be generated in the same directory and it will look like this

![Integration Test result](pytest_report.png?raw=true )



## License

The ibm_security_advisor_findings_api_sdk Python SDK is released under the Apache 2.0 license. The license's full text can be found in [LICENSE](LICENSE).

