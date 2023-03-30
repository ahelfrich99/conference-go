import json
import pika
from pika.exceptions import AMQPConnectionError
import django
import os
import sys
import time
from django.core.mail import send_mail

PRESENTATION_APPROVALS = "presentation_approvals"
PRESENTATION_REJECTIONS = "presentation_rejections"

sys.path.append("")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "presentation_mailer.settings")
django.setup()

def process_approval(ch, method, properties, body):
    print("Received %r" % body)
    body = json.loads(body)

    presenter_name = body["presenter_name"]
    presenter_email = body["presenter_email"]
    title = body["title"]
    message_body = f"{presenter_name}, we're happy to tell you that your presentation {title} has been accepted"

    print(presenter_email)
    send_mail(
        "Your presentation has been accepted",
        message_body,
        "admin@conference.go",
        [presenter_email],
        fail_silently=False,
    )

def process_rejection(ch, method, properties, body):
    print("Received %r" % body)
    body = json.loads(body)

    presenter_name = body["presenter_name"]
    presenter_email = body["presenter_email"]
    title = body["title"]
    message_body = f"{presenter_name}, we're sorry to tell you that your presentation {title} has been rejected"

    send_mail(
        "Your presentation has been rejected",
        message_body,
        "admin@conference.go",
        [presenter_email],
        fail_silently=False,
    )

# def get_channel(queue_name):
#     parameters = pika.ConnectionParameters(host="rabbitmq")
#     connection = pika.BlockingConnection(parameters)
#     channel = connection.channel()
#     channel.queue_declare(queue=queue_name)

#     return channel

while True:
    try:
        parameters = pika.ConnectionParameters(host="rabbitmq")
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue=PRESENTATION_APPROVALS)
        channel.queue_declare(queue=PRESENTATION_REJECTIONS)
        channel.basic_consume(
            queue=PRESENTATION_APPROVALS,
            on_message_callback=process_approval,
            auto_ack=True,
        )

        channel.basic_consume(
            queue=PRESENTATION_REJECTIONS,
            on_message_callback=process_rejection,
            auto_ack=True,
        )
        channel.start_consuming()
    except AMQPConnectionError:
        print("Could not connect to RabbitMQ")
        time.sleep(2.0)

# approved_channel = get_channel(PRESENTATION_APPROVALS)
# approved_channel.basic_consume(
#     queue=PRESENTATION_APPROVALS,
#     on_message_callback=process_approval,
#     auto_ack=True,
# )
# approved_channel.start_consuming()

# rejected_channel = get_channel(PRESENTATION_REJECTIONS)
# rejected_channel.basic_consume(
#     queue=PRESENTATION_REJECTIONS,
#     on_message_callback=process_rejection,
#     auto_ack=True,
# )
# rejected_channel.start_consuming()
