import { describe, expect, it } from 'vitest';
import { ANOMALY_MODELS, CLASSIFICATION_MODELS } from '../constants/models';

describe('model constants', () => {
  it('contains supported anomaly models', () => {
    expect(ANOMALY_MODELS.map((m) => m.value)).toEqual(['isolation_forest', 'lof', 'svm', 'dbscan']);
  });

  it('contains supported classification models', () => {
    expect(CLASSIFICATION_MODELS.map((m) => m.value)).toEqual(['random_forest', 'logistic_regression', 'decision_tree', 'xgboost']);
  });
});
