import json
import logging
from kafka import KafkaConsumer
from kafka.errors import KafkaError
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from home.models import Author

logger = logging.getLogger(__name__)


def process(message):
    data = message.value
    if not data:
        return

    event_type = data.get("event_type")
    logger.info("event_type=%s value=%s", event_type, data)

    if event_type == "author.created":
        name = (data.get("name") or "").strip()
        if not name:
            logger.warning("author.created без name — пропуск: %s", data)
            return

        email = data.get("email") or ""
        bio = data.get("bio") or ""

        author, created = Author.objects.get_or_create(
            name=name,
            email=email,
            defaults={"bio": bio},
        )

        if created:
            logger.info("Author создан: id=%s name=%s", author.id, author.name)
        else:
            logger.info("Author уже есть: id=%s name=%s", author.id, author.name)
    else:
        logger.warning("Неизвестный event_type: %s", event_type)


class Command(BaseCommand):
    help = "Читает события из Kafka и создаёт Author в БД"

    def handle(self, *args, **options):
        self.stdout.write(f"Подключение к Kafka: {settings.KAFKA_BOOTSTRAP_SERVERS}")
        self.stdout.write(f"Топик: {settings.KAFKA_TOPIC}")
        self.stdout.write(f"Группа: {settings.KAFKA_GROUP_ID}")

        try:
            consumer = KafkaConsumer(
                settings.KAFKA_TOPIC,
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                group_id=settings.KAFKA_GROUP_ID,
                auto_offset_reset='latest',
                enable_auto_commit=False,
                value_deserializer=lambda m: json.loads(m.decode('utf-8')) if m else None,
            )
            self.stdout.write(f"Подписка на: {consumer.subscription()}")
            partitions = consumer.partitions_for_topic(settings.KAFKA_TOPIC)
            self.stdout.write(f"Partitions: {partitions}")
        except KafkaError as e:
            self.stderr.write(f"Kafka недоступна: {e}")
            return

        self.stdout.write("Ожидание сообщений...")

        try:
            for message in consumer:
                self.stdout.write(f"Получено: {message.value}")
                try:
                    with transaction.atomic():
                        process(message)
                    consumer.commit()
                except Exception:
                    logger.exception("Ошибка обработки offset=%s", message.offset)
        except KeyboardInterrupt:
            self.stdout.write("Остановка по Ctrl+C")
        finally:
            consumer.close()
