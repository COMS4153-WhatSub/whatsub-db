from flask import Flask, request, jsonify
from db_handler import DatabaseHandler
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Database configuration
DB_CONFIG = {
    'host': '34.121.216.146',
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'whatsup')
}

db = DatabaseHandler(DB_CONFIG)


# User Routes
@app.route('/users', methods=['POST'])
def create_user():
    """Create a new user"""
    data = request.json
    try:
        user_id = db.create_user(
            username=data.get('username'),
            email=data.get('email'),
            phone=data.get('phone')
        )
        return jsonify({'user_id': user_id, 'message': 'User created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user by ID"""
    try:
        user = db.get_user(user_id)
        if user:
            return jsonify(user), 200
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/users', methods=['GET'])
def get_all_users():
    """Get all users"""
    try:
        users = db.get_all_users()
        return jsonify(users), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user"""
    data = request.json
    try:
        db.update_user(
            user_id=user_id,
            username=data.get('username'),
            email=data.get('email'),
            phone=data.get('phone')
        )
        return jsonify({'message': 'User updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete user"""
    try:
        db.delete_user(user_id)
        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


# Subscription Routes
@app.route('/subscriptions', methods=['POST'])
def create_subscription():
    """Create a new subscription"""
    data = request.json
    try:
        subscription_id = db.create_subscription(
            user_id=data.get('user_id'),
            name=data.get('name'),
            url=data.get('url'),
            account=data.get('account'),
            billing_date=data.get('billing_date'),
            price=data.get('price')
        )
        return jsonify({'subscription_id': subscription_id, 'message': 'Subscription created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/subscriptions/<int:subscription_id>', methods=['GET'])
def get_subscription(subscription_id):
    """Get subscription by ID"""
    try:
        subscription = db.get_subscription(subscription_id)
        if subscription:
            return jsonify(subscription), 200
        return jsonify({'error': 'Subscription not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/users/<int:user_id>/subscriptions', methods=['GET'])
def get_user_subscriptions(user_id):
    """Get all subscriptions for a user"""
    try:
        subscriptions = db.get_user_subscriptions(user_id)
        return jsonify(subscriptions), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/subscriptions/<int:subscription_id>', methods=['PUT'])
def update_subscription(subscription_id):
    """Update subscription"""
    data = request.json
    try:
        db.update_subscription(
            subscription_id=subscription_id,
            name=data.get('name'),
            url=data.get('url'),
            account=data.get('account'),
            billing_date=data.get('billing_date'),
            price=data.get('price')
        )
        return jsonify({'message': 'Subscription updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/subscriptions/<int:subscription_id>', methods=['DELETE'])
def delete_subscription(subscription_id):
    """Delete subscription"""
    try:
        db.delete_subscription(subscription_id)
        return jsonify({'message': 'Subscription deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


# Reminder Routes
@app.route('/reminders', methods=['POST'])
def create_reminder():
    """Create a new reminder"""
    data = request.json
    try:
        reminder_id = db.create_reminder(
            subscription_id=data.get('subscription_id'),
            reminder_type=data.get('reminder_type'),
            reminder_date=data.get('reminder_date'),
            message=data.get('message')
        )
        return jsonify({'reminder_id': reminder_id, 'message': 'Reminder created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/reminders/<int:reminder_id>', methods=['GET'])
def get_reminder(reminder_id):
    """Get reminder by ID"""
    try:
        reminder = db.get_reminder(reminder_id)
        if reminder:
            return jsonify(reminder), 200
        return jsonify({'error': 'Reminder not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/subscriptions/<int:subscription_id>/reminders', methods=['GET'])
def get_subscription_reminders(subscription_id):
    """Get all reminders for a subscription"""
    try:
        reminders = db.get_subscription_reminders(subscription_id)
        return jsonify(reminders), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/users/<int:user_id>/reminders', methods=['GET'])
def get_user_reminders(user_id):
    """Get all reminders for a user"""
    try:
        reminders = db.get_user_reminders(user_id)
        return jsonify(reminders), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/reminders/<int:reminder_id>', methods=['PUT'])
def update_reminder(reminder_id):
    """Update reminder"""
    data = request.json
    try:
        db.update_reminder(
            reminder_id=reminder_id,
            reminder_type=data.get('reminder_type'),
            reminder_date=data.get('reminder_date'),
            message=data.get('message'),
            is_sent=data.get('is_sent')
        )
        return jsonify({'message': 'Reminder updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/reminders/<int:reminder_id>', methods=['DELETE'])
def delete_reminder(reminder_id):
    """Delete reminder"""
    try:
        db.delete_reminder(reminder_id)
        return jsonify({'message': 'Reminder deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


# Health check
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)