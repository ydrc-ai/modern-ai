from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import asc, desc, func, or_, select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import ActionItem, Note
from ..schemas import (
    ExtractResult,
    NoteCreate,
    NoteRead,
    NoteUpdate,
    Paginated,
)
from ..services.extract import extract_action_items, extract_hashtags

router = APIRouter(prefix="/notes", tags=["notes"])


def _paginate_notes(
    db: Session,
    *,
    page: int,
    page_size: int,
    q: str | None = None,
    sort: str = "created_desc",
) -> Paginated[NoteRead]:
    stmt = select(Note)
    count_stmt = select(func.count()).select_from(Note)

    if q:
        pattern = f"%{q}%"
        filt = or_(Note.title.ilike(pattern), Note.content.ilike(pattern))
        stmt = stmt.where(filt)
        count_stmt = count_stmt.where(filt)

    if sort == "title_asc":
        stmt = stmt.order_by(asc(Note.title), asc(Note.id))
    else:
        # created_desc: higher autoincrement id ≈ newer
        stmt = stmt.order_by(desc(Note.id))

    total = db.execute(count_stmt).scalar_one()
    offset = (page - 1) * page_size
    rows = db.execute(stmt.offset(offset).limit(page_size)).scalars().all()
    return Paginated[NoteRead](
        items=[NoteRead.model_validate(row) for row in rows],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/", response_model=Paginated[NoteRead])
def list_notes(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
) -> Paginated[NoteRead]:
    return _paginate_notes(db, page=page, page_size=page_size)


@router.post("/", response_model=NoteRead, status_code=201)
def create_note(payload: NoteCreate, db: Session = Depends(get_db)) -> NoteRead:
    note = Note(title=payload.title.strip(), content=payload.content.strip())
    db.add(note)
    db.flush()
    db.refresh(note)
    return NoteRead.model_validate(note)


@router.get("/search", response_model=Paginated[NoteRead])
@router.get("/search/", response_model=Paginated[NoteRead])
def search_notes(
    q: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    sort: str = Query("created_desc", pattern="^(created_desc|title_asc)$"),
    db: Session = Depends(get_db),
) -> Paginated[NoteRead]:
    return _paginate_notes(db, page=page, page_size=page_size, q=q, sort=sort)


@router.get("/{note_id}", response_model=NoteRead)
def get_note(note_id: int, db: Session = Depends(get_db)) -> NoteRead:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return NoteRead.model_validate(note)


@router.put("/{note_id}", response_model=NoteRead)
def update_note(note_id: int, payload: NoteUpdate, db: Session = Depends(get_db)) -> NoteRead:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    note.title = payload.title.strip()
    note.content = payload.content.strip()
    db.add(note)
    db.flush()
    db.refresh(note)
    return NoteRead.model_validate(note)


@router.delete("/{note_id}", status_code=204, response_class=Response)
def delete_note(note_id: int, db: Session = Depends(get_db)) -> Response:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.flush()
    return Response(status_code=204)


@router.post("/{note_id}/extract", response_model=ExtractResult)
def extract_from_note(
    note_id: int,
    apply: bool = Query(False),
    db: Session = Depends(get_db),
) -> ExtractResult:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    text = f"{note.title}\n{note.content}"
    hashtags = extract_hashtags(text)
    action_texts = extract_action_items(text)
    created_ids: list[int] = []

    if apply:
        for desc in action_texts:
            item = ActionItem(description=desc, completed=False)
            db.add(item)
            db.flush()
            created_ids.append(item.id)

    return ExtractResult(
        hashtags=hashtags,
        action_items=action_texts,
        applied=apply,
        created_action_item_ids=created_ids,
    )
