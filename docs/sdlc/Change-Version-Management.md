# Smart Anomaly Detection & Classification Platform — Change & Version Management

## 1. Change Categories
- Feature/UI change
- anomaly algorithm/model change
- classification model change
- preprocessing/scaler change
- API change
- database change
- security change
- dependency change
- Docker/CI change
- documentation change

## 2. Change Workflow
Change/defect → impact analysis → implement → test → review → merge/version → deploy → verify → document.

## 3. ML Change Record
For an ML change record:
- model/algorithm
- parameter changes
- preprocessing/scaler changes
- affected datasets
- expected behavior impact
- benchmark result
- regression result
- release version

## 4. Versioning
Use Git history/tags or the project's release convention to identify stable baselines. Do not claim model-version management beyond the artifact/path information actually maintained by the application.

## 5. Database Changes
Update models/migrations, run migration checks, verify affected APIs and preserve recovery considerations.

## 6. Rollback
Return to the last known-good source/application/model artifact, verify persistent-data compatibility and rerun relevant tests.
