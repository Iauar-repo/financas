// This is a shim for web and Android where the tab bar is generally opaque.
import { View } from 'react-native';

export default function TabBarBackground() {
  return <View style={{ height: 0 }} />;
}

export function useBottomTabOverflow() {
  return 0;
}