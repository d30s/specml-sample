// Import shared types
import @/shared/data/base.data.spec
import @/shared/data/money.data.spec

// Single item in an order
OrderItem {
  productId string<ulid>
  productName string<trim>
  sku string<uppercase>
  quantity number<min:1|max:999>
  unitPrice#Money
  subtotal#Money
}

// Complete order structure
Order {
  >Timestamps
  id string<ulid>
  orderNumber string<unique>
  customerId string<ulid>
  
  // Order items
  items#OrderItem[]
  
  // Pricing
  subtotal#Money
  taxAmount#Money
  shippingAmount#Money
  discountAmount? Money
  totalAmount#Money
  
  // Addresses
  shippingAddress#Address
  billingAddress#Address
  
  // Status and tracking
  status string(pending|confirmed|processing|shipped|delivered|cancelled)
  paymentStatus string(pending|authorized|captured|failed|refunded)
  trackingNumber? string
  estimatedDelivery? string<isISO>
  
  // Optional fields
  customerEmail string<isEmail>
  customerPhone? string
  notes? string<maxLength:500>
}

// Simplified order for list responses
OrderSummary {
  id string
  orderNumber string
  customerId string
  totalAmount#Money
  status string
  paymentStatus string
  createdAt string<isISO>
}
