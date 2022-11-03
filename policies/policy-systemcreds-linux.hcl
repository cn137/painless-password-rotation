# Allows admins to only read passwords.

path "systemcreds/*" {
  capabilities = ["list"]
}
path "systemcreds/data/linux/*" {
  capabilities = ["list", "read"]
}
path "systemcreds/metadata/linux/*" {
  capabilities = ["list", "read"]
}
