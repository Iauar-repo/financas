import React, { useState, useRef, useEffect, useMemo } from 'react';
import { useColorScheme } from '@/hooks/useColorScheme';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  ActivityIndicator,
  Platform,
  TouchableOpacity,
} from 'react-native';
import { useRouter } from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';

function showAlert(title: string, message: string) {
  if (Platform.OS === 'web') {
    alert(`${title}\n\n${message}`);
  } else {
    // Funciona no celular (Android/iOS)
    import('react-native').then(({ Alert }) => {
      Alert.alert(title, message);
    });
  }
}

export default function LoginScreen() {
  const colorScheme = useColorScheme();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isPasswordFocused, setIsPasswordFocused] = useState(false);
  const [isUsernameFocused, setIsUsernameFocused] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);
  const router = useRouter();
  const passwordInputRef = useRef<TextInput>(null);
  const usernameInputRef = useRef<TextInput>(null);

  useEffect(() => {
    const loadCredentials = async () => {
      try {
        const storedCredentials = await AsyncStorage.getItem('rememberedCredentials');
        if (storedCredentials) {
          const { username: storedUsername, password: storedPassword } =
            JSON.parse(storedCredentials);
          setUsername(storedUsername);
          setPassword(storedPassword);
          setRememberMe(true);
        }
      } catch (error) {
        showAlert('Erro', 'Falha ao carregar as credenciais salvas.');
      }
    };
    loadCredentials();
  }, []);

  const handleLogin = async () => {
    if (!username.trim() || !password.trim()) {
      showAlert('Erro', 'Por favor, preencha todos os campos.');
      return;
    }

    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:5000/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      if (response.ok) {
        if (rememberMe) {
          const credentials = { username, password };
          await AsyncStorage.setItem('rememberedCredentials', JSON.stringify(credentials));
        } else {
          // Se "Lembrar" não estiver marcado, removemos quaisquer credenciais salvas.
          await AsyncStorage.removeItem('rememberedCredentials');
        }

        // Navega para a tela principal do aplicativo (abas) após um login bem-sucedido.
        router.replace('/(tabs)');
      } else {
        const errorBody = await response.text();
        try {
          const errorData = JSON.parse(errorBody);
          showAlert('Falha no login', errorData.message || 'Senha ou usuário incorretos.');
        } catch (e) {
          console.error('Server error response (not JSON):', errorBody);
          showAlert('Erro no Servidor', `Ocorreu um erro inesperado (Status: ${response.status}).`);
        }
      }
    } catch (error) {
      console.error('Erro de Conexão:', error);
      showAlert('Erro de Conexão', 'Não foi possível conectar ao servidor. Verifique sua conexão com a internet e tente novamente.');
    } finally {
      setIsLoading(false);
    }
  };

  const styles = useMemo(
    () =>
      StyleSheet.create({
        container: {
          flex: 1,
          justifyContent: 'center',
          alignItems: 'center',
          padding: 20,
          backgroundColor: colorScheme === 'dark' ? '#121212' : '#FFF',
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
          <Text style={styles.signupLink} onPress={() => router.push('/register')}>
            Registrar
          </Text>
        </Text>
      </View>
    </View>
  );
}
