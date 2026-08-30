import { describe, expect, it, vi, beforeEach } from 'vitest';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import ClassificationDashboard from '../pages/Dashboard/Classification_dashboard';
import ClassificationService from '../services/ClassificationService';

vi.mock('../services/ClassificationService', () => ({ default: { getResults: vi.fn(), downloadPDF: vi.fn() } }));
vi.mock('../components/dashboard/ConfusionMatrix', () => ({ default: ({ matrix }) => <div>Matrix {matrix[0][0]}</div> }));
vi.mock('../components/dashboard/DetectionSummary', () => ({ default: ({ summary }) => <div>Summary {summary.total_records}</div> }));
vi.mock('../components/dashboard/MetricGrid', () => ({ default: ({ metrics }) => <div>Accuracy {metrics.accuracy}</div> }));
vi.mock('../components/dashboard/InsightCard', () => ({ default: ({ insight }) => <div>{insight.title}</div> }));
vi.mock('../components/dashboard/DatasetCard', () => ({ default: ({ filename, modelName }) => <div>{filename} {modelName}</div> }));
vi.mock('../components/dashboard/Actions', () => ({ default: ({ onUpload, onDownload }) => <><button onClick={onUpload}>Upload</button><button onClick={onDownload}>Download</button></> }));
const navigate = vi.fn();
vi.mock('react-router-dom', async () => { const actual = await vi.importActual('react-router-dom'); return { ...actual, useNavigate: () => navigate }; });

describe('ClassificationDashboard', () => {
  beforeEach(() => vi.clearAllMocks());

  it('renders latest classification result', async () => {
    ClassificationService.getResults.mockResolvedValue({ data: { success: true, results: [{ id: 9, file_name: 'train.csv', model_name: 'random_forest', target_column: 'target', accuracy: 0.91, precision: 0.9, recall: 0.89, f1_score: 0.895, roc_auc: 0.93, confusion_matrix: [[8,1],[2,9]], summary: { total_records: 20 }, dataset_summary: {}, confusion_matrix_chart: 'matrix.png' }] } });
    render(<MemoryRouter><ClassificationDashboard /></MemoryRouter>);
    await waitFor(() => expect(screen.getByText(/train.csv/)).toBeInTheDocument());
    expect(screen.getByText(/Random Forest/)).toBeInTheDocument();
    expect(screen.getByText('Accuracy 0.91')).toBeInTheDocument();
  });

  it('shows no-result state', async () => {
    ClassificationService.getResults.mockResolvedValue({ data: { success: true, results: [] } });
    render(<MemoryRouter><ClassificationDashboard /></MemoryRouter>);
    await waitFor(() => expect(screen.getByText('No Classification Result Found')).toBeInTheDocument());
  });

  it('downloads the latest PDF', async () => {
    ClassificationService.getResults.mockResolvedValue({ data: { success: true, results: [{ id: 9, file_name: 'train.csv', model_name: 'random_forest', target_column: 'target', accuracy: 0.91, precision: 0.9, recall: 0.89, f1_score: 0.895, roc_auc: 0.93, confusion_matrix: [[8,1],[2,9]], summary: { total_records: 20 }, dataset_summary: {}, confusion_matrix_chart: 'matrix.png' }] } });
    ClassificationService.downloadPDF.mockResolvedValue({});
    render(<MemoryRouter><ClassificationDashboard /></MemoryRouter>);
    await waitFor(() => expect(screen.getByRole('button', { name: 'Download' })).toBeInTheDocument());
    fireEvent.click(screen.getByRole('button', { name: 'Download' }));
    await waitFor(() => expect(ClassificationService.downloadPDF).toHaveBeenCalledWith(9));
  });
});
