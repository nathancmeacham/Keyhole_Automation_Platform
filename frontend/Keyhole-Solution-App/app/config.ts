// Keyhole_Automation_Platform\frontend\Keyhole-Solution-App\app\config.ts

import { Platform } from 'react-native';

const getBackendUrl = (): string => {
  // ✅ Android emulators need 10.0.2.2 instead of localhost
  if (Platform.OS === 'android') {
    return process.env.EXPO_PUBLIC_API_BASE_URL_ANDROID || 'http://10.0.2.2:8000';
  }

  // ✅ Web/iOS fallback
  return process.env.EXPO_PUBLIC_API_BASE_URL || 'http://localhost:8000';
};

export const CONFIG = {
  BACKEND_URL: getBackendUrl(),

  ENV: process.env.EXPO_PUBLIC_ENV || 'development',
  USE_GEMINI: process.env.EXPO_PUBLIC_USE_GEMINI === 'true',
  DEBUG: process.env.EXPO_PUBLIC_DEBUG === 'true',
};
