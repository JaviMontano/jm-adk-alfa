"""HTML Engine — Jinja2 template rendering for branded HTML documents."""

from pathlib import Path

from generate import register_engine
from runtime import display_timestamp

# Default HTML template when no template file is provided
DEFAULT_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{ title | default('Document') }}</title>
<style>
  body { font-family: 'Segoe UI', Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 40px; color: #1a1a2e; line-height: 1.6; }
  h1 { color: #16213e; border-bottom: 3px solid #16213e; padding-bottom: 10px; }
  h2 { color: #16213e; margin-top: 30px; }
  table { width: 100%; border-collapse: collapse; margin: 15px 0; }
  th { background: #16213e; color: white; padding: 8px 12px; text-align: left; }
  td { padding: 6px 12px; border: 1px solid #ddd; }
  tr:nth-child(even) { background: #f9f9f9; }
  .header { text-align: center; margin-bottom: 30px; }
  .meta { background: #f5f5f5; padding: 15px; border-radius: 4px; margin: 15px 0; }
  .footer { text-align: center; font-size: 11px; color: #999; margin-top: 40px; border-top: 1px solid #e0e0e0; padding-top: 10px; }
  .amount { font-size: 20px; font-weight: bold; color: #16213e; }
  ul { padding-left: 20px; }
  li { margin: 5px 0; }
</style>
</head>
<body>
{% if folio %}<div class="header"><small>{{ folio }}</small></div>{% endif %}
<h1>{{ title | default('Document') }}</h1>
{% if date %}<div class="meta"><strong>Fecha:</strong> {{ date }}{% if client_name %} | <strong>Para:</strong> {{ client_name }}{% endif %}</div>{% endif %}

{% if sections %}
{% for section in sections %}
<h2>{{ section.title }}</h2>
<p>{{ section.content }}</p>
{% endfor %}
{% endif %}

{% if items %}
<h2>Detalle</h2>
<table>
<thead><tr><th>#</th><th>Descripcion</th><th>Cantidad</th><th>Precio</th><th>Total</th></tr></thead>
<tbody>
{% for item in items %}
<tr><td>{{ loop.index }}</td><td>{{ item.description }}</td><td>{{ item.quantity }}</td><td>{{ item.unit_price }}</td><td>{{ "%.2f" | format(item.quantity * item.unit_price) }}</td></tr>
{% endfor %}
</tbody>
</table>
{% endif %}

{% if content %}
{{ content }}
{% endif %}

{% if total %}<div class="meta"><span class="amount">Total: {{ currency | default('$') }} {{ "%.2f" | format(total) }}</span></div>{% endif %}

<div class="footer">
{% if folio %}Documento {{ folio }} | {% endif %}Generado {{ _generated_at }}
</div>
</body>
</html>"""


@register_engine('html')
class HtmlEngine:
    def generate(self, data, template_path, output_path, schema=None):
        try:
            from jinja2 import Template, Environment, FileSystemLoader
        except ImportError:
            raise RuntimeError("jinja2 required: pip install jinja2")

        # Add metadata to data
        render_data = {**data, '_generated_at': display_timestamp()}

        # Compute totals if items exist
        if 'items' in render_data and 'total' not in render_data:
            render_data['total'] = sum(
                i.get('quantity', 0) * i.get('unit_price', 0)
                for i in render_data['items']
            )
        # Compute subtotal, tax, grand_total for invoice templates
        if 'items' in render_data:
            render_data.setdefault('subtotal', render_data.get('total', 0))
            tax_rate = render_data.get('tax_rate', 0)
            render_data.setdefault('tax_amount', render_data['subtotal'] * tax_rate)
            render_data.setdefault('grand_total', render_data['subtotal'] + render_data.get('tax_amount', 0))

        if template_path and Path(template_path).exists():
            tmpl_dir = Path(template_path).parent
            tmpl_name = Path(template_path).name
            tmpl_content = Path(template_path).read_text(encoding='utf-8')

            # Auto-convert Handlebars syntax to Jinja2 if detected
            if '{{#' in tmpl_content or '{{/' in tmpl_content:
                import re
                tmpl_content = re.sub(r'\{\{#each\s+(\w+)\}\}', r'{% for item in \1 %}', tmpl_content)
                tmpl_content = tmpl_content.replace('{{/each}}', '{% endfor %}')
                tmpl_content = re.sub(r'\{\{this\.(\w+)\}\}', r'{{ item.\1 }}', tmpl_content)
                tmpl_content = tmpl_content.replace('{{this}}', '{{ item }}')
                tmpl_content = re.sub(r'\{\{@index_plus_one\}\}', '{{ loop.index }}', tmpl_content)
                # {{#if x}}...{{/if}}
                tmpl_content = re.sub(r'\{\{#if\s+([\w.]+)\}\}', r'{% if \1 %}', tmpl_content)
                tmpl_content = tmpl_content.replace('{{/if}}', '{% endif %}')
                template = Template(tmpl_content)
            else:
                env = Environment(loader=FileSystemLoader(str(tmpl_dir)))
                template = env.get_template(tmpl_name)
        else:
            template = Template(DEFAULT_TEMPLATE)

        html = template.render(**render_data)

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
