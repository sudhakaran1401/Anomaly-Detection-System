# Accessibility Test Record

## Automated checks

`testing/e2e/accessibility.spec.js` checks the login/application surface for:

- images with a missing `alt` attribute
- visible form controls without an accessible name
- invalid heading hierarchy
- unnamed visible buttons/links

Run with:

```bash
npx playwright test e2e/accessibility.spec.js
```

## Manual checks

| Check | Result | Evidence |
|---|---|---|
| Keyboard-only login | Pending execution | |
| Visible focus | Pending execution | |
| Form labels | Pending execution | |
| Heading hierarchy | Pending execution | |
| Color contrast | Pending execution | |
| Error messages | Pending execution | |
| Responsive/mobile layout | Pending execution | |

Automated checks do not replace the manual checks above. Record the actual result and evidence after testing the running UI.
