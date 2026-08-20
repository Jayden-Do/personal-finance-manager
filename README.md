# Personal Finance Manager

A web application for managing personal finances through a modular plugin-based system.

## Overview

Personal Finance Manager allows users to manage their finances based on the features they need. Users can enable or disable plugins, and the application dynamically adapts its available functionality.

### Plugins

- **Expense Plugin**
  - Track income and expenses
  - Categorize transactions using labels
  - Filter transactions
  - Compare income and expenses across months

- **Savings Plugin**
  - Create and track savings goals
  - Record savings contributions
  - Assign labels to savings goals
  - Simulate accumulated savings based on saving period and annual return rate

- **Investment Plugin** *(Coming later)*
  - Track investment portfolios such as ETFs and mutual funds
  - Requires integration with a financial market API

## Tech Stack

### Backend

- FastAPI
- SQLAlchemy
- PostgreSQL

### Frontend

- Next.js

### Infrastructure

- Nginx
- Docker
- Kubernetes
- CI/CD

## Project Status

Currently in development.

The project is being developed incrementally, starting with the Expense and Savings plugins. The Investment plugin will be implemented in a future phase.

## Development

### Prerequisites

- Python 3.10+
- uv
- PostgreSQL
- Node.js 20+
