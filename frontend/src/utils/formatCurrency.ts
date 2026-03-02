export const formatINR = (amount: number): string => {
  if (!amount && amount !== 0) return '₹0'
  if (amount >= 10000000) return `₹${(amount / 10000000).toFixed(1)} Cr`
  if (amount >= 100000) return `₹${(amount / 100000).toFixed(1)}L`
  return `₹${amount.toLocaleString('en-IN')}`
}
export const formatCrore = (amount: number): string => `₹${amount.toFixed(1)} Cr`
export const formatCurrency = formatINR

