import @/shared/data/base.data.spec

Customer {
  >Timestamps
  id string<ulid>
  email string<isEmail|lowercase>
  firstName string<trim>
  lastName string<trim>
  phone? string
  status string(active|suspended|closed)
}
