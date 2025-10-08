# SPECML Sample: E-commerce Order System

A practical example showing how to use SPECML and ASPECML to define an e-commerce order API.

## What is this?

This repo demonstrates how to organize and write SPECML schemas for a real-world API. You'll see how to define data structures, API endpoints, and reusable components using clean, readable syntax.

**Think of SPECML as:** Define your API once. Generate validators, docs, types, tests, and client SDKs from that single source of truth.

## Quick Look

Here's what a SPECML API endpoint looks like:

```specml
CreateOrderEndpoint {
  method POST
  path /api/orders
  
  body {
    customerId string<ulid>
    items[] {
      productId string<ulid>
      quantity number<min:1>
    }
    shippingAddress#Address
  }
  
  response {
    success {
      status 201
      body#Order
    }
    
    validation_error {
      status 422
      body#ValidationError
    }
  }
}
```

Clean. Readable. No JSON boilerplate. No YAML indentation headaches.

---

## The Problem SPECML Solves

You're probably maintaining:
- ❌ API docs in Swagger/OpenAPI
- ❌ Request validators in your backend code
- ❌ Response types in TypeScript
- ❌ Client SDK definitions
- ❌ Integration test schemas

When your API changes, you update **all of these separately**. They drift out of sync. Bugs slip through.

**With SPECML:**
- ✅ Write your API spec once
- ✅ Generate everything else automatically
- ✅ Single source of truth
- ✅ Never worry about drift again

---

## What You'll Learn

This sample shows you:

1. **How to organize schemas** - Separate data types from endpoints, shared types from domain-specific ones
2. **How to reuse definitions** - DRY principles with imports, references, and composition
3. **How to define APIs** - Request/response structures, validation rules, error scenarios
4. **Real-world patterns** - Money types, addresses, pagination, authentication
5. **How to scale** - Structure that grows with your API

---

## Project Structure

```
specml-sample/
├── .SPECML.config.json          # Configuration
├── shared/                       # Reusable types
│   ├── data/
│   │   ├── base.data.spec       # Timestamps, Address, Pagination
│   │   └── money.data.spec      # Money type (amount + currency)
│   └── endpoints/
│       ├── headers.endpoint.spec     # Auth headers, request headers
│       └── responses.endpoint.spec   # Error responses
└── orders/                      # Order domain
    ├── data/
    │   └── order.data.spec      # Order, OrderItem, OrderSummary
    └── endpoints/
        ├── create-order.endpoint.spec   # POST /api/orders
        └── list-orders.endpoint.spec    # GET /api/orders
```

**Key principle:** Separate **data** (what things are) from **endpoints** (how you interact with them).

---

## Reading the Specs (5-Minute Tutorial)

### 1. Basic Structure

Every line in SPECML has two parts:

```specml
fieldName type
```

Example:
```specml
email string
age number
isActive boolean
```

### 2. Adding Constraints

Use `<>` for validation rules:

```specml
email string<isEmail|lowercase>
age number<min:18|max:120>
username string<minLength:3|maxLength:20>
```

### 3. Allowed Values (Enums)

Use `()` for specific allowed values:

```specml
status string(pending|confirmed|shipped|delivered)
role string(admin|user|guest)
```

### 4. Nested Objects

Use `{}` to create structure:

```specml
Address {
  street string
  city string
  zipCode string
  country string
}
```

### 5. References

Use `#` to reference another type:

```specml
Order {
  shippingAddress#Address
  billingAddress#Address
}
```

Now both addresses have the same structure!

### 6. Arrays

Use `[]` for lists:

```specml
tags[] string
items#OrderItem[]
```

### 7. Optional Fields

Use `?` to make fields optional:

```specml
User {
  email string         // Required
  phone? string        // Optional
  bio? string          // Optional
}
```

### 8. Imports

Bring types from other files:

```specml
import @/shared/data/base.data.spec

Order {
  >Timestamps    // Copied from imported file
  orderNumber string
}
```

### 9. Copy Operator

Reuse fields with `>`:

```specml
Timestamps {
  createdAt string
  updatedAt string
}

Order {
  >Timestamps    // Copies createdAt and updatedAt
  orderNumber string
}
```

### 10. API Endpoints

Define your API routes:

```specml
CreateOrderEndpoint {
  method POST
  path /api/orders
  
  headers {
    Authorization string
  }
  
  body {
    customerId string
    items[] {
      productId string
      quantity number
    }
  }
  
  response {
    success {
      status 201
      body#Order
    }
    
    error {
      status 422
      body {
        error string
        message string
      }
    }
  }
}
```

