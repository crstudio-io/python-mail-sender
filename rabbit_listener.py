import os
import json
import pika

from sender import send_mail
from logger import get_logger


logger = get_logger("mq_listener")


def callback(ch, method, _, body):
    ch.basic_ack(delivery_tag=method.delivery_tag)
    payload = json.loads(body)
    logger.debug(payload)
    send_mail(payload["subject"], payload["body"], payload["to"])


if __name__ == '__main__':
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host="localhost",
        port=5672,
        credentials=pika.credentials.PlainCredentials(
            username="user",
            password="password",
        ),
    ))

    channel = connection.channel()
    channel.queue_declare(queue="send_mail_queue", durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue="send_mail_queue",
        on_message_callback=callback
    )

    try:
        logger.info("Start waiting for messages")
        channel.start_consuming()
    except KeyboardInterrupt:
        logger.info("Shutdown")
        exit(0)

