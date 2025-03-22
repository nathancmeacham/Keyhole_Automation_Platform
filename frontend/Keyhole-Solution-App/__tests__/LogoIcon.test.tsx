// Keyhole_Automation_Platform\frontend\Keyhole-Solution-App\__tests__\LogoIcon.test.tsx

import React from 'react';
import { render } from '@testing-library/react-native';
import LogoIcon from '../components/LogoIcon';

describe('LogoIcon', () => {
  it('renders with correct size', () => {
    const { getByTestId } = render(<LogoIcon size={64} />);
    expect(getByTestId('logo-svg')).toBeTruthy();
  });
});
