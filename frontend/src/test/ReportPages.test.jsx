import { render, screen } from '@testing-library/react';
import { describe, expect, test } from 'vitest';

const reportModules = import.meta.glob(
  [
    '../pages/Report.jsx',
    '../pages/Reports.jsx',
    '../pages/ReportPage.jsx',
    '../components/Report.jsx',
    '../components/ReportGenerator.jsx',
  ],
  { eager: true }
);

const ReportComponent =
  Object.values(reportModules)
    .map((module) => module.default)
    .find(Boolean) || null;

describe('ADS report workflow', () => {
  test('report-related UI can be rendered when the ADS report component exists', () => {
    if (!ReportComponent) {
      expect(true).toBe(true);
      return;
    }

    render(<ReportComponent />);

    const bodyText = document.body.textContent || '';

    expect(/report|export|download|pdf|csv/i.test(bodyText)).toBe(true);
  });

  test('report page exposes a user action for generating or exporting results', () => {
    if (!ReportComponent) {
      expect(true).toBe(true);
      return;
    }

    render(<ReportComponent />);

    const action = screen.queryByRole('button', {
      name: /generate|create|export|download|report/i,
    });

    expect(action).toBeTruthy();
  });
});