import json
import os
import django
from confluent_kafka import Consumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.apps import apps

Notification = apps.get_model('notifications', 'Notification')


def on_delivery(err, msg):
    if err:
        print(f"Delivery failed for message {msg}: {err}")
    else:
        print(f"Message {msg} delivered to {msg.topic()}")

consumer1 = Consumer({
    'bootstrap.servers': os.environ.get('KAFKA_BOOTSTRAP_SERVER'),
    'security.protocol': os.environ.get('KAFKA_SECURITY_PROTOCOL'),
    'sasl.username': os.environ.get('KAFKA_USERNAME'),
    'sasl.password': os.environ.get('KAFKA_PASSWORD'),
    'sasl.mechanism': 'PLAIN',
    'group.id': os.environ.get('KAFKA_GROUP'),
    'auto.offset.reset': 'earliest'
})
consumer1.subscribe([os.environ.get('KAFKA_TOPIC')])

while True:
    msg1 = consumer1.poll(1.0)

    if msg1 is None:
        continue
    if msg1.error():
        print(f"Error: {msg1.error()}")
        continue

    topic1 = msg1.topic()
    value1 = msg1.value()
    print(f"Message: {msg1.value()}")

    if topic1 == 'notifications':
        if msg1.key() == b'course_sold':
            notification_data = json.loads(value1)
            try:
                notif = Notification.objects.create(
                    from_user=notification_data['from_user'],
                    to_user=notification_data['to_user'],
                    notification_type=notification_data['notification_type'],
                    text_preview=notification_data['text_preview'],
                    url=notification_data['url'],
                    icon=notification_data['icon'],
                    is_seen=notification_data['is_seen'],
                    course=notification_data['course'],
                )
            except:
                continue
        if msg1.key() == b'friend_request':
            notification_data = json.loads(value1)
            try:
                notif = Notification.objects.create(
                    from_user=notification_data['from_user'],
                    to_user=notification_data['to_user'],
                    notification_type=notification_data['notification_type'],
                    text_preview=notification_data['text_preview'],
                    url=notification_data['url'],
                    icon=notification_data['icon'],
                    is_seen=notification_data['is_seen'],
                )
            except:
                continue
        if msg1.key() == b'cancel_friend_request':
            notification_data = json.loads(value1)
            notif = Notification.objects.get(
                id=notification_data['id'],
            )
            notif.delete()

consumer1.close()
        # Send delivery report to Kafka to confirm that message has been delivered successfully
        # producer.poll(0)
        # producer.flush(on_delivery=on_delivery)