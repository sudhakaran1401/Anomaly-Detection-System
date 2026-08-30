import { act, renderHook } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import useMessage from '../hooks/useMessage';

describe('useMessage', () => {
  it('shows success and error messages and clears them', () => {
    vi.useFakeTimers();
    const { result } = renderHook(() => useMessage());

    act(() => result.current.showSuccess('Saved'));
    expect(result.current.message).toEqual({ type: 'success', text: 'Saved' });

    act(() => result.current.showError('Failed'));
    expect(result.current.message).toEqual({ type: 'danger', text: 'Failed' });

    act(() => result.current.clearMessage());
    expect(result.current.message).toEqual({ type: '', text: '' });
    vi.useRealTimers();
  });

  it('auto clears a message after two seconds', () => {
    vi.useFakeTimers();
    const { result } = renderHook(() => useMessage());
    act(() => result.current.showSuccess('Done'));
    expect(result.current.message.text).toBe('Done');
    act(() => vi.advanceTimersByTime(2000));
    expect(result.current.message).toEqual({ type: '', text: '' });
    vi.useRealTimers();
  });
});
