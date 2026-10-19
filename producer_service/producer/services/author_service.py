from producer.models import AuthorIn, AuthorEvent
from producer.kafka_client import get_producer, KAFKA_TOPIC


class AuthorService:
    def post_author(self, author: AuthorIn) -> None:
        event = AuthorEvent(
            event_type="author.created",
            name=author.name,
            email=author.email,
            bio=author.bio,
        )
        get_producer().send(KAFKA_TOPIC, value=event.model_dump())