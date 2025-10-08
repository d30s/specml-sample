import @/shared/data/base.data.spec
import @/shared/data/money.data.spec

Product {
  >Timestamps
  id string<ulid>
  sku string<uppercase|unique>
  name string<trim|minLength:1|maxLength:200>
  description string<trim|maxLength:2000>
  price#Money
  stockQuantity number<min:0>
  isActive boolean
}
