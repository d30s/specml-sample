// Import dependencies
import @/shared/endpoints/headers.endpoint.spec
import @/shared/endpoints/responses.endpoint.spec
import @/shared/data/base.data.spec
import @/shared/data/money.data.spec
import @/orders/data/order.data.spec

// Create new order endpoint
CreateOrderEndpoint {
  method POST
  path /api/orders
  
  headers {
    >AuthHeaders
    >RequestHeaders
  }
  
  body {
    customerId string<ulid>
    
    // Order items
    items[] {
      productId string<ulid>
      quantity number<min:1|max:999>
    }
    
    // Addresses
    shippingAddress#Address
    billingAddress#Address?  // Optional, defaults to shipping if not provided
    
    // Payment
    paymentMethodId string<ulid>
    
    // Optional fields
    couponCode? string<uppercase|trim>
    notes? string<maxLength:500>
  }
  
  response {
    // Successful order creation
    success {
      status 201
      headers {
        Location string
        X-Request-ID string
      }
      body#Order
    }
    
    // Validation errors (invalid input)
    validation_error {
      status 422
      body#ValidationError
    }
    
    // Product out of stock
    out_of_stock {
      status 409
      body {
        error string
        message string
        timestamp string<isISO>
        requestId string
        unavailableItems[] {
          productId string
          requestedQuantity number
          availableQuantity number
        }
      }
    }
    
    // Payment failed
    payment_failed {
      status 402
      body {
        error string
        message string
        timestamp string<isISO>
        requestId string
        paymentError string
      }
    }
    
    // Unauthorized
    unauthorized {
      status 401
      body#ApiError
    }
    
    // Server error
    server_error {
      status 500
      body#ApiError
    }
  }
}
