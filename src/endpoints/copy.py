from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from ..dependencies import get_current_librarian, get_db
from ..models.copy import Copy
from ..schemas.copy import CopySchema

router = APIRouter(
    prefix="/copy", tags=["copy"], responses={401: {"user": "Not authorized"}}
)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_copies(db: Session = Depends(get_db)):
    """
    Endpoint to get all copies for copy.
    """
    return db.query(Copy).all()


@router.get("/all/{book_id}", status_code=status.HTTP_200_OK)
async def get_copies_by_book_id(book_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to get all copies by book id
    """
    copies = db.query(Copy).filter(Copy.book_id == book_id).all()
    if copies:
        return copies
    if not copies:
        raise http_exception()
    return copies


@router.get("/{copy_id}", status_code=status.HTTP_200_OK)
async def get_copy_by_id(copy_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to get copy by id
    """
    copy = db.query(Copy).filter(Copy.id == copy_id).first()
    if copy:
        return copy
    if not copy:
        raise http_exception()
    return copy


@router.post("/", status_code=status.HTTP_201_CREATED)
async def copy_create(
    copy: CopySchema,
    db: Session = Depends(get_db),
    librarian: dict = Depends(get_current_librarian),  # noqa
) -> dict:
    """
    Endpoint to create a copy
    """

    copy_model = Copy()
    copy_model.book_id = copy.book_id
    copy_model.language_id = copy.language_id
    copy_model.status = copy.status

    db.add(copy_model)
    db.commit()
    return succesful_response()


@router.put("/{copy_id}", status_code=status.HTTP_204_NO_CONTENT)
async def copy_update(
    copy_id: int,
    copy: CopySchema,
    db: Session = Depends(get_db),
    librarian: dict = Depends(get_current_librarian),  # noqa
):
    """
    Endpoint to Update an existing copy by ID.
    """

    copy_model = db.query(Copy).filter(Copy.id == copy_id).first()

    if copy_model is None:
        raise http_exception()

    copy_model.book_id = copy.book_id
    copy_model.language_id = copy.language_id
    copy_model.status = copy.status

    db.add(copy_model)
    db.commit()

    return succesful_response()


@router.delete("/{copy_id}", status_code=status.HTTP_200_OK)
async def copy_delete(
    copy_id: int,
    db: Session = Depends(get_db),
    librarian: dict = Depends(get_current_librarian),  # noqa
) -> dict:
    """
    Endpoint to delete a copy by ID.
    """

    copy_model = db.query(Copy).filter(Copy.id == copy_id).first()

    if copy_model is None:
        raise http_exception()

    db.query(Copy).filter(Copy.id == copy_id).delete()

    db.commit()

    return succesful_response()


def http_exception():
    return HTTPException(status_code=404, detail="Copy not found")


def succesful_response():
    return {"status": 201, "transaction": "succesful_response"}
