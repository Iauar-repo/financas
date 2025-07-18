import React, { useEffect, useState } from 'react';
import { View, Text, ActivityIndicator, Image, StyleSheet, ScrollView, Button, Alert, Modal, TextInput } from 'react-native';
import profilePlaceholder from '@/assets/images/profile-placeholder.png';
import { getCurrentUserInfo, getUserProfile, updateUserProfile, UserProfile } from '@/services/userService';
import { useAuth } from '@/hooks/useAuth';


export default function ProfileScreen() {
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [userId, setUserId] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const { signOut } = useAuth();
  
  // Modal state
  const [showEdit, setShowEdit] = useState(false);
  const [editName, setEditName] = useState('');
  const [editEmail, setEditEmail] = useState('');
  const [saving, setSaving] = useState(false);

  // Fetch current user id, then full user profile
  useEffect(() => {
    (async () => {
      setLoading(true);
      try {
        // Step 1: Get id from /api/auth/me
        const me = await getCurrentUserInfo(); // { id }
        console.log('me:', me);
        if (!me || typeof me.id !== 'number') throw new Error('No user id found.');
        setUserId(me.id);

        // Step 2: Get full user info from /api/users/<id>
        const userProfile = await getUserProfile(me.id);
        setProfile(userProfile);
      } catch (e) {
        Alert.alert('Error', 'Failed to load profile data.');
        setProfile(null);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const openEdit = () => {
    setEditName(profile?.name || '');
    setEditEmail(profile?.email || '');
    setShowEdit(true);
  };

  const handleSave = async () => {
    if (!userId) return;
    setSaving(true);
    try {
      await updateUserProfile(userId, { name: editName, email: editEmail });
      setShowEdit(false);
      // Reload profile after saving
      const updatedProfile = await getUserProfile(userId);
      setProfile(updatedProfile);
      Alert.alert('Success', 'Profile updated!');
    } catch {
      Alert.alert('Error', 'Failed to update profile.');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator size="large" />
      </View>
    );
  }

  if (!profile) {
    return (
      <View style={styles.centered}>
        <Text>User not found or not logged in.</Text>
      </View>
    );
  }

  const userPhotoUrl = profile.avatar || null;

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <View style={styles.avatarWrapper}>
        <Image
          source={userPhotoUrl ? { uri: userPhotoUrl } : profilePlaceholder}
          style={styles.avatar}
        />
      </View>
      <Text style={styles.label}>Username:</Text>
      <Text style={styles.value}>{profile.username || profile.nickname || 'N/A'}</Text>
      <Text style={styles.label}>Name:</Text>
      <Text style={styles.value}>{profile.name || 'N/A'}</Text>
      <Text style={styles.label}>Email:</Text>
      <Text style={styles.value}>{profile.email || 'N/A'}</Text>
      <Text style={styles.label}>Created At:</Text>
      <Text style={styles.value}>{profile.created_at ? new Date(profile.created_at).toLocaleString() : 'N/A'}</Text>
      <Button title="Edit Profile" onPress={openEdit} disabled={loading || saving} />
      <Button title="Logout" onPress={signOut} disabled={loading || saving} />

      {/* EDIT MODAL */}
      <Modal visible={showEdit} animationType="slide" transparent>
        <View style={styles.modalBackground}>
          <View style={styles.modalContent}>
            <Text style={styles.modalTitle}>Edit Profile</Text>
            <TextInput
              value={editName}
              onChangeText={setEditName}
              placeholder="Name"
              style={styles.input}
              autoCapitalize="words"
            />
            <TextInput
              value={editEmail}
              onChangeText={setEditEmail}
              placeholder="Email"
              style={styles.input}
              keyboardType="email-address"
              autoCapitalize="none"
            />
            <View style={{ flexDirection: 'row', justifyContent: 'space-between', marginTop: 18 }}>
              <Button title="Cancel" onPress={() => setShowEdit(false)} disabled={saving} />
              <Button title={saving ? "Saving..." : "Save"} onPress={handleSave} disabled={saving} />
            </View>
          </View>
        </View>
      </Modal>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { padding: 24, alignItems: 'center' },
  centered: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  avatarWrapper: {
    marginTop: 18,
    marginBottom: 18,
    width: 100,
    height: 100,
    borderRadius: 50,
    backgroundColor: '#F5F6FA',
    alignItems: 'center',
    justifyContent: 'center',
    elevation: 2,
    shadowColor: '#000',
    shadowOpacity: 0.07,
    shadowOffset: { width: 0, height: 2 },
    shadowRadius: 8,
  },
  avatar: { width: 92, height: 92, borderRadius: 46 },
  label: { fontWeight: 'bold', marginTop: 8 },
  value: { fontSize: 16, marginBottom: 8 },
  modalBackground: {
    flex: 1, backgroundColor: 'rgba(0,0,0,0.18)', justifyContent: 'center', alignItems: 'center',
  },
  modalContent: {
    width: 320, backgroundColor: 'white', borderRadius: 8, padding: 24,
  },
  modalTitle: { fontWeight: 'bold', fontSize: 18, marginBottom: 12 },
  input: { borderBottomWidth: 1, marginVertical: 12, padding: 4, fontSize: 16 },
});
