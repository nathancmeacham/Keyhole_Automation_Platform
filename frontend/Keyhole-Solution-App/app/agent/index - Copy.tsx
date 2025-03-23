//Keyhole_Automation_Platform\frontend\Keyhole-Solution-App\app\agent\index.tsx
import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  Button,
  StyleSheet,
  Keyboard,
  Platform
} from 'react-native';
import sendMessageToAgent from '@/utils/agentAPI';

export default function AgentScreen() {
  const [userMessage, setUserMessage] = useState('');
  const [agentResponse, setAgentResponse] = useState('');

  const handleSend = async () => {
    if (!userMessage.trim()) return;
    const response = await sendMessageToAgent(userMessage);
    setAgentResponse(response);
    setUserMessage('');
    Keyboard.dismiss();  // dismiss keyboard after sending
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>🤖 Digital Agent</Text>
      <Text style={styles.message}>
        Ask me anything about your organization, work orders, or services.
      </Text>

      <TextInput
        style={styles.input}
        value={userMessage}
        onChangeText={setUserMessage}
        placeholder="Type your message..."
        placeholderTextColor="#888"
        multiline
        blurOnSubmit={false}
        onSubmitEditing={() => {
          if (!Platform.OS.startsWith('web')) {
            handleSend();  // Send on Enter for iOS/Android
          }
        }}
        onKeyPress={({ nativeEvent }) => {
          if (Platform.OS === 'web') {
            if (nativeEvent.key === 'Enter' && !nativeEvent.shiftKey) {
              nativeEvent.preventDefault();
              handleSend();
            }
          }
        }}
      />

      <Button title="Send" onPress={handleSend} />

      <Text style={styles.response}>
        {agentResponse ? `Agent: ${agentResponse}` : ''}
      </Text>
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
    marginBottom: 24,
  },
  input: {
    width: '100%',
    minHeight: 50,
    maxHeight: 140,
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 6,
    padding: 12,
    marginBottom: 12,
    color: '#fff',
    backgroundColor: '#2E3B55',
    textAlignVertical: 'top',
  },
  response: {
    marginTop: 16,
    fontSize: 16,
    fontStyle: 'italic',
    color: '#fff',
    textAlign: 'center',
  },
});
