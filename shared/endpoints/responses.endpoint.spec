// Standard error response
ApiError {
  error string
  message string
  timestamp string<isISO>
  requestId string
}

// Validation error with field details
ValidationError {
  error string
  message string
  timestamp string<isISO>
  requestId string
  details[] {
    field string
    message string
    code string
  }
}
