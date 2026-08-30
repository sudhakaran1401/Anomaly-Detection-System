import { describe, expect, it, vi, beforeEach } from 'vitest';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import Home from '../pages/Main/Home';
import ThemeProvider from '../components/ThemeContext';
import AnomalyService from '../services/AnomalyService';
import ClassificationService from '../services/ClassificationService';

vi.mock('../services/AnomalyService', () => ({ default: { analyzeDataset: vi.fn() } }));
vi.mock('../services/ClassificationService', () => ({ default: { classifyDataset: vi.fn() } }));
const navigate = vi.fn();
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return { ...actual, useNavigate: () => navigate };
});

describe('Home upload page', () => {
  beforeEach(() => vi.clearAllMocks());
  const renderHome = () => render(<MemoryRouter><ThemeProvider><Home /></ThemeProvider></MemoryRouter>);

  it('warns when no CSV is selected', () => {
    renderHome();
    fireEvent.click(screen.getByRole('button', { name: 'Upload & Analyze' }));
    expect(screen.getByRole('alert')).toHaveTextContent('Please select a CSV file.');
    expect(AnomalyService.analyzeDataset).not.toHaveBeenCalled();
  });

  it('uploads an anomaly dataset and navigates to dashboard', async () => {
    AnomalyService.analyzeDataset.mockResolvedValue({ data: { data: { filename: 'sample.csv', total: 2, normal: 1, anomalies: 1, data: [] } } });
    renderHome();
    const file = new File(['a,b\n1,2'], 'sample.csv', { type: 'text/csv' });
    fireEvent.change(document.querySelector('input[accept=".csv"]'), { target: { files: [file] } });
    fireEvent.click(screen.getByRole('button', { name: 'Upload & Analyze' }));

    await waitFor(() => expect(AnomalyService.analyzeDataset).toHaveBeenCalled());
    expect(sessionStorage.getItem('anomalyResult')).toContain('sample.csv');
    expect(navigate).toHaveBeenCalledWith('/dashboard');
  });

  it('routes classification models to classification service', async () => {
    ClassificationService.classifyDataset.mockResolvedValue({ data: { result: { id: 1 } } });
    renderHome();
    const file = new File(['x,y\n1,A'], 'classification.csv', { type: 'text/csv' });
    fireEvent.change(document.querySelector('input[accept=".csv"]'), { target: { files: [file] } });
    const select = screen.getAllByRole('combobox')[0];
    fireEvent.change(select, { target: { value: 'logistic_regression' } });
    fireEvent.click(screen.getByRole('button', { name: 'Upload & Analyze' }));

    await waitFor(() => expect(ClassificationService.classifyDataset).toHaveBeenCalled());
    expect(sessionStorage.getItem('classificationResult')).toContain('id');
    expect(navigate).toHaveBeenCalledWith('/classification');
  });

  it('shows backend errors', async () => {
    AnomalyService.analyzeDataset.mockRejectedValue({ response: { data: { message: 'Invalid dataset' } } });
    renderHome();
    const file = new File(['bad'], 'bad.csv', { type: 'text/csv' });
    fireEvent.change(document.querySelector('input[accept=".csv"]'), { target: { files: [file] } });
    fireEvent.click(screen.getByRole('button', { name: 'Upload & Analyze' }));
    await waitFor(() => expect(screen.getByRole('alert')).toHaveTextContent('Invalid dataset'));
  });
});
