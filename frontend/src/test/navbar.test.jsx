import { describe, expect, it, vi } from 'vitest';
import { fireEvent, render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import Navbar from '../components/Navbar';
import ThemeProvider from '../components/ThemeContext';

const navigate = vi.fn();
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return { ...actual, useNavigate: () => navigate };
});

describe('Navbar', () => {
  it('shows public navigation when logged out', () => {
    render(<MemoryRouter><ThemeProvider><Navbar /></ThemeProvider></MemoryRouter>);
    expect(screen.getByText('Anomaly Detection Platform')).toBeInTheDocument();
    expect(screen.queryByText('History')).not.toBeInTheDocument();
    expect(screen.getByText('🌙 Dark Mode')).toBeInTheDocument();
  });

  it('shows authenticated navigation and logs out', () => {
    localStorage.setItem('access', 'token');
    localStorage.setItem('refresh', 'refresh-token');
    localStorage.setItem('username', 'alice');

    render(<MemoryRouter initialEntries={['/dashboard']}><ThemeProvider><Navbar /></ThemeProvider></MemoryRouter>);
    expect(screen.getByText('alice')).toBeInTheDocument();
    expect(screen.getByText('History')).toBeInTheDocument();
    expect(screen.getByText('Dashboard')).toBeInTheDocument();

    const logout = screen.getByText('Logout');
    fireEvent.click(logout);
    expect(localStorage.getItem('access')).toBeNull();
    expect(localStorage.getItem('refresh')).toBeNull();
    expect(localStorage.getItem('username')).toBeNull();
    expect(navigate).toHaveBeenCalledWith('/');
  });
});
