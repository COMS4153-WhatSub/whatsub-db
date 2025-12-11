# WhatSub Database Handler

A Python-based database handler for managing user subscriptions and reminders. This service provides RESTful API endpoints to handle CRUD operations for users, subscriptions, and reminders using a MySQL database.

## Database Schema

### Overview
The system manages three main entities:
- **Users**: People who have subscriptions
- **Subscriptions**: Services/products that users subscribe to
- **Notifications**: Notifications sent to users about their subscriptions (e.g., billing reminders)

### Entity Relationship Diagram
```
users (1) ----< (N) subscriptions (1) ----< (N) notifications
                |                              |
                +----------< (N) notifications-+
```
Note: Notifications reference both the subscription and the user directly.

### Table Schemas

#### Users Table
Stores user information.

| Column      | Type          | Constraints                    | Description                  |
|-------------|---------------|--------------------------------|------------------------------|
| user_id     | CHAR(36)      | PRIMARY KEY                    | Unique user identifier (UUID)|
| username    | VARCHAR(100)  | NOT NULL                       | User's username              |
| email       | VARCHAR(255)  | NOT NULL, UNIQUE               | User's email address         |
| phone       | VARCHAR(20)   | NULL                           | User's phone number          |
| created_at  | TIMESTAMP     | DEFAULT CURRENT_TIMESTAMP      | Account creation timestamp   |

**Indexes:**
- `idx_email`: On email column (UNIQUE)
- `idx_username`: On username column

---

#### Subscriptions Table
Stores subscription information for users.

| Column           | Type                                       | Constraints                              | Description                     |
|------------------|--------------------------------------------|------------------------------------------|---------------------------------|
| subscription_id  | INT                                        | PRIMARY KEY, AUTO_INCREMENT              | Unique subscription identifier  |
| user_id          | CHAR(36)                                   | NOT NULL, FOREIGN KEY → users.user_id    | Owner of the subscription       |
| name             | VARCHAR(255)                               | NOT NULL                                 | Subscription service name       |
| url              | VARCHAR(500)                               | NULL                                     | Subscription service URL        |
| account          | VARCHAR(255)                               | NULL                                     | Account identifier/username     |
| billing_type     | ENUM('monthly', 'quarterly', 'annualy')    | NOT NULL                                 | Billing frequency               |
| billing_date     | DATE                                       | NULL                                     | Next billing date               |
| price            | DECIMAL(10, 2)                             | NULL                                     | Subscription price              |
| created_at       | TIMESTAMP                                  | DEFAULT CURRENT_TIMESTAMP                | Subscription creation timestamp |

**Indexes:**
- `idx_user_id`: On user_id column
- `idx_billing_date`: On billing_date column
- `idx_billing_type`: On billing_type column

**Billing Types:**
- `monthly`: Billed every month
- `quarterly`: Billed every 3 months
- `annualy`: Billed every year

---

#### Notifications Table
Stores notifications for subscriptions.

| Column            | Type                                          | Constraints                                            | Description                         |
|-------------------|-----------------------------------------------|--------------------------------------------------------|-------------------------------------|
| notification_id   | INT                                           | PRIMARY KEY, AUTO_INCREMENT                            | Unique notification identifier      |
| subscription_id   | INT                                           | NOT NULL, FOREIGN KEY → subscriptions.subscription_id  | Associated subscription             |
| user_id           | VARCHAR(36)                                   | NOT NULL, FOREIGN KEY → users.user_id                  | User to notify                      |
| notification_type | ENUM('email', 'sms', 'push')                  | NOT NULL, DEFAULT 'push'                               | Delivery channel                    |
| subject           | VARCHAR(255)                                  | NULL                                                   | Notification subject/title          |
| message           | TEXT                                          | NULL                                                   | Notification message body           |
| status            | ENUM('queued', 'sent', 'delivered', 'failed') | NOT NULL, DEFAULT 'queued'                             | Current delivery status             |
| recipient_email   | VARCHAR(255)                                  | NULL                                                   | Email address for email type        |
| device_token      | VARCHAR(500)                                  | NULL                                                   | Device token for push notifications |
| read_at           | DATETIME                                      | NULL                                                   | When notification was read          |
| delivered_at      | DATETIME                                      | NULL                                                   | When notification was delivered     |
| created_at        | DATETIME                                      | NOT NULL, DEFAULT CURRENT_TIMESTAMP                    | Notification creation timestamp     |
| updated_at        | DATETIME                                      | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE          | Last update timestamp               |

