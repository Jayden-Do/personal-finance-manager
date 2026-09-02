# Authentication Design

## Overview

Authentication is handled by the FastAPI backend.

Next.js acts as the client and consumes authentication APIs provided
by FastAPI.

JWT is used as the authentication mechanism instead of server-side
sessions.

## Responsibilities

### FastAPI

- Register users
- Authenticate users
- Hash and verify passwords
- Issue JWT access tokens
- Validate JWT access tokens
- Identify the authenticated user
- Enforce authorization

### Next.js

- Provide login/register UI
- Send authentication requests to FastAPI
- Store/use authentication credentials
- Include JWT when calling protected APIs

## Authentication Flow

### Registration

Client
→ POST /auth/register
→ FastAPI
→ validate user
→ hash password
→ create User
→ return response

### Login

Client
→ POST /auth/login
→ FastAPI
→ verify credentials
→ issue JWT
→ return JWT

### Authenticated Request

Client
→ Authorization: Bearer <JWT>
→ FastAPI
→ validate JWT
→ identify User
→ authorize request
→ endpoint

## JWT Design

### Payload

- `sub`: User ID
- `username`: Username
- `exp`: Token expiration timestamp

### Token Lifetime

Access tokens expire after 2 days.

### Algorithm

HS256.

### Secret

The JWT signing secret is provided through environment configuration
and must not be committed to source control.