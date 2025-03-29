// Keyhole_Automation_Platform\frontend\Keyhole-Solution-App\__tests__\screens\ProfileScreen.test.tsx

import React from 'react';
import { render, waitFor } from '@testing-library/react-native';
import ProfileScreen from '../../app/screens/ProfileScreen';
import AsyncStorage from '@react-native-async-storage/async-storage';

global.fetch = jest.fn(() =>
  Promise.resolve({
    ok: true,
    json: () =>
      Promise.resolve({
        email: 'test@example.com',
        role: 'user',
        email_verified: true,
        last_login: '2025-03-27T01:23:45Z',
        ip_history: ['192.168.1.1', '10.0.0.2'],
      }),
  })
) as jest.Mock;

jest.mock('@react-native-async-storage/async-storage', () => ({
  getItem: jest.fn(() => Promise.resolve('mock-token')),
}));

describe('ProfileScreen', () => {
  it('renders user profile info', async () => {
    const { getByText } = render(<ProfileScreen />);

    await waitFor(() => {
      expect(getByText('User Profile')).toBeTruthy();
      expect(getByText('test@example.com')).toBeTruthy();
      expect(getByText('user')).toBeTruthy();
      expect(getByText('Yes')).toBeTruthy();
      expect(getByText('2025-03-27T01:23:45Z')).toBeTruthy();
      expect(getByText('• 192.168.1.1')).toBeTruthy(); // Fixed line
      expect(getByText('• 10.0.0.2')).toBeTruthy(); // Fixed line
    });
  });
});
