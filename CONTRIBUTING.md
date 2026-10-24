# Contributing to Neon Toolkit

Thanks for considering a contribution.

## Before opening a pull request

1. Explain the problem or improvement clearly.
2. Keep the tools compatible with Termux and ordinary non-root Android where practical.
3. Prefer Python standard-library features unless a dependency provides clear value.
4. Never add code that silently deletes files, collects credentials, bypasses Android locks, or probes systems without authorization.
5. Test the relevant script and describe the test environment and limitations.
6. Update the README when adding or changing a feature.

## Style

- Use descriptive names and small functions.
- Handle permission errors and unavailable Android APIs gracefully.
- Keep output understandable on narrow mobile terminals.
- Ask for confirmation before potentially overwriting user files.
- Do not commit tokens, private logs, personal documents, or other secrets.

## Pull requests

Use a concise title, explain why the change is useful, list the tests performed, and mention any known limitations. Small, focused pull requests are easier to review.
