// Keyhole_Automation_Platform\frontend\Keyhole-Solution-App\app\index.tsx

import React, { useRef, useEffect } from 'react';
import {
  Animated,
  Easing,
  Dimensions,
  View,
  StyleSheet,
  Text,
  TouchableOpacity,
} from 'react-native';
import { useRouter } from 'expo-router';
import LogoIcon from '../components/LogoIcon';

export default function HomeScreen() {
  const pulseAnim = useRef(new Animated.Value(1)).current;
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const logoSize = Dimensions.get('window').width * 0.3; // ✅ 30% of screen width
  const router = useRouter();

  useEffect(() => {
    // Pulse loop animation
    Animated.loop(
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
    ).start();

    // Fade-in animation
    Animated.timing(fadeAnim, {
      toValue: 1,
      duration: 2000,
      delay: 1000,
      useNativeDriver: true,
    }).start();
  }, []);

  const handleGetStarted = () => {
    router.push('/agent'); // Update this to your actual route
  };

  return (
    <View style={styles.container}>
      <View style={{ paddingVertical: 40 }}>
        <Animated.View style={{ transform: [{ scale: pulseAnim }] }}>
          <LogoIcon size={logoSize} />
        </Animated.View>
      </View>

      <Animated.View style={{ opacity: fadeAnim, alignItems: 'center' }}>
        <Text style={styles.subtitle}>
          Welcome to the Keyhole Automation Platform
        </Text>

        <TouchableOpacity onPress={handleGetStarted} style={styles.button}>
          <Text style={styles.buttonText}>Get Started</Text>
        </TouchableOpacity>
      </Animated.View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1F2D45',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24,
  },
  subtitle: {
    marginTop: 24,
    fontSize: 16,
    color: '#ffffffbb',
    textAlign: 'center',
  },
  button: {
    marginTop: 20,
    paddingVertical: 12,
    paddingHorizontal: 28,
    backgroundColor: '#374b6e',
    borderRadius: 8,
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
});
