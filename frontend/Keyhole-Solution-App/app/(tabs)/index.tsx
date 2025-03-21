// Keyhole-Solution-App\app\(tabs)\index.tsx

import React, { useRef, useEffect } from 'react';
import { View, TextInput, Button, Animated, Easing, StyleSheet, Dimensions } from 'react-native';
import LogoIcon from '../../components/LogoIcon'; // Make sure this path is correct

const ChatScreen = () => {
  const pulseAnim = useRef(new Animated.Value(1)).current;

  const screenWidth = Dimensions.get('window').width;
  const logoSize = screenWidth * 0.25;

  useEffect(() => {
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
  }, []);

  return (
    <View style={styles.container}>
      <Animated.View style={{ transform: [{ scale: pulseAnim }] }}>
        <LogoIcon size={logoSize} />
      </Animated.View>

      <View style={styles.inputContainer}>
        <TextInput placeholder="Type your message..." style={styles.input} />
        <Button title="Send" onPress={() => console.log('Send button pressed')} />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1F2D45',
    justifyContent: 'center',
    alignItems: 'center',
    paddingBottom: 50,
  },
  inputContainer: {
    position: 'absolute',
    bottom: 10,
    flexDirection: 'row',
    backgroundColor: 'white',
    borderRadius: 10,
    paddingHorizontal: 10,
    paddingVertical: 5,
    width: '90%',
    alignItems: 'center',
    elevation: 5,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 4,
  },
  input: {
    flex: 1,
    padding: 10,
  },
});

export default ChatScreen;
