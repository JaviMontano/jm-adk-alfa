# Example Output

## Summary

[CODE] schema=input-analysis-output.v1 selected_passes=surface, five_whys,
seven_so_whats, intent, reformulation

## Surface Errors

- [CODE] Corrected text: i need something for the meeting tmrw about that thing we talked about
- [CODE] transposition `\bteh\b` -> `the` confidence=very_high
- [CODE] misspelling `\bsomthing\b` -> `something` confidence=high
- [INFERENCE] `tmrw` is likely an intentional abbreviation; flag instead of autocorrecting.

## Intent Gap Analysis

- [INFERENCE] context gap evidence=`that`, `thing`, `meeting`
- [OPEN] What specific object, meeting, change, or artifact does the request refer to?

## Clarified Prompt

[INFERENCE] Clarify the missing context before executing: identify the specific
artifact, audience, deadline, expected output, and success criteria.

## Validation

- [CODE] `routing_hints.next_action=ask_clarification`
- [CODE] `user_safety_privacy_flags.external_api_required=false`
- [CODE] `confidence.overall=medium`
