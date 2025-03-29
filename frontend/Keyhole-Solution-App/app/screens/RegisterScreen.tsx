// Keyhole_Automation_Platform\frontend\Keyhole-Solution-App\app\screens\RegisterScreen.tsx

import React, { useState } from 'react';
import { View, Text, TextInput, Button, Alert, StyleSheet } from 'react-native';
import { useRouter } from 'expo-router';
import { CONFIG } from '../config';

const RegisterScreen = () => {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleRegister = async () => {
    try {
      const response = await fetch(`${CONFIG.BACKEND_URL}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (response.ok) {
        Alert.alert(
          'Registration Successful',
          'Please check your email to verify your account.',
          [{ text: 'OK', onPress: () => router.replace('/screens/LoginScreen') }]
        );
      } else {
        Alert.alert('Registration Failed', data.detail || 'Something went wrong.');
      }
    } catch (error: any) {
      console.log('[RegisterScreen] Fetch error:', error);
      Alert.alert('Registration Failed', 'Unable to register at this time.');
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.header}>Register</Text>
      <TextInput
        placeholder="Email"
        value={email}
        onChangeText={setEmail}
        autoCapitalize="none"
        keyboardType="email-address"
        style={styles.input}
      />
      <TextInput
        placeholder="Password"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
        style={styles.input}
      />
      <Button
        title="Register"
        onPress={handleRegister}
        testID="register-button"
        accessibilityLabel="SubmitRegistrationButton"
      />
    </View>
  );
};

export default RegisterScreen;

const styles = StyleSheet.create({
  container: { padding: 20, marginTop: 80 },
  header: { fontSize: 24, marginBottom: 20, fontWeight: 'bold' },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    padding: 10,
    marginBottom: 12,
    borderRadius: 6,
  },
});
