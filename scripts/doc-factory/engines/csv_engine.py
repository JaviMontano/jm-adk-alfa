"""CSV Engine — Structured CSV generation from data arrays."""

import csv
from pathlib import Path

from generate import register_engine


@register_engine('csv')
class CsvEngine:
    def generate(self, data, template_path, output_path, schema=None):
        """
        Generate CSV from data.

        Expected data formats:
        1. {"headers": ["A", "B"], "rows": [[1, 2], [3, 4]]}
        2. {"items": [{"col1": "val1", "col2": "val2"}, ...]}
        3. {"records": [{"col1": "val1"}, ...]}  (alias for items)
        """
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)

            # Format 1: explicit headers + rows
            if 'headers' in data and 'rows' in data:
                writer.writerow(data['headers'])
                writer.writerows(data['rows'])

            # Format 2/3: list of dicts
            elif 'items' in data or 'records' in data:
                items = data.get('items', data.get('records', []))
                if not items:
                    return

                # Use schema field order if available, otherwise dict keys
                if schema and 'properties' in schema:
                    # Get item schema
                    item_schema = schema.get('properties', {}).get('items', {}).get('items', {})
                    if 'properties' in item_schema:
                        headers = list(item_schema['properties'].keys())
                    else:
                        headers = list(items[0].keys())
                else:
                    headers = list(items[0].keys())

                writer.writerow(headers)
                for item in items:
                    writer.writerow([item.get(h, '') for h in headers])

            else:
                raise ValueError("CSV data must have 'headers'+'rows', 'items', or 'records' key")
