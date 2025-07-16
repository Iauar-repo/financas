// app/(tabs)/index.tsx
import React from 'react';
import { View, Text, TouchableOpacity, Image, StyleSheet } from 'react-native';
import { useRouter } from 'expo-router';
import profilePlaceholder from '@/assets/images/profile-placeholder.png'; // Update the path as needed

export default function DashboardScreen() {
  const router = useRouter();
  const userPhotoUrl = null; // Replace with your real user photo URL

  return (
    <View style={styles.container}>
      {/* Absolute header-style profile button */}
      <TouchableOpacity
        style={styles.profileButton}
        activeOpacity={0.8}
        onPress={() => router.push('/profile')}
      >
        <Image
          source={userPhotoUrl ? { uri: userPhotoUrl } : profilePlaceholder}
          style={styles.avatarImage}
        />
      </TouchableOpacity>

      {/* Main dashboard content */}
      <View style={styles.centeredContent}>
        <Text style={styles.dashboardText}>Dashboard</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f8f9fc' },
  profileButton: {
    position: 'absolute',
    top: 38, // Adjust for safe area/status bar (use react-native-safe-area-context for production)
    left: 20,
    width: 50,
    height: 50,
    borderRadius: 25,
    backgroundColor: '#F5F6FA',
    alignItems: 'center',
    justifyContent: 'center',
    elevation: 2,
    shadowColor: '#000',
    shadowOpacity: 0.07,
    shadowOffset: { width: 0, height: 2 },
    shadowRadius: 8,
    zIndex: 10,
  },
  avatarImage: {
    width: 44,
    height: 44,
    borderRadius: 22,
  },
  centeredContent: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  dashboardText: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#464575',
  },
});