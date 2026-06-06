# Brand XLSX Scripts

`check.sh` runs deterministic JSON fixtures through `validate_brand_xlsx.py`.
The validator uses the Python standard library to build and inspect minimal
XLSX packages in memory, so the gate does not depend on network access or
installed Excel/openpyxl.
