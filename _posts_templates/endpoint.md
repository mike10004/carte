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

{% if path_parameters|length == 0 %}
*None*
{% else %}
  {% for p in path_parameters %}
* **{{ p.name }}** *{{ p.type | default('untyped', true) }}* {{ p.description }}
  {% endfor %}
{% endif %}

#### Query parameters

{% if query_parameters|length == 0 %}
*None*
{% else %}
  {% for p in query_parameters %}
* **{{ p.name }}** *{{ p.type }}* {{ p.description }}
  {% endfor %}
{% endif %}

#### Body

{{ request_body | default('*Empty*', true) }}

### Response

**Status:** Success is indicated by status `{{ response_code_success }}`.

**Content type:** {{ response_content_type | default('*N/A*', true) }}

**Body:** {{ response_body | default('*Empty*', true) }}

For error responses, see the [response status codes documentation](#/response-status-codes).
