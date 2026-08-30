import '@testing-library/jest-dom/vitest';
import { afterEach } from "vitest";

Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: (query) => ({ matches: false, media: query, onchange: null, addListener: () => {}, removeListener: () => {}, addEventListener: () => {}, removeEventListener: () => {}, dispatchEvent: () => false }),
});

Object.defineProperty(URL, 'createObjectURL', { writable: true, value: () => 'blob:mock-url' });
Object.defineProperty(URL, 'revokeObjectURL', { writable: true, value: () => {} });


afterEach(() => {
  localStorage.clear();
  sessionStorage.clear();
  document.body.className = '';
});
