import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from ..dependencies import get_current_librarian, get_db
from ..models.copy import Copy
from ..schemas.copy import CopySchema

router = APIRouter(
    prefix="/copy", tags=["copy"], responses={401: {"user": "Not authorized"}}
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=None)
async def get_copies(db: Session = Depends(get_db)) -> List[Copy]:
    """
    Endpoint to get all copies for copy.
    """
    logging.info("All Copy Requested")

    return db.query(Copy).all()


@router.get("/book/{book_id}", status_code=status.HTTP_200_OK, response_model=None)
async def get_copies_by_book_id(
    book_id: int, db: Session = Depends(get_db)
) -> List[Copy]:
    """
    Endpoint to get all copies by book id
    """
    copies = db.query(Copy).filter(Copy.book_id == book_id).all()
    if copies:
        logging.info(f"Copies with book id : {book_id}")
        return copies
    logging.info(f"No Copy with book id : {book_id}")
    return copies


@router.get("/{copy_id}", status_code=status.HTTP_200_OK, response_model=None)
async def get_copy_by_id(copy_id: int, db: Session = Depends(get_db)) -> Copy:
    """
    Endpoint to get copy by id
    """
    copy = db.query(Copy).filter(Copy.id == copy_id).first()
    if copy:
        logging.info(f"Copy with copy id : {copy_id}")
        return copy
    if not copy:
        logging.info(f"No Copy with copy id : {copy_id}")
        raise http_exception()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=None)
async def copy_create(
    copy: CopySchema,
    db: Session = Depends(get_db),
    librarian: dict = Depends(get_current_librarian),  # noqa
) -> dict:
    """
    Endpoint to create a copy
    """
    logging.info(f"Copy Create Request by Librarian {librarian['id']}")

    copy_model = Copy()
    copy_model.book_id = copy.book_id
    copy_model.language_id = copy.language_id
    copy_model.status = copy.status

    db.add(copy_model)
    db.commit()
    logging.info(
        f"Copy with id : {copy_model.id} Created by Librarian {librarian['id']}"
    )
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
    logging.info(
        f"Book Update with id :{copy_id} Request by Librarian {librarian['id']}"
    )

    copy_model = db.query(Copy).filter(Copy.id == copy_id).first()

    if copy_model is None:
        logging.info(f"Book Update with id :{copy_id} , not found")
        raise http_exception()

    copy_model.book_id = copy.book_id
    copy_model.language_id = copy.language_id
    copy_model.status = copy.status

    db.add(copy_model)
    db.commit()
    logging.info(
        f"Book Updated with id :{copy_id} Request by Librarian {librarian['id']}"
    )
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
    logging.info(
        f"Book Delete with id :{copy_id} Request by Librarian {librarian['id']}"
    )

    copy_model = db.query(Copy).filter(Copy.id == copy_id).first()

    if copy_model is None:
        raise http_exception()

    db.query(Copy).filter(Copy.id == copy_id).delete()

    db.commit()
    logging.info(
        f"Book Updated with id :{copy_id} Request by Librarian {librarian['id']}"
    )

    return succesful_response()


def http_exception() -> dict:
    return HTTPException(status_code=404, detail="Copy not found")


def succesful_response() -> dict:
    return {"status": 201, "transaction": "succesful_response"}
