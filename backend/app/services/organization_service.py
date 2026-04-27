from app.repositories.organization_repository import fetch_all_organizations


def get_all_organizations() -> list[dict]:
    return fetch_all_organizations()