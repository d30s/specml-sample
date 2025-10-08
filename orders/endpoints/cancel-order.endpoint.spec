import @/shared/endpoints/headers.endpoint.spec
import @/shared/endpoints/responses.endpoint.spec
import @/orders/data/order.data.spec

CancelOrderEndpoint {
  method POST
  path /api/orders/:orderId/cancel
  
  headers {
    >AuthHeaders
    >RequestHeaders
  }
  
  params {
    orderId string<ulid>
  }
  
  body {
    reason string<trim|maxLength:500>
  }
  
  response {
    success {
      status 200
      body#Order
    }
    
    cannot_cancel {
      status 409
      body {
        error string
        message string
        timestamp string<isISO>
        requestId string
        currentStatus string
      }
    }
    
    not_found {
      status 404
      body#ApiError
    }
  }
}
