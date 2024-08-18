import os
import json
import pika

from logger import get_logger
from sender import send_mail

config = None
config_file = os.getenv("RUNNER_CONF_FILE")
if config_file and os.path.isfile(config_file):
    with open(config_file) as conf_json:
        config = json.load(conf_json)

logger = get_logger("mq_listener")


def callback(ch, method, _, body):
    ch.basic_ack(delivery_tag=method.delivery_tag)
    payload = json.loads(body)
    logger.debug(payload)
    send_mail(payload["subject"], payload["body"], payload["to"])


if __name__ == '__main__':
    rabbit_host = os.getenv("RABBIT_HOST", "localhost")
    rabbit_port = os.getenv("RABBIT_PORT", 5672)
    rabbit_user = os.getenv("RABBIT_PORT", "user")
    rabbit_password = os.getenv("RABBIT_PASSWORD", "password")
    rabbit_queue = os.getenv("RABBIT_QUEUE_NAME", "send_mail_queue")
    if config and "rabbitmq" in config.keys():
        logger.info("using config from file: " + config_file)
        rabbit_config = config["rabbitmq"]
        rabbit_host = rabbit_config.get("host", rabbit_host)
        rabbit_port = rabbit_config.get("port", rabbit_port)
        rabbit_user = rabbit_config.get("user", rabbit_user)
        rabbit_password = rabbit_config.get("password", rabbit_password)
        rabbit_queue = rabbit_config.get("queue_name", rabbit_queue)

    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=rabbit_host,
        port=rabbit_port,
        credentials=pika.credentials.PlainCredentials(
            username=rabbit_user,
            password=rabbit_password,
        ),
    ))

    channel = connection.channel()
    channel.queue_declare(queue=rabbit_queue, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue=rabbit_queue,
        on_message_callback=callback
    )

    try:
        logger.info("Start waiting for messages")
        channel.start_consuming()
    except KeyboardInterrupt:
        logger.info("Shutdown")
        exit(0)

