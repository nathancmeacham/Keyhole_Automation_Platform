// Keyhole_Automation_Platform\frontend\Keyhole-Solution-App\app\index.tsx

import React, { useRef, useEffect, useState } from 'react';
import {
  Animated,
  Easing,
  Dimensions,
  View,
  StyleSheet,
  Text,
  TouchableOpacity,
  StatusBar,
  SafeAreaView,
  Alert,
} from 'react-native';
import { useRouter } from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';
import LogoIcon from '../components/LogoIcon';

export default function HomeScreen() {
  const pulseAnim = useRef(new Animated.Value(1)).current;
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const [logoSize, setLogoSize] = useState(Dimensions.get('window').width * 0.3);
  const router = useRouter();
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const updateLogoSize = () => {
      setLogoSize(Dimensions.get('window').width * 0.3);
    };

    const dimensionsListener = Dimensions.addEventListener('change', updateLogoSize);

    const pulseAnimation = Animated.loop(
      Animated.sequence([
        Animated.timing(pulseAnim, {
          toValue: 1.05,
          duration: 1250,
          easing: Easing.inOut(Easing.ease),
          useNativeDriver: true,
        }),
        Animated.timing(pulseAnim, {
          toValue: 1,
          duration: 1250,
          easing: Easing.inOut(Easing.ease),
          useNativeDriver: true,
        }),
      ])
    );

    const fadeAnimation = Animated.timing(fadeAnim, {
      toValue: 1,
      duration: 2000,
      delay: 1000,
      useNativeDriver: true,
    });

    pulseAnimation.start();
    fadeAnimation.start();
    checkAuthToken();

    return () => {
      pulseAnimation.stop();
      fadeAnimation.stop();
      dimensionsListener.remove();
    };
  }, []);

  const checkAuthToken = async () => {
    try {
      const token = await AsyncStorage.getItem('authToken');
      setIsLoggedIn(!!token);
      if (!token) {
        router.replace('/screens/LoginScreen');
      }
    } catch (error) {
      console.error('Error checking auth token:', error);
      Alert.alert('Error', 'Failed to check authentication status.');
      router.replace('/screens/LoginScreen');
    }
  };

  const handleGetStarted = () => {
    router.push('/agent');
  };

  if (!isLoggedIn) return null;

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" />
      <View style={styles.content}>
        <View style={styles.logoContainer}>
          <Animated.View style={{ transform: [{ scale: pulseAnim }] }}>
            <LogoIcon size={logoSize} />
          </Animated.View>
        </View>
        <Animated.View style={[styles.contentContainer, { opacity: fadeAnim }]}>
          <Text style={styles.subtitle}>Welcome to the Keyhole Automation Platform</Text>
          <TouchableOpacity onPress={handleGetStarted} style={styles.button}>
            <Text style={styles.buttonText}>Get Started</Text>
          </TouchableOpacity>
        </Animated.View>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1F2D45',
  },
  content: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24,
  },
  logoContainer: {
    paddingVertical: 40,
  },
  contentContainer: {
    alignItems: 'center',
  },
  subtitle: {
    marginTop: 24,
    fontSize: 18,
    color: '#ffffffcc',
    textAlign: 'center',
    fontWeight: '500',
  },
  button: {
    marginTop: 32,
    paddingVertical: 14,
    paddingHorizontal: 32,
    backgroundColor: '#374b6e',
    borderRadius: 8,
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
});
