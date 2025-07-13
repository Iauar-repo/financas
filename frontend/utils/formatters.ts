
// utils/formatters.ts
export function formatCurrency(value: number | string, locale = 'pt-BR', currency = 'BRL') {
  const number = typeof value === 'string' ? parseFloat(value) : value;
  return new Intl.NumberFormat(locale, {
    style: 'currency',
    currency,
  }).format(number);
}

export function formatDate(date: string | Date, locale = 'pt-BR') {
  const d = typeof date === 'string' ? new Date(date) : date;
  return d.toLocaleDateString(locale);
}

export function formatDateTime(date: string | Date, locale = 'pt-BR') {
  const d = typeof date === 'string' ? new Date(date) : date;
  return d.toLocaleString(locale);
}
export function formatPercentage(value: number | string, locale = 'pt-BR') {
  const number = typeof value === 'string' ? parseFloat(value) : value;
  return new Intl.NumberFormat(locale, {
    style: 'percent',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(number);
}