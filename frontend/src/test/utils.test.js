import { describe, expect, it, vi } from 'vitest';
import { getPerformanceInsight } from '../utils/performanceInsight';
import { downloadFile } from '../utils/downloadFile';

describe('performanceInsight', () => {
  it.each([
    [0.98, 'Excellent Model Performance', 'alert-success'],
    [0.90, 'Very Good Model Performance', 'alert-success'],
    [0.80, 'Good Model Performance', 'alert-warning'],
    [0.65, 'Fair Model Performance', 'alert-warning'],
    [0.40, 'Poor Model Performance', 'alert-danger'],
  ])('classifies average score %s correctly', (score, title, className) => {
    const insight = getPerformanceInsight({ accuracy: score, precision: score, recall: score, f1: score, roc_auc: score });
    expect(insight.title).toBe(title);
    expect(insight.className).toBe(className);
  });

  it('handles missing metrics as zero', () => {
    expect(getPerformanceInsight({}).title).toBe('Poor Model Performance');
  });
});

describe('downloadFile', () => {
  it('creates a downloadable link using the response filename', () => {
    const click = vi.fn();

    const appendChild = vi.spyOn(document.body, 'appendChild');
    const removeChild = vi.spyOn(document.body, 'removeChild');

    const anchor = document.createElement('a');
    vi.spyOn(anchor, 'click').mockImplementation(click);

    const createElement = vi
      .spyOn(document, 'createElement')
      .mockReturnValueOnce(anchor);

    downloadFile(
      {
        data: 'hello',
        headers: {
          'content-disposition':
            'attachment; filename="result.csv"',
        },
      },
      'default.csv',
      'text/csv',
    );

    expect(anchor.download).toBe('result.csv');
    expect(anchor.href).toBe('blob:mock-url');
    expect(click).toHaveBeenCalledOnce();
    expect(appendChild).toHaveBeenCalledWith(anchor);
    expect(removeChild).toHaveBeenCalledWith(anchor);

    createElement.mockRestore();
    appendChild.mockRestore();
    removeChild.mockRestore();
  });
});
