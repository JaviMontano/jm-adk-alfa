# Brand DOCX Scripts

`check.sh` runs deterministic JSON fixtures through `validate_brand_docx.py`.
The validator uses the Python standard library to build and inspect minimal
DOCX packages in memory, so the gate does not depend on network access or
installed Word processors.
