import { describe, expect, it, vi, beforeEach } from 'vitest';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import History from '../pages/List/History';
import ThemeProvider from '../components/ThemeContext';
import AnomalyService from '../services/AnomalyService';

vi.mock('../services/AnomalyService', () => ({ default: { getHistory: vi.fn(), deleteHistory: vi.fn(), clearHistory: vi.fn() } }));

describe('History page', () => {
  beforeEach(() => vi.clearAllMocks());

  const renderHistory = () => render(<ThemeProvider><History /></ThemeProvider>);

  it('loads and displays history records', async () => {
    AnomalyService.getHistory.mockResolvedValue({ data: { results: [{ id: 1, filename: 'data.csv', model_name: 'isolation_forest', scaler_type: 'standard', contamination: 0.01, anomaly_count: 3, created_at: '2026-01-01T10:00:00Z' }] } });
    renderHistory();
    await waitFor(() => expect(screen.getByText('data.csv')).toBeInTheDocument());
    expect(screen.getByText('Detection History')).toBeInTheDocument();
    expect(screen.getByText('isolation_forest')).toBeInTheDocument();
    expect(screen.getByText('3')).toBeInTheDocument();
  });

  it('handles history loading failure', async () => {
    AnomalyService.getHistory.mockRejectedValue(new Error('network'));
    renderHistory();
    await waitFor(() => expect(screen.getByRole('alert')).toHaveTextContent('Failed to load history.'));
  });

  it('deletes a confirmed record', async () => {
    vi.spyOn(window, 'confirm').mockReturnValue(true);
    AnomalyService.getHistory.mockResolvedValue({ data: [{ id: 2, filename: 'remove.csv', model_name: 'lof', scaler_type: 'minmax', anomaly_count: 1, created_at: '2026-01-01T10:00:00Z' }] });
    AnomalyService.deleteHistory.mockResolvedValue({});
    renderHistory();
    await waitFor(() => expect(screen.getByText('remove.csv')).toBeInTheDocument());
    fireEvent.click(screen.getByRole('button', { name: 'Delete' }));
    await waitFor(() => expect(screen.getByRole('alert')) .toHaveTextContent('History deleted successfully.'));
  });

  it('clears all history', async () => { AnomalyService.getHistory .mockResolvedValueOnce({
      data: [
        {
          id: 3,
          filename: 'clear.csv',
          model_name: 'dbscan',
          scaler_type: 'robust',
          anomaly_count: 2,
          created_at: '2026-01-01T10:00:00Z',
        },
      ],
    })
    .mockResolvedValueOnce({ data: [], });

  AnomalyService.clearHistory.mockResolvedValue({});
  renderHistory();
  await waitFor(() => expect(screen.getByText('clear.csv')).toBeInTheDocument() );
  fireEvent.click( screen.getByRole('button', { name: /clear all/i }) );
  await waitFor(() => expect(AnomalyService.clearHistory).toHaveBeenCalled() );
  await waitFor(() => expect(screen.getByText('No history found.')).toBeInTheDocument() );
  });
});
