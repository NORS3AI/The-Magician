# Project Todo

Development tasks and requirements for The-Magician.

---

## Player Account System

### Requirements

- [ ] **Encrypted Account Storage**
  - [ ] Hash passwords using secure algorithm (bcrypt or argon2)
  - [ ] Generate unique key tokens for session management
  - [ ] Store credentials securely (never plain text)

- [ ] **Password Requirements**
  - [ ] Minimum 8 characters
  - [ ] English characters only (a-z, A-Z, 0-9, common symbols)
  - [ ] Validate on registration and password change

- [ ] **Email Integration**
  - [ ] Email field required at registration
  - [ ] Password reset via email link
  - [ ] Username reminder via email
  - [ ] Email verification (optional but recommended)

- [ ] **Account Features**
  - [ ] Create new account (register)
  - [ ] Login with username/password
  - [ ] Logout and session cleanup
  - [ ] Forgot password flow
  - [ ] Forgot username flow
  - [ ] Change password (when logged in)

### System Structure (Skeleton)

```
src/
├── auth/
│   ├── __init__.py
│   ├── account.py          # Account creation, login, logout
│   ├── password.py         # Hashing, validation, reset logic
│   ├── token.py            # Session tokens, key generation
│   └── email_service.py    # Email sending for reset/reminder
├── data/
│   └── users/              # Encrypted user data storage
├── config/
│   └── auth_config.py      # Auth settings (token expiry, hash rounds)
└── utils/
    └── validation.py       # Input validation (password rules, email format)
```

### Implementation Notes

1. **Password Hashing**
   - Use `bcrypt` or `argon2-cffi` library
   - Salt automatically included with bcrypt
   - Cost factor of 12+ recommended

2. **Token Generation**
   - Use `secrets` module for cryptographic tokens
   - Tokens should expire (configurable, e.g., 24 hours for reset)
   - Store token hashes, not raw tokens

3. **Email Service**
   - For localhost/dev: use `smtplib` with a test SMTP server or logging
   - Production: integrate with service (SendGrid, Mailgun, etc.)
   - Templates for reset and reminder emails

4. **Validation Rules**
   ```
   Password:
   - Length: 8+ characters
   - Allowed: a-z, A-Z, 0-9, !@#$%^&*()_+-=
   - Not allowed: Unicode, spaces, non-English characters

   Username:
   - Length: 3-20 characters
   - Allowed: a-z, A-Z, 0-9, underscore
   - Must be unique

   Email:
   - Valid email format
   - Must be unique
   ```

5. **Security Considerations**
   - Rate limit login attempts
   - Rate limit password reset requests
   - Secure token transmission (HTTPS in production)
   - Don't reveal if username/email exists on reset requests

---

## Future Tasks

- [ ] Game engine core
- [ ] Story system and chapter loading
- [ ] Combat system implementation
- [ ] Inventory system
- [ ] Save/load game state
- [ ] Character creation flow
