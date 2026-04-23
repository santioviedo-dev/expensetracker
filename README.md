# ExpenseTracker

A lightweight personal finance tracking application built with Flask, MySQL, and Tailwind CSS.

---

## Features

- User authentication (register / login)
- Account management (cash, bank, etc.)
- Categories for income and expenses
- Transaction tracking
- Basic financial summaries (balance, totals)

---

## Tech Stack

- Backend: Flask
- Database: MySQL
- Frontend: Jinja2 + Tailwind CSS

---

## Project Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd expense-tracker
```

---

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Environment variables

Create a `.env` file in the root directory:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=expense_tracker
SECRET_KEY=your_secret_key
```

---

## Database Setup

### 1. Create database

```sql
CREATE DATABASE expense_tracker;
USE expense_tracker;
```

---

### 2. Create tables

#### users

```sql
CREATE TABLE users (
  id CHAR(36) PRIMARY KEY,
  email VARCHAR(255) UNIQUE,
  password_hash TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

#### accounts

```sql
CREATE TABLE accounts (
  id CHAR(36) PRIMARY KEY,
  user_id CHAR(36),
  name VARCHAR(100),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

#### categories

```sql
CREATE TABLE categories (
  id CHAR(36) PRIMARY KEY,
  user_id CHAR(36),
  name VARCHAR(100),
  type ENUM('income', 'expense'),
  FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

#### transactions

```sql
CREATE TABLE transactions (
  id CHAR(36) PRIMARY KEY,
  user_id CHAR(36),
  account_id CHAR(36),
  category_id CHAR(36),

  amount DECIMAL(10,2),
  type ENUM('income', 'expense'),
  description TEXT,
  date DATE,

  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (account_id) REFERENCES accounts(id),
  FOREIGN KEY (category_id) REFERENCES categories(id)
);
```

---

## Running the application

```bash
python run.py
```

Then open:

```
http://localhost:5000
```

---

## API (basic example)

### Create transaction

```
POST /transactions
```

Body:

```json
{
  "user_id": "uuid",
  "account_id": "uuid",
  "category_id": "uuid",
  "amount": 5000,
  "type": "expense",
  "date": "2026-04-22"
}
```

---

## Notes

- IDs are generated using UUIDs from Python
- Amount values are always stored as positive numbers
- Balance is calculated dynamically (not stored in database)

---

## Future Improvements

- Budgets per category/month
- Reports and charts
- Transfers between accounts
- CSV import/export