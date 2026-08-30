import { describe, expect, it, vi, beforeEach } from 'vitest';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import AnomalyDashboard from '../pages/Dashboard/Anomaly_dashboard';
import AnomalyService from '../services/AnomalyService';

vi.mock('../services/AnomalyService', () => ({ default: { downloadPDF: vi.fn(), downloadCSV: vi.fn() } }));
vi.mock('../components/dashboard/ChartSection', () => ({ default: () => <div>Charts</div> }));
vi.mock('../components/dashboard/MetricCards', () => ({ default: ({ total, normal, anomalies }) => <div>{total} total {normal} normal {anomalies} anomalies</div> }));
vi.mock('../components/dashboard/DataTable', () => ({ default: ({ rows }) => <div>Rows: {rows.length}</div> }));

describe('AnomalyDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    sessionStorage.setItem('anomalyResult', JSON.stringify({ filename: 'data.csv', total: 3, normal: 2, anomalies: 1, model_name: 'isolation_forest', scaler_type: 'standard', contamination: 0.01, data: [
      { feature: 'alpha', result: 'Anomaly' },
      { feature: 'beta', result: 'Normal' },
      { feature: 'gamma', result: 'Normal' },
    ] }));
  });

  it('renders dataset summary and filters rows', () => {
    render(<MemoryRouter><AnomalyDashboard /></MemoryRouter>);
    expect(screen.getByText('data.csv')).toBeInTheDocument();
    expect(screen.getByText(/3 total/)).toBeInTheDocument();
    expect(screen.getByText('Rows: 3')).toBeInTheDocument();

    fireEvent.click(screen.getByRole('button', { name: 'Anomalies' }));
    expect(screen.getByText('Rows: 1')).toBeInTheDocument();

    fireEvent.change(screen.getByPlaceholderText('Search...'), { target: { value: 'beta' } });
    expect(screen.getByText('Rows: 0')).toBeInTheDocument();
  });

  it('downloads CSV and PDF', async () => {
    AnomalyService.downloadCSV.mockResolvedValue({});
    AnomalyService.downloadPDF.mockResolvedValue({});
    render(<MemoryRouter><AnomalyDashboard /></MemoryRouter>);

    fireEvent.click(screen.getByRole('button', { name: 'CSV' }));
    await waitFor(() => expect(AnomalyService.downloadCSV).toHaveBeenCalled());
    expect(screen.getByRole('alert')).toHaveTextContent('CSV downloaded successfully.');

    fireEvent.click(screen.getByRole('button', { name: 'PDF' }));
    await waitFor(() => expect(AnomalyService.downloadPDF).toHaveBeenCalledWith(expect.objectContaining({ filename: 'data.csv' })));
  });

  it('deletes the stored dataset', () => {
    vi.useFakeTimers();
    render(<MemoryRouter><AnomalyDashboard /></MemoryRouter>);
    fireEvent.click(screen.getByRole('button', { name: 'Delete Dataset' }));
    expect(sessionStorage.getItem('anomalyResult')).toBeNull();
    expect(screen.getByRole('alert')).toHaveTextContent('Dataset deleted successfully.');
    vi.useRealTimers();
  });
});
