# Password Rotation with HashiCorp Vault
This repository is a streamlined systemd setup for automating password rotation with Hashicorp Vault.

## Prerequisites
* Running Hashicorp Vault server instance. (Inbound TCP port 8200 to Vault)
* Seth Vargo's plugin configured and installed: [vault-secrets-gen plugin](https://github.com/sethvargo/vault-secrets-gen)
* Version 2 K/V secrets backend mounted at systemcreds:   
```
vault secrets enable -version=2 -path=systemcreds/ kv
```
### Vault Server Configuration
---
#### 1. Configure Policies:
```
 vault policy write policy-service-linux-rotate polcies/policy-service-linux-rotate.hcl
 vault policy write policy-systemcreds-linux policies/policy-systemcreds-linux.hcl
```

#### 2. Generate a token:
```
vault token create -period 960h -policy policy-service-linux-rotate -display-name service-linux-rotate
```

### Linux Host Configuration (System for which you need to rotate the password)
---
#### 1. Install package 
```
dnf install painless-password-rotation
```

#### 2. Update Environment File
Update Vault Address and Token in /etc/sysconfig/vault-rotate
```
VAULT_ADDR="https://your_vault.server.com:8200"
VAULT_TOKEN="hvs.my-vault-token"
```

#### 3. Run password rotation service
```bash
systemctl start rotate-password.service
```

#### 4. Log onto the Vault UI and verify that the password was saved successfully   

#### 5. Start/Enable password rotation timer
```bash
systemctl enable rotate-password.timer
systemctl start rotate-password.timer
```
