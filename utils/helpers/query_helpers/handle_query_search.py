import re
import unicodedata
from sqlalchemy import func, or_, cast, String
from sqlalchemy.sql import Select


def clean_search_value(value: str) -> str:
    # remove acentos e caracteres especiais no Python também
    normalized = unicodedata.normalize("NFKD", value)
    ascii_only = normalized.encode("ASCII", "ignore").decode("utf-8")
    cleaned = re.sub(r"[^a-zA-Z0-9]", "", ascii_only)
    return cleaned.strip().lower()


def handle_query_search(query: Select, search_params, search_value):
    search = clean_search_value(search_value)
    conditions = []

    for param in search_params:
        normalized_param = func.lower(
            func.regexp_replace(
                func.unaccent(cast(param, String)),  # <--- remove acentos no SQL
                r'[^a-zA-Z0-9]',
                '',
                'g'
            )
        )
        conditions.append(normalized_param.like(f"%{search}%"))

    return query.where(or_(*conditions))