---

## Key Patterns in This Sample

### Pattern 1: Shared Base Types

**Problem:** Every entity needs timestamps and you're copying them everywhere.

**Solution:** Define once, import everywhere.

```specml
// shared/data/base.data.spec
Timestamps {
  createdAt string<isISO>
  updatedAt string<isISO>
}

// orders/data/order.data.spec
import @/shared/data/base.data.spec

Order {
  >Timestamps    // Copies createdAt and updatedAt
  orderNumber string
}
```

### Pattern 2: Money Type

**Problem:** Amount and currency should always travel together.

**Solution:** Create a Money type.

```specml
// shared/data/money.data.spec
Money {
  amount number<min:0>
  currency string<uppercase|length:3>(USD|EUR|GBP)
}

// orders/data/order.data.spec
Order {
  subtotal#Money
  taxAmount#Money
  totalAmount#Money
}
```

Now you can't accidentally forget the currency!

### Pattern 3: Reusable Headers

**Problem:** Every endpoint needs the same auth headers.

**Solution:** Define once, copy everywhere.

```specml
// shared/endpoints/headers.endpoint.spec
AuthHeaders {
  Authorization string
  X-API-Key string
}

// orders/endpoints/create-order.endpoint.spec
CreateOrderEndpoint {
  headers {
    >AuthHeaders    // Copies both headers
    Content-Type string(application/json)
  }
}
```

### Pattern 4: Standard Error Responses

**Problem:** Error responses are inconsistent across endpoints.

**Solution:** Define standard error types.

```specml
// shared/endpoints/responses.endpoint.spec
ApiError {
  error string
  message string
  timestamp string<isISO>
  requestId string
}

ValidationError {
  error string
  message string
  details[] {
    field string
    message string
  }
}

// orders/endpoints/create-order.endpoint.spec
CreateOrderEndpoint {
  response {
    validation_error {
      status 422
      body#ValidationError    // Reuses structure
    }
    
    server_error {
      status 500
      body#ApiError          // Reuses structure
    }
  }
}
```

### Pattern 5: Domain Organization

**Problem:** Everything in one file becomes unmanageable.

**Solution:** Organize by domain.

```
orders/
  data/          # What orders are
  endpoints/     # How to interact with orders
  
products/
  data/          # What products are
  endpoints/     # How to interact with products
```

---

## What You Can Generate from These Specs

Using SPECML adapters, you can generate:

### 1. API Documentation (OpenAPI/Swagger)

```yaml
# Auto-generated from SPECML
openapi: 3.0.0
paths:
  /api/orders:
    post:
      summary: Create Order
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                customerId:
                  type: string
                items:
                  type: array
                  items:
                    type: object
                    # ... full schema
```

### 2. Request Validators (Node.js)

```javascript
// Auto-generated validator
const validateCreateOrder = (data) => {
  if (!data.customerId) {
    throw new ValidationError('customerId is required');
  }
  if (!Array.isArray(data.items) || data.items.length === 0) {
    throw new ValidationError('items must be a non-empty array');
  }
  // ... full validation logic
};
```

### 3. TypeScript Types

```typescript
// Auto-generated types
interface Money {
  amount: number;
  currency: 'USD' | 'EUR' | 'GBP';
}

interface OrderItem {
  productId: string;
  productName: string;
  quantity: number;
  unitPrice: Money;
  subtotal: Money;
}

interface Order {
  id: string;
  orderNumber: string;
  customerId: string;
  items: OrderItem[];
  subtotal: Money;
  totalAmount: Money;
  status: 'pending' | 'confirmed' | 'processing' | 'shipped' | 'delivered';
  createdAt: string;
  updatedAt: string;
}
```

### 4. Client SDKs

```javascript
// Auto-generated API client
const client = new OrdersAPI({
  baseUrl: 'https://api.example.com',
  apiKey: 'your-key'
});

// Type-safe, auto-completed
const order = await client.orders.create({
  customerId: '01CUSTOMER123',
  items: [
    { productId: '01PRODUCT456', quantity: 2 }
  ],
  shippingAddress: {
    street: '123 Main St',
    city: 'New York',
    state: 'NY',
    zipCode: '10001',
    country: 'US'
  }
});
```

### 5. Integration Tests

