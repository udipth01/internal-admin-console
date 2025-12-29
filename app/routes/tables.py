from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from app.db import supabase
from app.auth import get_current_user
from io import StringIO
import csv

router = APIRouter()

# -------------------------
# Helpers
# -------------------------

def mask_value(value, mask_type):
    if value is None:
        return None
    if mask_type == "full":
        return "****"
    if mask_type == "partial":
        return str(value)[:2] + "****"
    return value


def get_mask_map(table_name: str):
    masks = supabase.table("admin_column_masks") \
        .select("*") \
        .eq("table_name", table_name) \
        .execute().data or []
    return {m["column_name"]: m["mask_type"] for m in masks}


# -------------------------
# List allowed tables
# -------------------------

@router.get("/tables")
def list_tables(user=Depends(get_current_user)):
    perms = supabase.table("admin_permissions") \
        .select("table_name") \
        .eq("user_id", user["user_id"]) \
        .eq("can_read", True) \
        .execute()

    return [p["table_name"] for p in perms.data]


# -------------------------
# Fetch table with pagination + search + masking
# -------------------------

@router.get("/table/{table_name}")
def fetch_table(
    table_name: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(25, le=100),
    q: str | None = None,
    user=Depends(get_current_user)
):
    # permission check
    perm = supabase.table("admin_permissions") \
        .select("*") \
        .eq("user_id", user["user_id"]) \
        .eq("table_name", table_name) \
        .eq("can_read", True) \
        .execute()

    if not perm.data:
        raise HTTPException(403, "Access denied")

    start = (page - 1) * page_size
    end = start + page_size - 1

    query = supabase.table(table_name).select("*", count="exact")

    # simple safe search (id / name fallback)
    if q:
        query = query.ilike("id", f"%{q}%")

    res = query.range(start, end).execute()

    mask_map = get_mask_map(table_name)

    for row in res.data:
        for col, mask in mask_map.items():
            if col in row:
                row[col] = mask_value(row[col], mask)

    return {
        "data": res.data,
        "page": page,
        "page_size": page_size,
        "total": res.count
    }


# -------------------------
# CSV Export (permission based)
# -------------------------

@router.get("/table/{table_name}/csv")
def download_csv(table_name: str, user=Depends(get_current_user)):
    perm = supabase.table("admin_permissions") \
        .select("*") \
        .eq("user_id", user["user_id"]) \
        .eq("table_name", table_name) \
        .eq("can_export", True) \
        .execute()

    if not perm.data:
        raise HTTPException(403, "CSV export not allowed")

    rows = supabase.table(table_name).select("*").execute().data or []
    mask_map = get_mask_map(table_name)

    def generate():
        buf = StringIO()
        writer = csv.DictWriter(buf, fieldnames=rows[0].keys())
        writer.writeheader()
        for r in rows:
            for col, mask in mask_map.items():
                r[col] = mask_value(r.get(col), mask)
            writer.writerow(r)
        yield buf.getvalue()

    return StreamingResponse(
        generate(),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={table_name}.csv"}
    )


# -------------------------
# Admin: manage permissions
# -------------------------

@router.post("/admin/permission")
def set_permission(
    user_id: str,
    table_name: str,
    can_read: bool = True,
    can_export: bool = False,
    user=Depends(get_current_user)
):
    if user.get("role") != "admin":
        raise HTTPException(403, "Admin only")

    supabase.table("admin_permissions").upsert({
        "user_id": user_id,
        "table_name": table_name,
        "can_read": can_read,
        "can_export": can_export
    }).execute()

    return {"status": "ok"}
