import { describe, expect, it, vi, beforeEach } from 'vitest';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import Login from '../pages/Main/Login';
import ThemeProvider from '../components/ThemeContext';
import api from '../api/axios';

vi.mock('../api/axios', () => ({ default: { post: vi.fn() } }));
const navigate = vi.fn();
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return { ...actual, useNavigate: () => navigate };
});

describe('Login page', () => {
  beforeEach(() => { vi.clearAllMocks(); });

  const renderLogin = () => render(<MemoryRouter><ThemeProvider><Login /></ThemeProvider></MemoryRouter>);

  it('submits credentials and stores tokens', async () => {
    api.post.mockResolvedValue({ data: { access: 'access-token', refresh: 'refresh-token' } });
    renderLogin();
    fireEvent.change(screen.getByPlaceholderText('Enter username'), { target: { value: 'alice' } });
    fireEvent.change(screen.getByPlaceholderText('Enter password'), { target: { value: 'secret' } });
    fireEvent.click(screen.getByRole('button', { name: 'Login' }));

    await waitFor(() => expect(api.post).toHaveBeenCalledWith('token/', { username: 'alice', password: 'secret' }));
    expect(localStorage.getItem('access')).toBe('access-token');
    expect(localStorage.getItem('refresh')).toBe('refresh-token');
    expect(localStorage.getItem('username')).toBe('alice');
    expect(screen.getByRole('alert')).toHaveTextContent('Login successful.');

    await waitFor(() => {
      expect(navigate).toHaveBeenCalledWith('/upload');
    });
  });

  it('shows an error for invalid credentials', async () => {
    api.post.mockRejectedValue(new Error('401'));
    renderLogin();
    fireEvent.change(screen.getByPlaceholderText('Enter username'), { target: { value: 'bad' } });
    fireEvent.change(screen.getByPlaceholderText('Enter password'), { target: { value: 'bad' } });
    fireEvent.click(screen.getByRole('button', { name: 'Login' }));
    await waitFor(() => expect(screen.getByRole('alert')).toHaveTextContent('Invalid username or password.'));
    expect(localStorage.getItem('access')).toBeNull();
  });
});
