import React from 'react';
import { render, waitFor, screen } from '@testing-library/react';
import axios from 'axios';
import App from './App'; // Adjust the path according to your project structure
import { jest } from '@jest/globals';

jest.unstable_mockModule('axios', () => ({
  get: jest.fn().mockResolvedValue({ data: [] }), // Adjust the resolved value as needed
}));

describe('App Component', () => {
  const mockUsers = [
    {
      id: 1,
      name: 'Leanne Graham',
      email: 'Sincere@april.biz',
      address: {
        city: 'Gwenborough'
      }
    },
    // Add more users as per your mock data requirement
  ];

  beforeEach(() => {
    // Reset mocks before each test
    axios.get.mockClear();
  });

  it('fetches and displays user data', async () => {
    // Mock the Axios get request
    axios.get.mockResolvedValueOnce({
      data: mockUsers
    });

    // Render the component
    render(<App />);

    // Wait for the promise to resolve
    await waitFor(() => expect(axios.get).toHaveBeenCalledTimes(1));

    // Check if the data is displayed
    mockUsers.forEach(user => {
      expect(screen.getByText(user.name)).toBeInTheDocument();
      expect(screen.getByText(user.email)).toBeInTheDocument();
      expect(screen.getByText(user.address.city)).toBeInTheDocument();
    });
  });
});
