// Keyhole_Automation_Platform\frontend\Keyhole-Solution-App\__tests__\screens\VerifySuccessScreen.test.tsx

import React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import VerifySuccessScreen from '../../app/screens/VerifySuccessScreen';
import { useRouter } from 'expo-router';

// Mock the router
const mockReplace = jest.fn();
jest.mock('expo-router', () => ({
  useRouter: () => ({ replace: mockReplace }),
}));

describe('VerifySuccessScreen', () => {
  it('renders success message', () => {
    const { getByText } = render(<VerifySuccessScreen />);
    expect(getByText('✅ Email Verified!')).toBeTruthy();
    expect(
      getByText(
        'Your email has been successfully verified. You can now log in and start using the app.'
      )
    ).toBeTruthy();
    expect(getByText('Go to Login')).toBeTruthy();
  });

  it('navigates to LoginScreen on button press', () => {
    const { getByText } = render(<VerifySuccessScreen />);
    fireEvent.press(getByText('Go to Login'));
    expect(mockReplace).toHaveBeenCalledWith('/screens/LoginScreen');
  });
});
