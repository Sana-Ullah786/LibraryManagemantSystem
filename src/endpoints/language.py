from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.endpoints.auth import get_current_librarian, get_user_exception
from src.models import all_models
from src.models.database import get_db
from src.schemas import language_schema

router = APIRouter(
    prefix="/language",
    tags=["language"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=None, status_code=status.HTTP_201_CREATED)
async def create_language(
    language: language_schema.LanguageSchema,
    user: dict = Depends(get_current_librarian),
    db: Session = Depends(get_db),
) -> all_models.Language:
    """
    This function will be used to create a new language.
    Parameters:
        language: The language data.
        db: The database session.
    Returns:
        language: The created language.
    """
    try:
        new_language = all_models.Language()
        new_language.language = language.language
        db.add(new_language)
        db.commit()
        return new_language
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=None, status_code=status.HTTP_200_OK)
async def get_all_languages(db: Session = Depends(get_db)) -> List[all_models.Language]:
    """
    This function will be used to get all the languages.
    Parameters:
        db: The database session.
    Returns:
        languages: The list of all languages.
    """
    try:
        languages = db.query(all_models.Language).all()
        return languages
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{language_id}", response_model=None, status_code=status.HTTP_200_OK)
async def get_language_by_id(
    language_id: int,
    user: dict = Depends(get_current_librarian),
    db: Session = Depends(get_db),
) -> all_models.Language:
    """
    This function will be used to get a language by id.
    Parameters:
        language_id: The id of the language.
        user: The user data. (current libarian)
        db: The database session.
    Returns:
        language: The language.
    """
    language = (
        db.query(all_models.Language)
        .filter(all_models.Language.id == language_id)
        .first()
    )
    if not language:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Language not found"
        )
    return language


@router.put("/{language_id}", response_model=None, status_code=status.HTTP_200_OK)
async def update_language_by_id(
    language_id: int,
    language: language_schema.LanguageSchema,
    user: dict = Depends(get_current_librarian),
    db: Session = Depends(get_db),
) -> all_models.Language:
    """
    This function will be used to update a language by id.
    Parameters:
        language_id: The id of the language.
        language: The language data.
        user: The user data. (current librarian)
        db: The database session.
    Returns:
        language: The updated language.
    """
    found_language = (
        db.query(all_models.Language)
        .filter(all_models.Language.id == language_id)
        .first()
    )
    if not found_language:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Language not found"
        )
    try:
        found_language.language = language.language
        db.commit()
        updated_language = (
            db.query(all_models.Language)
            .filter(all_models.Language.id == language_id)
            .first()
        )
        return updated_language
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{language_id}", response_model=None, status_code=status.HTTP_200_OK)
async def delete_language_by_id(
    language_id: int,
    user: dict = Depends(get_current_librarian),
    db: Session = Depends(get_db),
) -> all_models.Language:
    """
    This function will be used to delete a language by id.
    Parameters:
        language_id: The id of the language.
        user: The user data. (current librarian)
        db: The database session.
    Returns:
        language: The deleted language.
    """
    found_language = (
        db.query(all_models.Language)
        .filter(all_models.Language.id == language_id)
        .first()
    )
    if not found_language:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Language not found"
        )
    try:
        db.delete(found_language)
        db.commit()
        return found_language
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
