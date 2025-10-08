// Import dependencies
import @/shared/endpoints/headers.endpoint.spec
import @/shared/endpoints/responses.endpoint.spec
import @/shared/data/base.data.spec
import @/orders/data/order.data.spec

// List orders with filtering and pagination
ListOrdersEndpoint {
  method GET
  path /api/orders
  
  headers {
    >AuthHeaders
  }
  
  query {
    // Pagination
    page? number<min:1>
    limit? number<min:1|max:100>
    
    // Filters
    customerId? string<ulid>
    status? string(pending|confirmed|processing|shipped|delivered|cancelled)
    paymentStatus? string(pending|authorized|captured|failed|refunded)
    
    // Date range
    startDate? string<isISO>
    endDate? string<isISO>
    
    // Sorting
    sortBy? string(createdAt|totalAmount|status)
    sortOrder? string(asc|desc)
    
    // Search
    search? string<minLength:2>  // Search by order number or customer email
  }
  
  response {
    // Successful retrieval
    success {
      status 200
      headers {
        X-Request-ID string
        X-Total-Count number
      }
      body {
        orders#OrderSummary[]
        pagination#Pagination
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
