# Browser Compatibility Test Record

The Playwright configuration provides Chromium, Firefox and WebKit projects. The compatibility smoke suite exercises four viewport sizes and checks that the application renders without horizontal overflow.

Run:

```bash
npx playwright test e2e/compatibility.spec.js
```

For individual browser evidence:

```bash
npx playwright test e2e/compatibility.spec.js --project=chromium
npx playwright test e2e/compatibility.spec.js --project=firefox
npx playwright test e2e/compatibility.spec.js --project=webkit
```

| Browser | Login | Upload | Detection | History | Classification | Export |
|---|---|---|---|---|---|---|
| Chrome/Chromium | Pending execution | Pending | Pending | Pending | Pending | Pending |
| Firefox | Pending execution | Pending | Pending | Pending | Pending | Pending |
| WebKit/Safari engine | Pending execution | Pending | Pending | Pending | Pending | Pending |

Record browser version, OS, execution result and evidence for each executed environment. Microsoft Edge is available as an optional Playwright project when Edge is installed. Run it with `E2E_EDGE=1 npx playwright test e2e/compatibility.spec.js --project=edge`.
