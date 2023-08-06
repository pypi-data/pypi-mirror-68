# oktajwt

This is a simple JWT package built to work specifically with Okta's API Access Management product (API AM). It was inspried in part by [jpadilla's PyJWT package](https://github.com/jpadilla/pyjwt). This is not meant to be a full implementation of [RFC 7519](https://tools.ietf.org/html/rfc7519), but rather a subset of JWT operations specific to working with Okta.

## Requirements
* Python >= 3.7

## Installing
Install with **pip**:
```
$ pip install OktaJWT
```

## Usage
This module has a command line interface:
```
usage:
    Decodes and verifies JWTs from an Okta authorization server.

    oktajwt [options] <JWT>


positional arguments:
  JWT                   The base64 encoded JWT to decode and verify

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -i ISSUER, --issuer ISSUER
                        The expected issuer of the token
  -a AUDIENCE, --audience AUDIENCE
                        The expected audience of the token
  -c CLIENT_ID, --client_id CLIENT_ID
                        The OIDC client ID
  -s CLIENT_SECRET, --client_secret CLIENT_SECRET
                        The OIDC client secret (not required if using PKCE)
```

However, it's much more likely that this package will be used inside something like an API server, so the
usage would look something more like this:

```python
import json
from oktajwt import JwtVerifier

issuer = "your OAuth issuer"
client_id = "OIDC client ID"
client_secret = "OIDC client secret or None if using PKCE"
expectedAudience = "expected audience"
accessToken = "your base64 encoded JWT, pulled out of the HTTP Authorization header bearer token"

jwtVerifier = JwtVerifier(issuer, client_id, client_secret)

# just check for validity, this includes checks on standard claims:
#   * signature is valid
#   * iss, aud, exp and iat claims are all present
#   * iat is <= "now"
#   * exp is >= "now"
#   * iss matches the expexted issuer
#   * aud matches the expected audience
if jwtVerifier.isTokenValid(accessToken, expectedAudience):
    print("Token is valid")
else:
    print("Token is not valid")

# check for validity and get verified claims
try:
    claims = jwtVerifier.verifyAccessToken(accessToken, expectedAudience)
    print("Verified claims: {0}".format(json.dumps(claims, indent=4, sort_keys=True)))
except Exception as e:
    print("There was a problem verifying the token: ", e)
```

## Okta Configuration
**Okta Org**
You need to have an Okta org with API Access management available. You can get a free developer account at https://developer.okta.com.

**NOTE:**, this package will **NOT** work with the "stock" organization authorization server as access tokens minted by that server are opaque (and no public key is published).

**Create an OIDC Application**
Create a new OIDC application in Okta. This is where you'll get the client ID and client secret values. If you create an app that uses PKCE, a client secret value is not necessary and will not be generated.