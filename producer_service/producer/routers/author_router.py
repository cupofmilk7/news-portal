from fastapi import APIRouter, Depends, status

from producer.services.author_service import AuthorService
from producer.models import AuthorIn

router = APIRouter(prefix="/authors", tags=["news"])


def get_author_service() -> AuthorService:
    return AuthorService()


@router.post("/", status_code=status.HTTP_202_ACCEPTED)
def post_authors(author: AuthorIn,
                 service: AuthorService = Depends(get_author_service)):
    service.post_author(author)