**Indexes:**
- `idx_subscription_id`: On subscription_id column
- `idx_user_id`: On user_id column
- `idx_status`: On status column
- `idx_created_at`: On created_at column

**Notification Types:**
- `email`: Send via email to recipient_email
- `sms`: Send via SMS
- `push`: Send via push notification using device_token

**Status Values:**
- `queued`: Notification is waiting to be sent
- `sent`: Notification has been sent
- `delivered`: Notification was successfully delivered
- `failed`: Notification delivery failed

---

## Installation

### Prerequisites
- Python 3.8+
- MySQL 5.7+
- Access to MySQL database at `34.121.216.146`

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd whatsub-db
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file with database credentials:
```bash
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=whatsub
```

4. Initialize the database schema:
```bash
mysql -h 34.121.216.146 -u your_username -p < schema.sql
```

---

## API Endpoints

### User Endpoints

#### Create User
```http
POST /users
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "phone": "+1234567890"
}
```

#### Get User
```http
GET /users/{user_id}
```

#### Get All Users
```http
GET /users
```

#### Update User
```http
PUT /users/{user_id}
Content-Type: application/json

{
  "username": "john_updated",
  "email": "john_new@example.com",
  "phone": "+9876543210"
}
```

#### Delete User
```http
DELETE /users/{user_id}
```

---

### Subscription Endpoints

#### Create Subscription
```http
POST /subscriptions
Content-Type: application/json

{
  "user_id": 1,
  "name": "Netflix",
  "url": "https://netflix.com",
  "account": "john@example.com",
  "billing_date": "2025-10-15",
  "price": 15.99
}
```

#### Get Subscription
```http
GET /subscriptions/{subscription_id}
```

#### Get User Subscriptions
```http
GET /users/{user_id}/subscriptions
```

#### Update Subscription
```http
PUT /subscriptions/{subscription_id}
Content-Type: application/json

{
  "name": "Netflix Premium",
  "price": 19.99,
  "billing_date": "2025-11-15"
}
```

#### Delete Subscription
```http
DELETE /subscriptions/{subscription_id}
```

---

### Reminder Endpoints

#### Create Reminder
```http
POST /reminders
Content-Type: application/json

{
  "subscription_id": 1,
  "reminder_type": "pre_billing",
  "reminder_date": "2025-10-10 09:00:00",
  "message": "Netflix billing in 5 days"
}
```

#### Get Reminder
```http
GET /reminders/{reminder_id}
```

#### Get Subscription Reminders
```http
GET /subscriptions/{subscription_id}/reminders
```

#### Get User Reminders
```http
GET /users/{user_id}/reminders
```

#### Update Reminder
```http
PUT /reminders/{reminder_id}
Content-Type: application/json

{
  "reminder_type": "custom",
  "reminder_date": "2025-10-12 10:00:00",
  "message": "Updated reminder message",
  "is_sent": true
}
```

#### Delete Reminder
```http
DELETE /reminders/{reminder_id}
```

---

### Health Check
```http
GET /health
```

---

## Running the Application

### Development Mode
```bash
python app.py
```

The server will start on `http://0.0.0.0:5000`

### Production Mode
Use a WSGI server like Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## Database Connection

The application connects to the MySQL database at:
- **Host**: `34.121.216.146`
- **Database**: `whatsub` (configurable via `.env`)
- **User**: Set in `.env` file
- **Password**: Set in `.env` file

---

## Error Handling

All endpoints return appropriate HTTP status codes:
- `200 OK`: Successful GET/PUT/DELETE
- `201 Created`: Successful POST
- `400 Bad Request`: Invalid request data
- `404 Not Found`: Resource not found

Error responses include a JSON object with an error message:
```json
{
  "error": "Error description"
}
```

---

## Features

- **CRUD Operations**: Full create, read, update, delete operations for all entities
- **Cascade Deletes**: Deleting a user removes all their subscriptions and reminders
- **Type Safety**: Strong typing with Python type hints
- **Connection Management**: Automatic database connection handling
- **Error Handling**: Comprehensive error handling with rollback support
- **Flexible Updates**: Update only the fields you need to change

---

## Project Structure

```
whatsub-db/
├── app.py              # Flask application with API routes
├── db_handler.py       # Database handler class
├── schema.sql          # Database schema definition
├── requirements.txt    # Python dependencies
├── .env                # Environment variables (not in git)
├── .gitignore          # Git ignore file
└── README.md           # This file
```
