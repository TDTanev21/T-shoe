from datetime import datetime
from models.order import product_notifications, notification_id_counter


def add_product_notification(product_name, category, price):
    global notification_id_counter

    notification_id_counter += 1
    notification = {
        'id': notification_id_counter,
        'type': 'new_product',
        'product_name': product_name,
        'category': category,
        'price': price,
        'timestamp': datetime.now(),
        'read_by': set()
    }

    product_notifications.append(notification)

    if len(product_notifications) > 20:
        product_notifications = product_notifications[-20:]


def get_unread_notifications(username):
    if not username:
        return []

    unread = []
    for notification in reversed(product_notifications):
        if username not in notification['read_by']:
            unread.append(notification)

    return unread


def mark_notification_as_read(notification_id, username):
    if not username:
        return

    for notification in product_notifications:
        if notification['id'] == notification_id:
            notification['read_by'].add(username)
            break


def mark_all_notifications_as_read(username):
    if not username:
        return

    for notification in product_notifications:
        notification['read_by'].add(username)