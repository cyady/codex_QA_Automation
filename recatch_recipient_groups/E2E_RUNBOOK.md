# Re:catch E2E Runbook

This package is the current reference implementation for Re:catch recipient-group browser automation.

## Current Reference

- Main flow: `src/recatch_recipient_groups/segments.py`
- Browser helpers: `src/recatch_recipient_groups/browser.py`
- Login flow: `src/recatch_recipient_groups/auth.py`
- CLI entry: `src/recatch_recipient_groups/cli.py`

## Stable Practices

- Keep `teamSlug` in every direct page navigation.
- Prefer exact selectors or tag-restricted text clicks over broad text searches.
- Treat Ant overlays as separate DOM state.
- Wait for menu items and inputs to exist before clicking or typing.
- Add short settle delays after create, rename, and modal open when the UI is animation-heavy.

## Known Re:catch Pitfalls

- The filter-edit button label can exist on nested `div`, `button`, and `span` nodes. Clicking the wrapper may do nothing.
- The condition-add modal being open does not mean the operator menu is ready.
- Freshly created groups can be more timing-sensitive than older groups.
- Missing `teamSlug` can send the browser back to login.
- Vibium `26.3.11` was not stable against this target. Keep `vibium==0.1.8` unless the newer version is re-verified.

## Encoding Rules

- In checked-in Python files, UTF-8 Korean literals are acceptable.
- In PowerShell inline debug scripts, prefer unicode escapes such as `\uD544\uD130 \uC218\uC815`.
- Serialize strings into injected JavaScript with JSON escaping, not raw literals.
- When visible text and JS comparison disagree, assume string transport or shell encoding is broken before rewriting selectors.

## Suggested Workflow For New E2E

1. Reproduce the flow manually with browser tooling.
2. Identify the real clickable node and post-click state change.
3. Encode the flow with selector-first interactions.
4. Add explicit waits around every modal, overlay, or redirect.
5. Run one small end-to-end case first.
6. Scale out only after the one-case run is stable.

## Global Skill

- Reuse the global skill `recatch-e2e-korean-ui` for future Re:catch E2E work and Korean text debugging.
