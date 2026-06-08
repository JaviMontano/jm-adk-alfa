# Cierre Conversacion Meta Prompt

Decide whether this request is a real closeout.

## Activate When

- The user explicitly asks to close, audit, harvest, summarize for handoff, or end a long conversation.
- The current workflow requires a final ReleasePacket, retrospective, or next-session handoff.
- The conversation has accumulated enough state that losing decisions, risks, or validations would harm continuity.

## Do Not Activate When

- The request is only generic cleanup of files or downloads.
- The user wants a normal short summary with no closure or handoff.
- A more specific active skill must finish first.

## Routing Output

Return activation decision, evidence, missing authority for durable writes, and whether Guardian should start in `pass` or `block` posture.
