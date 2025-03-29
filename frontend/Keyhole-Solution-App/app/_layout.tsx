// Keyhole_Automation_Platform\frontend\Keyhole-Solution-App\app\_layout.tsx

import { Slot } from 'expo-router';
import { SafeAreaView, StyleSheet, StatusBar } from 'react-native';

export default function Layout() {
  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#1F2D45" />
      <Slot />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1F2D45',
  },
});
