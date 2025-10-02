-- whatsub Database Schema
-- Database for managing user subscriptions and reminders

CREATE DATABASE IF NOT EXISTS whatsub;
USE whatsub;

-- User Table
-- Stores user information
CREATE TABLE IF NOT EXISTS user (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Subscription Table
-- Stores subscription information for users
CREATE TABLE IF NOT EXISTS subscription (
    subscription_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    url VARCHAR(500),
    account VARCHAR(255),
    billing_date DATE,
    price DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_billing_date (billing_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Reminder Table
-- Stores reminders for subscriptions
CREATE TABLE IF NOT EXISTS reminder (
    reminder_id INT AUTO_INCREMENT PRIMARY KEY,
    subscription_id INT NOT NULL,
    reminder_type ENUM('pre_billing', 'after_payment', 'renewal', 'custom') NOT NULL,
    reminder_date DATETIME NOT NULL,
    message TEXT,
    is_sent BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (subscription_id) REFERENCES subscription(subscription_id) ON DELETE CASCADE,
    INDEX idx_subscription_id (subscription_id),
    INDEX idx_reminder_date (reminder_date),
    INDEX idx_is_sent (is_sent)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;