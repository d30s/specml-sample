// Money type - amount always paired with currency
Money {
  amount number<min:0>
  currency string<uppercase|length:3>(USD|EUR|GBP|CAD)
}
