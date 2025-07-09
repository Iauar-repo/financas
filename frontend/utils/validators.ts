export function isValidEmail(email: string): boolean {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email.toLowerCase());
}

export function isValidPassword(password: string): boolean {
  // Exemplo: mínimo 6 caracteres
  return password.length >= 6;
}

export function isValidUsername(username: string): boolean {
  return username.trim().length > 0;
}
