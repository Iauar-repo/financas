import React, { useEffect, useState } from 'react';
import { View, Text } from 'react-native';

export default function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch('http://SEU_IP_OU_URL_DO_BACKEND:PORTA/sua-rota')
      .then(response => response.json())
      .then(json => setData(json))
      .catch(error => console.error(error));
  }, []);

  return (
    <View style={{ flex:1, justifyContent: 'center', alignItems: 'center' }}>
      <Text>Dados do backend:</Text>
      <Text>{data ? JSON.stringify(data) : 'Carregando...'}</Text>
    </View>
  );
}
