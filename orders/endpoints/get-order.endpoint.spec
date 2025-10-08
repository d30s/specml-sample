import @/shared/endpoints/headers.endpoint.spec
import @/shared/endpoints/responses.endpoint.spec
import @/orders/data/order.data.spec

GetOrderEndpoint {
  method GET
  path /api/orders/:orderId
  
  headers {
    >AuthHeaders
  }
  
  params {
    orderId string<ulid>
  }
  
  response {
    success {
      status 200
      body#Order
    }
    
    not_found {
      status 404
      body#ApiError
    }
    
    unauthorized {
      status 401
      body#ApiError
    }
  }
}
