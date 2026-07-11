from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import ActionItem
from ..schemas import (
    ActionItemCreate,
    ActionItemRead,
    BulkCompleteRequest,
    Paginated,
)

router = APIRouter(prefix="/action-items", tags=["action_items"])


@router.get("/", response_model=Paginated[ActionItemRead])
def list_items(
    completed: bool | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
) -> Paginated[ActionItemRead]:
    stmt = select(ActionItem)
    count_stmt = select(func.count()).select_from(ActionItem)

    if completed is not None:
        stmt = stmt.where(ActionItem.completed.is_(completed))
        count_stmt = count_stmt.where(ActionItem.completed.is_(completed))

    total = db.execute(count_stmt).scalar_one()
    offset = (page - 1) * page_size
    rows = (
        db.execute(stmt.order_by(ActionItem.id.desc()).offset(offset).limit(page_size))
        .scalars()
        .all()
    )
    return Paginated[ActionItemRead](
        items=[ActionItemRead.model_validate(row) for row in rows],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.post("/", response_model=ActionItemRead, status_code=201)
def create_item(payload: ActionItemCreate, db: Session = Depends(get_db)) -> ActionItemRead:
    item = ActionItem(description=payload.description.strip(), completed=False)
    db.add(item)
    db.flush()
    db.refresh(item)
    return ActionItemRead.model_validate(item)


@router.post("/bulk-complete", response_model=list[ActionItemRead])
def bulk_complete(
    payload: BulkCompleteRequest, db: Session = Depends(get_db)
) -> list[ActionItemRead]:
    items = db.execute(select(ActionItem).where(ActionItem.id.in_(payload.ids))).scalars().all()
    found_ids = {item.id for item in items}
    missing = [i for i in payload.ids if i not in found_ids]
    if missing:
        raise HTTPException(
            status_code=404,
            detail=f"Action items not found: {missing}",
        )

    for item in items:
        item.completed = True
        db.add(item)
    db.flush()
    for item in items:
        db.refresh(item)
    return [ActionItemRead.model_validate(item) for item in items]


@router.put("/{item_id}/complete", response_model=ActionItemRead)
def complete_item(item_id: int, db: Session = Depends(get_db)) -> ActionItemRead:
    item = db.get(ActionItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")
    item.completed = True
    db.add(item)
    db.flush()
    db.refresh(item)
    return ActionItemRead.model_validate(item)
