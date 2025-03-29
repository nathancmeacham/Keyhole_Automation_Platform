// Keyhole_Automation_Platform\frontend\Keyhole-Solution-App\app\screens\ProfileScreen.tsx

import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView, ActivityIndicator, Alert } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { CONFIG } from '../config'; // ✅ Your dynamic backend config

const ProfileScreen = () => {
  const [profile, setProfile] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const token = await AsyncStorage.getItem('access_token');
        if (!token) throw new Error('No token');

        const response = await fetch(`${CONFIG.BACKEND_URL}/auth/me`, {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (!response.ok) throw new Error('Profile fetch failed');

        const data = await response.json();
        setProfile(data);
      } catch (error: any) {
        console.log('[ProfileScreen] Unable to load profile:', error.message);
        // We do NOT alert the user on failure here — just allow blank fallback view
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, []);

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color="#1F2D45" />
        <Text>Loading profile...</Text>
      </View>
    );
  }

  if (!profile) {
    return (
      <View style={styles.center}>
        <Text>Unable to load profile.</Text>
      </View>
    );
  }

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.heading}>User Profile</Text>
      <Text style={styles.label}>Email:</Text>
      <Text style={styles.value}>{profile.email}</Text>

      <Text style={styles.label}>Role:</Text>
      <Text style={styles.value}>{profile.role}</Text>

      <Text style={styles.label}>Verified:</Text>
      <Text style={styles.value}>{profile.email_verified ? 'Yes' : 'No'}</Text>

      <Text style={styles.label}>Last Login:</Text>
      <Text style={styles.value}>{profile.last_login || 'N/A'}</Text>

      <Text style={styles.label}>IP History:</Text>
      {profile.ip_history?.length ? (
        profile.ip_history.map((ip: string, index: number) => (
          <Text key={index} style={styles.value}>• {ip}</Text>
        ))
      ) : (
        <Text style={styles.value}>No IP data found.</Text>
      )}
    </ScrollView>
  );
};

export default ProfileScreen;

const styles = StyleSheet.create({
  container: { padding: 20, flexGrow: 1 },
  heading: { fontSize: 26, fontWeight: 'bold', marginBottom: 20, textAlign: 'center' },
  label: { fontSize: 16, fontWeight: 'bold', marginTop: 10 },
  value: { fontSize: 16, marginBottom: 6 },
  center: { flex: 1, justifyContent: 'center', alignItems: 'center' },
});
