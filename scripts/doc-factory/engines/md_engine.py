"""Markdown Engine — Jinja2 template rendering for markdown documents."""

from pathlib import Path

from generate import register_engine
from runtime import display_timestamp

DEFAULT_TEMPLATE = """# {{ title | default('Document') }}

{% if folio %}**{{ folio }}**{% endif %}
{% if date %}**Fecha**: {{ date }}{% endif %}
{% if client_name %}**Para**: {{ client_name }}{% endif %}

---

{% if sections %}
{% for section in sections %}
## {{ section.title }}

{{ section.content }}

{% endfor %}
{% endif %}

{% if items %}
## Detalle

| # | Descripcion | Cantidad | Precio | Total |
|---|-------------|----------|--------|-------|
{% for item in items %}
| {{ loop.index }} | {{ item.description }} | {{ item.quantity }} | {{ item.unit_price }} | {{ "%.2f" | format(item.quantity * item.unit_price) }} |
{% endfor %}

{% if total %}**Total: {{ currency | default('$') }} {{ "%.2f" | format(total) }}**{% endif %}
{% endif %}

{% if content %}
{{ content }}
{% endif %}

---

*{% if folio %}{{ folio }} | {% endif %}Generado {{ _generated_at }}*
"""


@register_engine('md')
class MdEngine:
    def generate(self, data, template_path, output_path, schema=None):
        try:
            from jinja2 import Template, Environment, FileSystemLoader
        except ImportError:
            raise RuntimeError("jinja2 required: pip install jinja2")

        render_data = {**data, '_generated_at': display_timestamp()}

        if 'items' in render_data and 'total' not in render_data:
            render_data['total'] = sum(
                i.get('quantity', 0) * i.get('unit_price', 0)
                for i in render_data['items']
            )

        if template_path and Path(template_path).exists():
            tmpl_dir = Path(template_path).parent
            tmpl_name = Path(template_path).name
            env = Environment(loader=FileSystemLoader(str(tmpl_dir)))
            template = env.get_template(tmpl_name)
        else:
            template = Template(DEFAULT_TEMPLATE)

        md = template.render(**render_data)

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md)
