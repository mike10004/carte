---
category: Types
title: '{{ type_name }}'

layout: nil
---

{{ summary }}

### Fields

{% for field in fields %}
* **{{ field.name }}** *{{ field.type }}* {{ field.description }}
{% endfor %}
