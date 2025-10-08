// Standard headers for authenticated requests
AuthHeaders {
  Authorization string
  X-API-Key string
}

// Standard request headers
RequestHeaders {
  Content-Type string(application/json)
  X-Request-ID string<ulid>
}
