from app.core.config import settings

def resolve_ai_provider(is_premium: bool) -> str:
    mode = settings.AI_MODE.lower()
    if mode == "free":
        return "free"
    if mode == "openai":
        return "openai"
    if mode == "auto":
        return "openai" if is_premium else "free"
    return "free"
