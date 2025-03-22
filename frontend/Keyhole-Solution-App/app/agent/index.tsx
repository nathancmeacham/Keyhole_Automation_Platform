// Keyhole_Automation_Platform\frontend\Keyhole-Solution-App\app\agent\index.tsx

import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

export default function AgentScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>🤖 Digital Agent</Text>
      <Text style={styles.message}>
        Ask me anything about your organization, work orders, or services.
      </Text>
      {/* Later: Drop in your chat UI / Agent component here */}
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
  title: {
    fontSize: 28,
    color: '#fff',
    fontWeight: 'bold',
    marginBottom: 16,
  },
  message: {
    fontSize: 16,
    color: '#ffffffbb',
    textAlign: 'center',
    paddingHorizontal: 16,
  },
});
