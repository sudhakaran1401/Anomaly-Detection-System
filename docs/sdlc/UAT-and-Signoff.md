# Smart Anomaly Detection & Classification Platform — User Acceptance Testing & Sign-off

## 1. Purpose
UAT verifies the end-user workflow of the running platform rather than merely verifying individual functions.

## 2. UAT Execution Record

**Execution date:** 2026-08-25  
**Execution basis:** Project owner/user confirmation that the listed workflows are working properly.

| ID | Scenario | Expected Result | Actual Result | Status |
|---|---|---|---|---|
| UAT-01 | Login with valid credentials | User enters application | Login completed and application accessible | PASS |
| UAT-02 | Upload valid CSV | Dataset is accepted | Valid CSV upload works correctly | PASS |
| UAT-03 | Upload invalid/non-CSV file | Validation error is shown | Invalid input is handled correctly | PASS |
| UAT-04 | Run Isolation Forest | Detection results are displayed | Results are generated correctly | PASS |
| UAT-05 | Run LOF | Detection results are displayed | Results are generated correctly | PASS |
| UAT-06 | Run One-Class SVM | Detection results are displayed | Results are generated correctly | PASS |
| UAT-07 | Run DBSCAN | Detection results are displayed | Results are generated correctly | PASS |
| UAT-08 | Review anomaly analytics | Counts, scores and charts are usable | Analytics are displayed correctly | PASS |
| UAT-09 | Review anomaly explanations | Reasons are displayed where generated | Explanations are displayed correctly | PASS |
| UAT-10 | Open detection history | User's history is available | History is accessible and usable | PASS |
| UAT-11 | Run classification | Classification metrics/results are displayed | Classification works correctly | PASS |
| UAT-12 | Review confusion matrix | Matrix/chart is displayed | Confusion matrix is displayed correctly | PASS |
| UAT-13 | Export anomaly result | CSV/PDF export works | Export functions work correctly | PASS |
| UAT-14 | Export classification report | Classification PDF works | Classification export works correctly | PASS |
| UAT-15 | Logout | User session/access is terminated | Logout works correctly | PASS |

## 3. Acceptance Criteria

- Authentication works.
- Supported CSV datasets can be processed.
- Detection models produce usable results.
- Classification produces metrics for labelled data.
- History is restricted to the authenticated user.
- Reports/exports work.
- No release-blocking functional issue was identified during the reported verification.

## 4. Sign-off

| Role | Name | Date | Result |
|---|---|---|---|
| Developer / Project Owner | | 2026-08-25 | PASS |
| Evaluator/Supervisor | | | Pending formal signature |

**UAT status: PASS based on the reported functional verification.**

This record does not claim a deployment smoke test, load test or stress test; those remain separate execution items.
