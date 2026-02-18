# vibium-python-automation-guide.md

## Scope

Define how to build reusable browser tests with Vibium and Python without Selenium.

## 1) MCP + Skills Setup

- Keep MCP server: `npx vibium mcp` in `C:\Users\syh\.codex\config.toml`.
- Add custom skill: `vibium-python-automation`.
- Use skill references for coding rules and LLM behavior.

## 2) Vibium-Optimized Coding Rules

- Use Vibium only (CLI or MCP).
- Add explicit waits before assertions on async pages.
- Prefer `data-testid` selectors.
- Save screenshots with `shot-YYYYMMDD-HHmmss.png`.
- Block forbidden stacks: Selenium/WebDriver/Playwright.

## 3) LLM Action Design Guideline

- Discovery phase: run flow with MCP once.
- Freeze phase: convert flow into deterministic Python test.
- Verify phase: assert user outcome and save artifact.
- Guard phase: scan output for forbidden framework keywords.

## Minimal template

```bash
npx vibium navigate <url>
npx vibium text
npx vibium screenshot -o shot-<timestamp>.png
```

```bash
python C:\Users\syh\.codex\skills\vibium-python-automation\scripts\new_vibium_test.py --name smoke-home --url https://example.com
```
