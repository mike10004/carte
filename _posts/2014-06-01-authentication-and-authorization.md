---
title: 'Authentication and Authorization'

layout: nil
---

Requests must be authenticated by providing an `Authorization` header
in the HTTP request. The header must be of the form

    Authorization: Bearer <token>

where `<token>` is a pre-defined access token distributed in a separate
channel.