```javascript
// Auto-generated test templates
describe('POST /api/orders', () => {
  it('creates order successfully', async () => {
    const response = await request(app)
      .post('/api/orders')
      .send({
        customerId: '01CUSTOMER123',
        items: [/* ... */],
        shippingAddress: {/* ... */}
      });
    
    expect(response.status).toBe(201);
    expect(response.body).toMatchSchema(OrderSchema);
  });
  
  it('returns 422 for invalid data', async () => {
    const response = await request(app)
      .post('/api/orders')
      .send({ /* invalid data */ });
    
    expect(response.status).toBe(422);
    expect(response.body).toMatchSchema(ValidationErrorSchema);
  });
});
```

### 6. Mock Servers

```javascript
// Auto-generated mock server for testing
const mockServer = new SpecMLMockServer('orders/endpoints/');
mockServer.start(3000);

// Now you have a working API that returns valid responses
// Perfect for frontend development before backend is ready
```

---

## Try It Yourself

### Step 1: Read the Specs

Start with the shared types to understand the foundation:
1. `shared/data/base.data.spec` - See how timestamps and addresses work
2. `shared/data/money.data.spec` - See the Money type pattern

Then look at the order domain:
3. `orders/data/order.data.spec` - See how Order is structured
4. `orders/endpoints/create-order.endpoint.spec` - See a complete API endpoint

### Step 2: Trace the Imports

Follow the `import` statements to see how types are composed:
- How does `Order` get timestamps?
- Where does the `Money` type come from?
- How are `AuthHeaders` reused?

### Step 3: Modify Something

Try adding a new field:
1. Add `giftMessage? string` to the Order type
2. Add it to the CreateOrderEndpoint body
3. See how it flows through the system

### Step 4: Add a New Endpoint

Create `orders/endpoints/get-order.endpoint.spec`:

```specml
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
  }
}
```

### Step 5: Extend the Domain

Add products or customers following the same patterns.

---

## Common Questions

**Q: Do I need to learn a complex syntax?**  
A: No. If you can read `email string` and `age number`, you already understand 80% of SPECML.

**Q: Can I use this for existing APIs?**  
A: Yes! Start by documenting one endpoint, then gradually add more.

**Q: What if my API is complex?**  
A: SPECML scales. Use imports, references, and composition to manage complexity.

**Q: Do I need special tools?**  
A: To read and write specs? No, just a text editor. To generate code? Yes, you'll need SPECML adapters for your language/framework.

**Q: Is this production-ready?**  
A: SPECML is being used by teams in production. The syntax is stable.

**Q: Can I integrate with existing OpenAPI/Swagger?**  
A: Yes! Use adapters to convert between SPECML and OpenAPI formats.

---

## Next Steps

### 1. Read the Full Documentation

**Core SPECML:** Learn the complete syntax  
→ [SPECML Documentation](https://docs.specml.dev/)

**ASPECML for APIs:** Deep dive into API specifications  
→ [ASPECML Documentation](https://docs.specml.dev/a-specml-1647273m0)

### 2. Try SPECML in Your Project

**Start small:**
- Document one data type
- Define one endpoint
- Generate validators or types

**Then expand:**
- Add more endpoints
- Create shared types
- Build your schema library

### 3. Explore Adapters

**Official adapters:**
- `@specml/validator` - Runtime validation
- `@specml/typescript` - TypeScript type generation
- `@specml/openapi` - OpenAPI/Swagger conversion
- `@specml/mock` - Mock server generation

**Community adapters:**
- Database schema generators
- GraphQL schema generators
- Client SDK generators

### 4. Join the Community

- **GitHub:** [github.com/specml/specml](link)
- **Discord:** [Join our Discord](link)
- **Discussions:** Share your use cases and learn from others

---

## Why Teams Choose SPECML

> "We reduced API documentation drift from 'constant problem' to 'non-existent' in 2 weeks."  
> — *Engineering Lead, Fintech Startup*

> "Our frontend and backend teams finally speak the same language. Literally."  
> — *CTO, E-commerce Platform*

> "Onboarding new developers is 10x faster when they can read the API specs in plain English."  
> — *Developer, SaaS Company*

---

## License

This sample project is MIT licensed. Use it, learn from it, build with it.

---

## Contributing

Found an issue? Have a better pattern? PRs welcome!

1. Fork this repo
2. Create your feature branch
3. Make your changes
4. Submit a PR

---

**Ready to define your APIs with clarity?**  
Start with this sample, then adapt it to your needs. SPECML grows with you.

Happy spec-ing! 🚀
