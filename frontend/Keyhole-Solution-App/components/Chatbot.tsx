// keyhole-solution-app/components/Chatbot.tsx

import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, TouchableOpacity, FlatList, StyleSheet } from 'react-native';

const Chatbot = () => {
  const [messages, setMessages] = useState([{ text: 'Hello! How can I assist you today?', sender: 'bot' }]);
  const [inputText, setInputText] = useState('');

  useEffect(() => {
    fetchGreeting();
  }, []);

  const fetchGreeting = async () => {
    try {
      const response = await fetch('https://your-mcp-server.com/chat/greet');
      const data = await response.json();
      setMessages([{ text: data.message, sender: 'bot' }]);
    } catch (error) {
      console.error('Error fetching greeting:', error);
    }
  };

  const sendMessage = () => {
    if (!inputText.trim()) return;
    const newMessage = { text: inputText, sender: 'user' };
    setMessages([...messages, newMessage]);
    setInputText('');
  };

  return (
    <View style={styles.container}>
      <FlatList
        data={messages}
        renderItem={({ item }) => (
          <View style={[styles.message, item.sender === 'user' ? styles.userMessage : styles.botMessage]}>
            <Text>{item.text}</Text>
          </View>
        )}
        keyExtractor={(item, index) => index.toString()}
      />
      <View style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          value={inputText}
          onChangeText={setInputText}
          placeholder="Type your message..."
        />
        <TouchableOpacity style={styles.sendButton} onPress={sendMessage}>
          <Text>Send</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, padding: 10, backgroundColor: '#fff' },
  message: { padding: 10, marginVertical: 5, borderRadius: 10 },
  userMessage: { alignSelf: 'flex-end', backgroundColor: '#dcf8c6' },
  botMessage: { alignSelf: 'flex-start', backgroundColor: '#f1f1f1' },
  inputContainer: { flexDirection: 'row', alignItems: 'center', padding: 5 },
  input: { flex: 1, borderWidth: 1, borderRadius: 5, padding: 8 },
  sendButton: { padding: 10, backgroundColor: '#007bff', borderRadius: 5, marginLeft: 5 },
});

export default Chatbot;