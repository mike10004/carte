---
category: {{ category }}
path: {{ path }}
title: '{{ title }}'
type: '{{ method }}'

layout: nil
---

{{ summary }}

### Request

#### Path parameters

{{ path_parameters | default('*None*', true) }}

#### Query parameters

{{ request_parameters | default('*None*', true) }}

#### Body

{{ request_body | default('*Empty*', true) }}

### Response

**Status:** Success is indicated by status `{{ response_code_success }}`.

**Content type:** {{ response_content_type | default('*N/A*', true) }}

**Body:** {{ response_body | default('*Empty*', true) }}

For error responses, see the [response status codes documentation](#/response-status-codes).
