// Keyhole_Automation_Platform\frontend\Keyhole-Solution-App\app\screens\VerifySuccessScreen.tsx

import React from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';
import { useRouter } from 'expo-router';

const VerifySuccessScreen = () => {
  const router = useRouter();

  const handleGoToLogin = () => {
    router.replace('/screens/LoginScreen'); // ✅ Clean screen reset
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>✅ Email Verified!</Text>
      <Text style={styles.message}>
        Your email has been successfully verified. You can now log in and start using the app.
      </Text>
      <Button title="Go to Login" onPress={handleGoToLogin} />
    </View>
  );
};

export default VerifySuccessScreen;

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center', padding: 20 },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 10, color: '#2e7d32' },
  message: { fontSize: 16, marginBottom: 20, textAlign: 'center' },
});
