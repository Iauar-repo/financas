import React, { useState, useRef, useEffect, useMemo } from 'react';
import { useColorScheme } from '@/hooks/useColorScheme';
import {
  Alert,
  View,
  Text,
  StyleSheet,
  TextInput,
  ActivityIndicator,
  Platform,
  TouchableOpacity,
  KeyboardAvoidingView,
  ScrollView,
  TouchableWithoutFeedback,
  Keyboard,
} from 'react-native';
import { useRouter, Stack } from 'expo-router';
import {
  loadRememberedCredentials,
  saveRememberedCredentials,
  clearRememberedCredentials,
} from '@/services/credentialsService';
import { useAuth } from '@/contexts/AuthContext';



export default function LoginScreen() {
  const colorScheme = useColorScheme();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isPasswordFocused, setIsPasswordFocused] = useState(false);
  const [isUsernameFocused, setIsUsernameFocused] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);
  const { signIn } = useAuth();
  const router = useRouter();
  const passwordInputRef = useRef<TextInput>(null);
  const usernameInputRef = useRef<TextInput>(null);

  useEffect(() => {
    const loadCredentials = async () => {
      try {
        const storedCredentials = await loadRememberedCredentials();
        if (storedCredentials) {
          setUsername(storedCredentials.username);
          setPassword(storedCredentials.password || '');
          setRememberMe(true);
        }
      } catch (error) {
        console.error('Falha ao carregar as credenciais salvas.', error);
      }
    };
    loadCredentials();
  }, []);

  const handleLogin = async () => {
    if (!username.trim() || !password.trim()) {
      Alert.alert('Erro', 'Por favor, preencha todos os campos.');
      return;
    }

    setIsLoading(true);

    try {
      // Usar a função signIn do contexto, que lida com o login e a atualização do estado.
      await signIn(username, password);

      if (rememberMe) {
        await saveRememberedCredentials(username, password);
      } else {
        await clearRememberedCredentials();
      }
    } catch (error) {
      console.error('Erro de Login:', error);
      if (error instanceof Error) {
        Alert.alert('Falha no Login', error.message);
      } else {
        Alert.alert('Erro de Conexão', 'Não foi possível conectar ao servidor. Verifique sua conexão com a internet e tente novamente.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const styles = useMemo(
    () =>
      StyleSheet.create({
        keyboardAvoidingContainer: {
          flex: 1,
          backgroundColor: colorScheme === 'dark' ? '#121212' : '#FFF',
        },
        scrollViewContent: {
          flexGrow: 1,
          justifyContent: 'center',
        },
        container: {
          justifyContent: 'center',
          alignItems: 'center',
          padding: 20,
        },
        formWrapper: {
          width: '80%',
          maxWidth: 400,
          alignItems: 'center',
        },
        title: {
          fontSize: 24,
          fontWeight: 'bold',
          marginBottom: 20,
          color: colorScheme === 'dark' ? '#FFF' : '#000',
        },
        inputContainer: {
          width: '100%',
          height: 40,
          borderColor: colorScheme === 'dark' ? '#555' : 'gray',
          borderWidth: 1,
          borderRadius: 5,
          marginBottom: 12,
          justifyContent: 'center',
        },
        textInput: {
          height: '100%',
          paddingHorizontal: 10,
          color: colorScheme === 'dark' ? '#FFF' : '#000',
        },
        placeholderOverlay: {
          position: 'absolute',
          flexDirection: 'row',
          justifyContent: 'space-between',
          alignItems: 'center',
          width: '100%',
          height: '100%', // Garante que o overlay ocupe toda a altura do contêiner
          paddingHorizontal: 10,
          ...Platform.select({
            web: {
              cursor: 'text',
            },
          }),
        } as any,
        placeholderText: {
          color: colorScheme === 'dark' ? '#8e8e8e' : 'gray',
        },
        forgotPasswordText: {
          color: '#007BFF',
          fontWeight: '500',
          ...Platform.select({
            web: {
              cursor: 'pointer',
            },
          }),
        } as any,
        button: {
          width: '100%',
          backgroundColor: '#007BFF',
          paddingVertical: 12,
          borderRadius: 5,
          alignItems: 'center',
          marginTop: 10,
        },
        buttonDisabled: {
          backgroundColor: '#A9A9A9',
        },
        buttonText: {
          color: '#fff',
          fontSize: 16,
          fontWeight: 'bold',
        },
        checkboxContainer: {
          flexDirection: 'row',
          alignItems: 'center',
          alignSelf: 'flex-start',
          marginBottom: 20,
        },
        checkbox: {
          width: 20,
          height: 20,
          borderRadius: 3,
          borderWidth: 1.5,
          borderColor: colorScheme === 'dark' ? '#8e8e8e' : 'gray',
          justifyContent: 'center',
          alignItems: 'center',
          marginRight: 10,
        },
        checkboxChecked: {
          backgroundColor: '#007BFF',
          borderColor: '#007BFF',
        },
        checkmark: {
          color: '#fff',
          fontSize: 12,
          fontWeight: 'bold',
        },
        checkboxLabel: {
          fontSize: 16,
          color: colorScheme === 'dark' ? '#FFF' : '#000',
        },
        signupText: {
          marginTop: 20,
          color: colorScheme === 'dark' ? '#8e8e8e' : 'gray',
          fontSize: 16,
        },
        signupLink: {
          color: '#007BFF',
          fontWeight: 'bold',
        },
      }),
    [colorScheme]
  );

  return (
    <KeyboardAvoidingView
      style={styles.keyboardAvoidingContainer}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}>
      <ScrollView
        contentContainerStyle={styles.scrollViewContent}
        keyboardShouldPersistTaps="handled">
        <TouchableWithoutFeedback onPress={Keyboard.dismiss}>
          <View style={styles.container}>
            <View style={styles.formWrapper}>
              <Text style={styles.title}>Login</Text>
              <View style={styles.inputContainer}>
                <TextInput
                  ref={usernameInputRef}
                  style={styles.textInput}
                  value={username}
                  onChangeText={setUsername}
                  autoCapitalize="none"
                  editable={!isLoading}
                  returnKeyType="next"
                  onSubmitEditing={() => passwordInputRef.current?.focus()}
                  blurOnSubmit={false}
                  onFocus={() => setIsUsernameFocused(true)}
                  onBlur={() => setIsUsernameFocused(false)}
                />
                {!isUsernameFocused && !username ? (
                  <TouchableOpacity
                    style={styles.placeholderOverlay}
                    activeOpacity={1}
                    onPress={() => usernameInputRef.current?.focus()}>
                    <Text style={styles.placeholderText}>Usuário</Text>
                  </TouchableOpacity>
                ) : null}
              </View>
              <View style={styles.inputContainer}>
                <TextInput
                  ref={passwordInputRef}
                  style={styles.textInput}
                  value={password}
                  onChangeText={setPassword}
                  secureTextEntry
                  editable={!isLoading}
                  returnKeyType="go"
                  onSubmitEditing={handleLogin}
                  onFocus={() => setIsPasswordFocused(true)}
                  onBlur={() => setIsPasswordFocused(false)}
                />
                {!isPasswordFocused && !password ? (
                  <TouchableOpacity
                    style={styles.placeholderOverlay}
                    activeOpacity={1}
                    onPress={() => passwordInputRef.current?.focus()}>
                    <Text style={styles.placeholderText}>Senha</Text>
                    <Text
                      style={styles.forgotPasswordText}
                      onPress={(e) => {
                        // Impede que o evento de clique se propague para o TouchableOpacity pai
                        e.stopPropagation();
                        router.push('/forgot-password');
                      }}>
                      Esqueci a senha
                    </Text>
                  </TouchableOpacity>
                ) : null}
              </View>
              <TouchableOpacity
                style={styles.checkboxContainer}
                onPress={() => setRememberMe(!rememberMe)}
                activeOpacity={0.8}>
                <View style={[styles.checkbox, rememberMe && styles.checkboxChecked]}>
                  {rememberMe && <Text style={styles.checkmark}>✓</Text>}
                </View>
                <Text style={styles.checkboxLabel}>Lembrar neste dispositivo</Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={[styles.button, isLoading && styles.buttonDisabled]}
                onPress={handleLogin}
                disabled={isLoading}>
                {isLoading ? (
                  <ActivityIndicator color="#fff" />
                ) : (
                  <Text style={styles.buttonText}>Entrar</Text>
                )}
              </TouchableOpacity>
              <Text style={styles.signupText}>
                Não tem uma conta?{' '}
                <Text style={styles.signupLink} onPress={() => router.push('/(auth)/register')}>
                  Registrar
                </Text>
              </Text>
            </View>
          </View>
        </TouchableWithoutFeedback>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}
