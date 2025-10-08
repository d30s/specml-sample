// Common timestamp fields for all entities
Timestamps {
  createdAt string<isISO>
  updatedAt string<isISO>
}

// Standard address structure
Address {
  streetLine1 string<trim|minLength:3|maxLength:100>
  streetLine2? string<trim|maxLength:100>
  city string<trim|minLength:2|maxLength:50>
  state string<trim|length:2|uppercase>
  postalCode string<trim|minLength:5|maxLength:10>
  country string<length:2|uppercase>
}

// Pagination for list responses
Pagination {
  page number<min:1>
  limit number<min:1|max:100>
  total number<min:0>
  totalPages number<min:0>
  hasMore boolean
}
