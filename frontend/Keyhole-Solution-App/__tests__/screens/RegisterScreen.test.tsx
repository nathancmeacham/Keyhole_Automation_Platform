// Keyhole_Automation_Platform\frontend\Keyhole-Solution-App\__tests__\screens\RegisterScreen.test.tsx

import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react-native';
import RegisterScreen from '../../app/screens/RegisterScreen';
import { Alert } from 'react-native';
import { v4 as uuidv4 } from 'uuid';

jest.mock('expo-router', () => ({
  useRouter: () => ({
    replace: jest.fn(),
  }),
}));

global.fetch = jest.fn();

describe('RegisterScreen - Integration', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('registers a new user and navigates to login screen', async () => {
    const email = `test_${uuidv4().slice(0, 8)}@example.com`;
    const password = 'password123';
    const alertSpy = jest.spyOn(Alert, 'alert');

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ message: 'Check your email' }),
    });

    const { getByPlaceholderText, getByTestId } = render(<RegisterScreen />);

    fireEvent.changeText(getByPlaceholderText('Email'), email);
    fireEvent.changeText(getByPlaceholderText('Password'), password);
    fireEvent.press(getByTestId('register-button'));

    await waitFor(() => {
      expect(alertSpy).toHaveBeenCalledWith(
        'Registration Successful',
        expect.stringContaining('verify your account'),
        expect.any(Array)
      );
    });
  });

  it('shows alert on duplicate email registration attempt', async () => {
    const email = 'duplicate@example.com';
    const password = 'password123';
    const alertSpy = jest.spyOn(Alert, 'alert');

    fetch.mockResolvedValueOnce({
      ok: false,
      json: async () => ({ detail: 'Email already registered' }),
    });

    const { getByPlaceholderText, getByTestId } = render(<RegisterScreen />);

    fireEvent.changeText(getByPlaceholderText('Email'), email);
    fireEvent.changeText(getByPlaceholderText('Password'), password);
    fireEvent.press(getByTestId('register-button'));

    await waitFor(() => {
      expect(alertSpy).toHaveBeenCalledWith(
        'Registration Failed',
        expect.stringMatching(/already registered/i)
      );
    });
  });
});
