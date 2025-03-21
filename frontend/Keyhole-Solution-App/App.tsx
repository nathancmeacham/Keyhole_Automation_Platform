// keyhole-solution-app/App.tsx

import React from 'react';
import { SafeAreaView } from 'react-native';
import Chatbot from './components/Chatbot'; // Ensure the case matches exactly

const App = () => {
  return (
    <SafeAreaView style={{ flex: 1 }}>
      <Chatbot />
    </SafeAreaView>
  );
};

export default App;
