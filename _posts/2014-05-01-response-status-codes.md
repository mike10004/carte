---
title: 'Response status codes'

layout: nil
---

### Error

Error responses return 
[standard HTTP error codes](http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html) 
along with some additional information:

* The error code is sent back as a status header,
* The body has content type `application/json` and represents an object
  with the following fields:

For a call with an invalid authentication token for example:

    Status: 401 Access denied
    {
        code: 401,
        message: 'Access denied: invalid authentication token.'
    }

### Success

Responses to successful requests contain an HTTP status code in the 2xx
range and the response body varies dependening on the request.

* `GET`, `PUT`, and `DELETE` return `200 OK` on success
* `POST ` returns 201 on success
* `DELETE` returns 204 on success 

See documentation of individual endpoints for what to expect in the
response body.
