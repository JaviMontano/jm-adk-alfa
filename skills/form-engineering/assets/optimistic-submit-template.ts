type SubmitState = "idle" | "pending" | "succeeded" | "failed";

export async function submitWithOptimism<TPayload>(
  payload: TPayload,
  submit: (payload: TPayload, idempotencyKey: string) => Promise<void>,
  setState: (state: SubmitState) => void,
  setError: (message: string | null) => void,
) {
  const idempotencyKey = crypto.randomUUID();
  setState("pending");
  setError(null);
  try {
    await submit(payload, idempotencyKey);
    setState("succeeded");
  } catch (error) {
    setState("failed");
    setError(error instanceof Error ? error.message : "Submission failed. Retry with the same saved draft.");
  }
}
