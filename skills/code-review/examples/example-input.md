# Example Input

Review this pull request diff at standard depth. The intent is to prevent
anonymous users from updating billing addresses. [CONFIG]

```diff
diff --git a/app/billing/address.py b/app/billing/address.py
@@
 def update_billing_address(user, address):
-    if user is None:
-        raise PermissionError("login required")
     normalized = normalize_address(address)
     save_address(user.id, normalized)
     return normalized
```

Validation supplied by the author:

```text
pytest tests/billing/test_address.py::test_update_billing_address_success passed
```
