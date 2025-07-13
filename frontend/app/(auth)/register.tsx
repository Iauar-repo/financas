//app/(auth)/register.tsx
import React, { useState, useMemo, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  ActivityIndicator,
  Platform,
} from 'react-native';
import { useRouter, Stack } from 'expo-router';
import { useColorScheme } from '@/hooks/useColorScheme';
import { register } from '@/services/authService';

// Reutilizando a função de alerta para consistência
function showAlert(title: string, message: string) {
  if (Platform.OS === 'web') {
    alert(`${title}\n\n${message}`);
  } else {
    import('react-native').then(({ Alert }) => {
      Alert.alert(title, message);
    });
  }
}

export default function RegisterScreen() {
  const colorScheme = useColorScheme();
  const router = useRouter();

  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Estados para o foco para lidar com o placeholder
  const [isUsernameFocused, setIsUsernameFocused] = useState(false);
  const [isEmailFocused, setIsEmailFocused] = useState(false);
  const [isPasswordFocused, setIsPasswordFocused] = useState(false);
  const [isConfirmPasswordFocused, setIsConfirmPasswordFocused] = useState(false);

  // Refs para os inputs
  const usernameInputRef = useRef<TextInput>(null);
  const emailInputRef = useRef<TextInput>(null);
  const passwordInputRef = useRef<TextInput>(null);
  const confirmPasswordInputRef = useRef<TextInput>(null);

  const handleRegister = async () => {
    if (!username.trim() || !email.trim() || !password.trim() || !confirmPassword.trim()) {
      showAlert('Erro', 'Por favor, preencha todos os campos.');
      return;
    }

    if (password !== confirmPassword) {
      showAlert('Erro', 'As senhas não coincidem.');
      return;
    }

    setIsLoading(true);
    try {
      await register(username, email, password);
      showAlert('Sucesso', 'Conta criada com sucesso! Você será redirecionado para o login.');
      router.replace('/login'); // Navega de volta para a tela de login
    } catch (error) {
      console.error('Erro de Registro:', error);
      if (error instanceof Error) {
        showAlert('Falha no Registro', error.message);
      } else {
        showAlert('Erro de Conexão', 'Não foi possível conectar ao servidor.');
      }
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
          alignItems: 'center',
          width: '100%',
          height: '100%',
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
        loginText: {
          marginTop: 20,
          color: colorScheme === 'dark' ? '#8e8e8e' : 'gray',
          fontSize: 16,
        },
        loginLink: {
          color: '#007BFF',
          fontWeight: 'bold',
        },
      }),
    [colorScheme]
  );

  return (
    <>
      <Stack.Screen options={{ title: 'Criar Conta' }} />
      <View style={styles.container}>
        <View style={styles.formWrapper}>
          <Text style={styles.title}>Criar Conta</Text>

          {/* Input de Usuário */}
          <View style={styles.inputContainer}>
            <TextInput
              ref={usernameInputRef}
              style={styles.textInput}
              value={username}
              onChangeText={setUsername}
              autoCapitalize="none"
              editable={!isLoading}
              returnKeyType="next"
              onSubmitEditing={() => emailInputRef.current?.focus()}
              blurOnSubmit={false}
              onFocus={() => setIsUsernameFocused(true)}
              onBlur={() => setIsUsernameFocused(false)}
            />
            {!isUsernameFocused && !username && (
              <TouchableOpacity
                style={styles.placeholderOverlay}
                activeOpacity={1}
                onPress={() => usernameInputRef.current?.focus()}>
                <Text style={styles.placeholderText}>Usuário</Text>
              </TouchableOpacity>
            )}
          </View>

          {/* Input de E-mail */}
          <View style={styles.inputContainer}>
            <TextInput
              ref={emailInputRef}
              style={styles.textInput}
              value={email}
              onChangeText={setEmail}
              autoCapitalize="none"
              keyboardType="email-address"
              editable={!isLoading}
              returnKeyType="next"
              onSubmitEditing={() => passwordInputRef.current?.focus()}
              blurOnSubmit={false}
              onFocus={() => setIsEmailFocused(true)}
              onBlur={() => setIsEmailFocused(false)}
            />
            {!isEmailFocused && !email && (
              <TouchableOpacity
                style={styles.placeholderOverlay}
                activeOpacity={1}
                onPress={() => emailInputRef.current?.focus()}>
                <Text style={styles.placeholderText}>E-mail</Text>
              </TouchableOpacity>
            )}
          </View>

          {/* Input de Senha */}
          <View style={styles.inputContainer}>
            <TextInput
              ref={passwordInputRef}
              style={styles.textInput}
              value={password}
              onChangeText={setPassword}
              secureTextEntry
              editable={!isLoading}
              returnKeyType="go"
              onSubmitEditing={() => confirmPasswordInputRef.current?.focus()}
              onFocus={() => setIsPasswordFocused(true)}
              onBlur={() => setIsPasswordFocused(false)}
            />
            {!isPasswordFocused && !password && (
              <TouchableOpacity
                style={styles.placeholderOverlay}
                activeOpacity={1}
                onPress={() => passwordInputRef.current?.focus()}>
                <Text style={styles.placeholderText}>Senha</Text>
              </TouchableOpacity>
            )}
          </View>

          {/* Input de Confirmar Senha */}
          <View style={styles.inputContainer}>
            <TextInput
              ref={confirmPasswordInputRef}
              style={styles.textInput}
              value={confirmPassword}
              onChangeText={setConfirmPassword}
              secureTextEntry
              editable={!isLoading}
              returnKeyType="go"
              onSubmitEditing={handleRegister}
              onFocus={() => setIsConfirmPasswordFocused(true)}
              onBlur={() => setIsConfirmPasswordFocused(false)}
            />
            {!isConfirmPasswordFocused && !confirmPassword && (
              <TouchableOpacity
                style={styles.placeholderOverlay}
                activeOpacity={1}
                onPress={() => confirmPasswordInputRef.current?.focus()}
              >
                <Text style={styles.placeholderText}>Confirmar Senha</Text>
              </TouchableOpacity>
            )}
          </View>

          <TouchableOpacity
            style={[styles.button, isLoading && styles.buttonDisabled]}
            onPress={handleRegister}
            disabled={isLoading}>
            {isLoading ? (
              <ActivityIndicator color="#fff" />
            ) : (
              <Text style={styles.buttonText}>Registrar</Text>
            )}
          </TouchableOpacity>

          <Text style={styles.loginText}>
            Já tem uma conta?{' '}
            <Text style={styles.loginLink} onPress={() => router.back()}>
              Faça Login
            </Text>
          </Text>
        </View>
      </View>
    </>
  );
}