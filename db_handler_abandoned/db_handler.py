import mysql.connector
from mysql.connector import Error
from typing import Optional, Dict, List, Any
from datetime import datetime
import uuid


class DatabaseHandler:
    """Database handler for WhatSub subscription management system"""

    def __init__(self, config: Dict[str, str]):
        """
        Initialize database handler with connection configuration

        Args:
            config: Dictionary with keys: host, user, password, database
        """
        self.config = config
        self.connection = None

    def connect(self):
        """Establish database connection"""
        try:
            if self.connection is None or not self.connection.is_connected():
                self.connection = mysql.connector.connect(**self.config)
            return self.connection
        except Error as e:
            raise Exception(f"Database connection error: {e}")

    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def execute_query(self, query: str, params: tuple = None, fetch: bool = False) -> Any:
        """
        Execute a database query

        Args:
            query: SQL query string
            params: Query parameters
            fetch: Whether to fetch results

        Returns:
            Query results if fetch=True, otherwise last row id
        """
        connection = self.connect()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(query, params or ())

            if fetch:
                result = cursor.fetchall()
                return result
            else:
                connection.commit()
                return cursor.lastrowid
        except Error as e:
            connection.rollback()
            raise Exception(f"Query execution error: {e}")
        finally:
            cursor.close()

    # User Operations
    def create_user(self, username: str, email: str, phone: Optional[str] = None) -> str:
        """
        Create a new user

        Args:
            username: User's username
            email: User's email address
            phone: User's phone number (optional)

        Returns:
            Created user ID (UUID)
        """
        user_id = str(uuid.uuid4())
        query = """
            INSERT INTO users (user_id, username, email, phone, created_at)
            VALUES (%s, %s, %s, %s, %s)
        """
        self.execute_query(query, (user_id, username, email, phone, datetime.now()))
        return user_id

    def get_user(self, user_id: str) -> Optional[Dict]:
        """
        Get user by ID

        Args:
            user_id: User ID (UUID)

        Returns:
            User data dictionary or None
        """
        query = "SELECT * FROM users WHERE user_id = %s"
        result = self.execute_query(query, (user_id,), fetch=True)
        return result[0] if result else None

    def get_all_users(self) -> List[Dict]:
        """
        Get all users

        Returns:
            List of user data dictionaries
        """
        query = "SELECT * FROM users ORDER BY created_at DESC"
        return self.execute_query(query, fetch=True)

    def update_user(self, user_id: str, username: Optional[str] = None,
                   email: Optional[str] = None, phone: Optional[str] = None):
        """
        Update user information

        Args:
            user_id: User ID (UUID)
            username: New username (optional)
            email: New email (optional)
            phone: New phone (optional)
        """
        updates = []
        params = []

        if username is not None:
            updates.append("username = %s")
            params.append(username)
        if email is not None:
            updates.append("email = %s")
            params.append(email)
        if phone is not None:
            updates.append("phone = %s")
            params.append(phone)

        if not updates:
            return

        params.append(user_id)
        query = f"UPDATE users SET {', '.join(updates)} WHERE user_id = %s"
        self.execute_query(query, tuple(params))

    def delete_user(self, user_id: str):
        """
        Delete user and all associated data

        Args:
            user_id: User ID (UUID)
        """
        # Delete reminders for user's subscriptions
        query = """
            DELETE r FROM reminders r
            INNER JOIN subscriptions s ON r.subscription_id = s.subscription_id
            WHERE s.user_id = %s
        """
        self.execute_query(query, (user_id,))

        # Delete user's subscriptions
        query = "DELETE FROM subscriptions WHERE user_id = %s"
        self.execute_query(query, (user_id,))

        # Delete user
        query = "DELETE FROM users WHERE user_id = %s"
        self.execute_query(query, (user_id,))

    # Subscription Operations
    def create_subscription(self, user_id: str, name: str, url: Optional[str] = None,
                          account: Optional[str] = None, billing_date: Optional[str] = None,
                          price: Optional[float] = None) -> int:
        """
        Create a new subscription

        Args:
            user_id: User ID (UUID)
            name: Subscription name
            url: Subscription URL (optional)
            account: Account identifier (optional)
            billing_date: Billing date (optional)
            price: Subscription price (optional)

        Returns:
            Created subscription ID
        """
        query = """
            INSERT INTO subscriptions (user_id, name, url, account, billing_date, price, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        return self.execute_query(query, (user_id, name, url, account, billing_date, price, datetime.now()))

    def get_subscription(self, subscription_id: int) -> Optional[Dict]:
        """
        Get subscription by ID

        Args:
            subscription_id: Subscription ID

        Returns:
            Subscription data dictionary or None
        """
        query = "SELECT * FROM subscriptions WHERE subscription_id = %s"
        result = self.execute_query(query, (subscription_id,), fetch=True)
        return result[0] if result else None

    def get_user_subscriptions(self, user_id: str) -> List[Dict]:
        """
        Get all subscriptions for a user

        Args:
            user_id: User ID (UUID)

        Returns:
            List of subscription data dictionaries
        """
        query = "SELECT * FROM subscriptions WHERE user_id = %s ORDER BY created_at DESC"
        return self.execute_query(query, (user_id,), fetch=True)

    def update_subscription(self, subscription_id: int, name: Optional[str] = None,
                          url: Optional[str] = None, account: Optional[str] = None,
                          billing_date: Optional[str] = None, price: Optional[float] = None):
        """
        Update subscription information

        Args:
            subscription_id: Subscription ID
            name: New name (optional)
            url: New URL (optional)
            account: New account (optional)
            billing_date: New billing date (optional)
            price: New price (optional)
        """
        updates = []
        params = []

        if name is not None:
            updates.append("name = %s")
            params.append(name)
        if url is not None:
            updates.append("url = %s")
            params.append(url)
        if account is not None:
            updates.append("account = %s")
            params.append(account)
        if billing_date is not None:
            updates.append("billing_date = %s")
            params.append(billing_date)
        if price is not None:
            updates.append("price = %s")
            params.append(price)

        if not updates:
            return

        params.append(subscription_id)
        query = f"UPDATE subscriptions SET {', '.join(updates)} WHERE subscription_id = %s"
        self.execute_query(query, tuple(params))

    def delete_subscription(self, subscription_id: int):
        """
        Delete subscription and all associated reminders

        Args:
            subscription_id: Subscription ID
        """
        # Delete associated reminders
        query = "DELETE FROM reminders WHERE subscription_id = %s"
        self.execute_query(query, (subscription_id,))

        # Delete subscription
        query = "DELETE FROM subscriptions WHERE subscription_id = %s"
        self.execute_query(query, (subscription_id,))

    # Reminder Operations
    def create_reminder(self, subscription_id: int, reminder_type: str,
                       reminder_date: str, message: Optional[str] = None) -> int:
        """
        Create a new reminder

        Args:
            subscription_id: Subscription ID
            reminder_type: Type of reminder (e.g., 'pre_billing', 'after_payment')
            reminder_date: Date for reminder
            message: Reminder message (optional)

        Returns:
            Created reminder ID
        """
        query = """
            INSERT INTO reminders (subscription_id, reminder_type, reminder_date, message, is_sent, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        return self.execute_query(query, (subscription_id, reminder_type, reminder_date, message, False, datetime.now()))

    def get_reminder(self, reminder_id: int) -> Optional[Dict]:
        """
        Get reminder by ID

        Args:
            reminder_id: Reminder ID

        Returns:
            Reminder data dictionary or None
        """
        query = "SELECT * FROM reminders WHERE reminder_id = %s"
        result = self.execute_query(query, (reminder_id,), fetch=True)
        return result[0] if result else None

    def get_subscription_reminders(self, subscription_id: int) -> List[Dict]:
        """
        Get all reminders for a subscription

        Args:
            subscription_id: Subscription ID

        Returns:
            List of reminder data dictionaries
        """
        query = "SELECT * FROM reminders WHERE subscription_id = %s ORDER BY reminder_date ASC"
        return self.execute_query(query, (subscription_id,), fetch=True)

    def get_user_reminders(self, user_id: str) -> List[Dict]:
        """
        Get all reminders for a user's subscriptions

        Args:
            user_id: User ID (UUID)

        Returns:
            List of reminder data dictionaries
        """
        query = """
            SELECT r.* FROM reminders r
            INNER JOIN subscriptions s ON r.subscription_id = s.subscription_id
            WHERE s.user_id = %s
            ORDER BY r.reminder_date ASC
        """
        return self.execute_query(query, (user_id,), fetch=True)

    def update_reminder(self, reminder_id: int, reminder_type: Optional[str] = None,
                       reminder_date: Optional[str] = None, message: Optional[str] = None,
                       is_sent: Optional[bool] = None):
        """
        Update reminder information

        Args:
            reminder_id: Reminder ID
            reminder_type: New reminder type (optional)
            reminder_date: New reminder date (optional)
            message: New message (optional)
            is_sent: New is_sent status (optional)
        """
        updates = []
        params = []

        if reminder_type is not None:
            updates.append("reminder_type = %s")
            params.append(reminder_type)
        if reminder_date is not None:
            updates.append("reminder_date = %s")
            params.append(reminder_date)
        if message is not None:
            updates.append("message = %s")
            params.append(message)
        if is_sent is not None:
            updates.append("is_sent = %s")
            params.append(is_sent)

        if not updates:
            return

        params.append(reminder_id)
        query = f"UPDATE reminders SET {', '.join(updates)} WHERE reminder_id = %s"
        self.execute_query(query, tuple(params))

    def delete_reminder(self, reminder_id: int):
        """
        Delete reminder

        Args:
            reminder_id: Reminder ID
        """
        query = "DELETE FROM reminders WHERE reminder_id = %s"
        self.execute_query(query, (reminder_id,))