import React, { useState, useRef, useMemo } from 'react';
import { useColorScheme } from '@/hooks/useColorScheme';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  ActivityIndicator,
  Platform,
  Alert,
} from 'react-native';
import { useRouter } from 'expo-router';

export default function ForgotPasswordScreen() {
  const colorScheme = useColorScheme();
  const [email, setEmail] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isEmailFocused, setIsEmailFocused] = useState(false);
  const router = useRouter();
  const emailInputRef = useRef<TextInput>(null);

  const handlePasswordReset = async () => {
    if (!email.trim()) {
      Alert.alert('Erro', 'Por favor, insira seu e-mail.');
      return;
    }

    setIsLoading(true);
    // Simula uma chamada de API para redefinição de senha
    await new Promise(resolve => setTimeout(resolve, 1500));
    setIsLoading(false);

    Alert.alert(
      'Verifique seu E-mail',
      'Se uma conta com este e-mail existir, um link para redefinir a senha foi enviado.'
    );
    router.back();
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
          marginBottom: 10,
          color: colorScheme === 'dark' ? '#FFF' : '#000',
        },
        instructions: {
          fontSize: 16,
          textAlign: 'center',
          color: colorScheme === 'dark' ? '#8e8e8e' : 'gray',
          marginBottom: 20,
        },
        inputContainer: {
          width: '100%',
          height: 40,
          borderColor: colorScheme === 'dark' ? '#555' : 'gray',
          borderWidth: 1,
          borderRadius: 5,
          marginBottom: 20,
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
        },
        buttonDisabled: {
          backgroundColor: '#A9A9A9',
        },
        buttonText: {
          color: '#fff',
          fontSize: 16,
          fontWeight: 'bold',
        },
        backLink: {
          marginTop: 20,
          color: '#007BFF',
          fontSize: 16,
        },
      }),
    [colorScheme]
  );

  return (
    <View style={styles.container}>
      <View style={styles.formWrapper}>
        <Text style={styles.title}>Recuperar Senha</Text>
        <Text style={styles.instructions}>
          Insira o e-mail associado à sua conta e enviaremos um link para redefinir sua senha.
        </Text>

        {/* Usando o mesmo estilo de input customizado da tela de login */}
        <View style={styles.inputContainer}>
          <TextInput
            ref={emailInputRef}
            style={styles.textInput}
            value={email}
            onChangeText={setEmail}
            autoCapitalize="none"
            keyboardType="email-address"
            editable={!isLoading}
            returnKeyType="go"
            onSubmitEditing={handlePasswordReset}
            onFocus={() => setIsEmailFocused(true)}
            onBlur={() => setIsEmailFocused(false)}
          />
          {!isEmailFocused && !email ? (
            <TouchableOpacity
              style={styles.placeholderOverlay}
              activeOpacity={1}
              onPress={() => emailInputRef.current?.focus()}>
              <Text style={styles.placeholderText}>Seu e-mail</Text>
            </TouchableOpacity>
          ) : null}
        </View>

        <TouchableOpacity
          style={[styles.button, isLoading && styles.buttonDisabled]}
          onPress={handlePasswordReset}
          disabled={isLoading}>
          {isLoading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.buttonText}>Enviar Link</Text>
          )}
        </TouchableOpacity>
        <TouchableOpacity onPress={() => router.back()}>
          <Text style={styles.backLink}>Voltar para o Login</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}