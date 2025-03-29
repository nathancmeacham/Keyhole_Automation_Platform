// Keyhole_Automation_Platform\frontend\Keyhole-Solution-App\app\screens\VerifyEmailScreen.tsx

import React, { useEffect, useState } from 'react';
import { View, Text, ActivityIndicator, Button, StyleSheet, Alert } from 'react-native';
import { useSearchParams, useRouter } from 'expo-router';

const VerifyEmailScreen = () => {
  const { token } = useSearchParams();
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [status, setStatus] = useState<'success' | 'error' | 'invalid' | null>(null);

  useEffect(() => {
    const verify = async () => {
      if (!token) {
        setStatus('invalid');
        setLoading(false);
        return;
      }

      try {
        const response = await fetch('http://10.0.2.2:8000/auth/verify-email', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ token }),
        });

        const data = await response.json();
        setStatus(response.ok ? 'success' : 'error');
      } catch (err) {
        setStatus('error');
      } finally {
        setLoading(false);
      }
    };

    verify();
  }, [token]);

  return (
    <View style={styles.container}>
      {loading ? (
        <>
          <ActivityIndicator size="large" />
          <Text style={styles.message}>Verifying your email...</Text>
        </>
      ) : status === 'success' ? (
        <>
          <Text style={styles.success}>✅ Email verified successfully!</Text>
          <Button title="Go to Login" onPress={() => router.replace('/screens/LoginScreen')} />
        </>
      ) : status === 'invalid' ? (
        <>
          <Text style={styles.error}>⚠️ Invalid or missing token.</Text>
          <Button title="Back to Login" onPress={() => router.replace('/screens/LoginScreen')} />
        </>
      ) : (
        <>
          <Text style={styles.error}>❌ Verification failed. Please try again later.</Text>
          <Button title="Back to Login" onPress={() => router.replace('/screens/LoginScreen')} />
        </>
      )}
    </View>
  );
};

export default VerifyEmailScreen;

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center', padding: 20 },
  message: { fontSize: 16, marginTop: 20 },
  success: { fontSize: 20, fontWeight: 'bold', color: 'green', marginBottom: 20 },
  error: { fontSize: 18, color: 'red', marginBottom: 20 },
});
