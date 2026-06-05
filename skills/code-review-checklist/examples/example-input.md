# Example Input

Run a standard PR checklist on this Firebase/TypeScript diff. The PR intent is
to load recent orders for an authenticated dashboard. [CONFIG]

```diff
diff --git a/src/orders/loadOrders.ts b/src/orders/loadOrders.ts
@@
+export async function loadOrders(db: Firestore) {
+  const snap = await getDocs(query(collection(db, "orders")));
+  return snap.docs.map((doc) => doc.data() as any);
+}
```

Additional evidence:

```text
npm audit: 0 high, 0 critical
pytest/js tests: not supplied
Firestore rules: not supplied
```
