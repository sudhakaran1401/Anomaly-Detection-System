import { describe, expect, it, vi, beforeEach } from 'vitest';
import api from '../api/axios';
import { downloadFile } from '../utils/downloadFile';
import AnomalyService from '../services/AnomalyService';
import ClassificationService from '../services/ClassificationService';

vi.mock('../api/axios', () => ({
  default: {
    post: vi.fn(),
    get: vi.fn(),
    delete: vi.fn(),
  },
}));

vi.mock('../utils/downloadFile', () => ({
  downloadFile: vi.fn(),
}));

describe('AnomalyService', () => {
  beforeEach(() => vi.clearAllMocks());

  it('posts a dataset for anomaly analysis', async () => {
    const form = new FormData();
    api.post.mockResolvedValue({ data: { success: true } });
    await AnomalyService.analyzeDataset(form);
    expect(api.post).toHaveBeenCalledWith('anomaly/analyze/', form, { headers: { 'Content-Type': 'multipart/form-data' } });
  });

  it('loads, deletes and clears history', async () => {
    api.get.mockResolvedValue({ data: [] });
    api.delete.mockResolvedValue({ data: { success: true } });
    await AnomalyService.getHistory();
    await AnomalyService.deleteHistory(7);
    await AnomalyService.clearHistory();
    expect(api.get).toHaveBeenCalledWith('anomaly/history/');
    expect(api.delete).toHaveBeenNthCalledWith(1, 'anomaly/history/7/');
    expect(api.delete).toHaveBeenNthCalledWith(2, 'anomaly/history/clear/');
  });

  it('downloads anomaly PDF and CSV', async () => {
    api.get.mockResolvedValue({ data: 'blob', headers: {} });
    await AnomalyService.downloadPDF({ filename: 'data.csv', model_name: 'isolation_forest', scaler_type: 'standard', contamination: 0.01 });
    await AnomalyService.downloadCSV();
    expect(api.get).toHaveBeenNthCalledWith(1, 'anomaly/download/pdf/', expect.objectContaining({ responseType: 'blob' }));
    await AnomalyService.downloadCSV();

    expect(api.get).toHaveBeenNthCalledWith(2, "anomaly/download/csv/",
        {
            params: { filter: "all", },
            responseType: "blob",
        }
    );
    expect(downloadFile).toHaveBeenNthCalledWith(1, expect.anything(), 'anomaly_report.pdf', 'application/pdf');
    expect(downloadFile).toHaveBeenNthCalledWith(2, expect.anything(), 'anomaly_results.csv', 'text/csv');
  });
});

describe('ClassificationService', () => {
  beforeEach(() => vi.clearAllMocks());

  it('classifies a dataset with multipart headers', async () => {
    const form = new FormData();
    api.post.mockResolvedValue({ data: { success: true } });
    await ClassificationService.classifyDataset(form);
    expect(api.post).toHaveBeenCalledWith('classification/classify/', form, { headers: { 'Content-Type': 'multipart/form-data' } });
  });

  it('gets, gets by id and deletes classification results', async () => {
    api.get.mockResolvedValue({ data: [] });
    api.delete.mockResolvedValue({ data: {} });
    await ClassificationService.getResults();
    await ClassificationService.getResult(4);
    await ClassificationService.deleteResult(4);
    expect(api.get).toHaveBeenNthCalledWith(1, 'classification/results/');
    expect(api.get).toHaveBeenNthCalledWith(2, 'classification/results/4/');
    expect(api.delete).toHaveBeenCalledWith('classification/results/4/');
  });

  it('downloads a classification PDF', async () => {
    api.get.mockResolvedValue({ data: 'blob', headers: {} });
    await ClassificationService.downloadPDF(12);
    expect(api.get).toHaveBeenCalledWith('classification/results/12/download/pdf/', { responseType: 'blob' });
    expect(downloadFile).toHaveBeenCalledWith(expect.anything(), 'classification_report.pdf', 'application/pdf');
  });
});
