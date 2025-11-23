from json import load, JSONDecodeError
from os import path, makedirs, dump
from typing import Dict, Any


SUPPORTED_LANGUAGES = ["en", "ru"]
DEFAULT_LANGUAGE = "en"
_STRINGS_CACHE:  Dict[str, Dict[str, str]] = {}
_GUILD_SETTINGS: Dict[int, Dict[str, Any]] = {}


def load_strings() -> None:
    '''
    загружаем локализацию в память
    '''
    global _STRINGS_CACHE
    for lang in SUPPORTED_LANGUAGES:
        path_ = path.join("core", "strings", f"{lang}.json")
        with open(path_, encoding="utf-8") as file:
            _STRINGS_CACHE[lang] = load(file)


def get_text(guild_id: int, key: str, **kwargs) -> str:
    """
    Возвращает локализованный текст для сервера.
    """
    lang = get_guild_language(guild_id)
    text = _STRINGS_CACHE.get(lang, {}).get(key)
    if text is None: text = _STRINGS_CACHE.get(DEFAULT_LANGUAGE, {}).get(key, key)
    return text.format(**kwargs)



def load_guild_settings() -> None:
    """
    Загружает настройки серверов из data/guilds.json.
    """
    global _GUILD_SETTINGS
    path = "data/guilds.json"
    try:
        if path.exists(path):
            with open(path, encoding="utf-8") as f:
                raw = load(f)
                _GUILD_SETTINGS = {int(k): v for k, v in raw.items()}
        else:
            makedirs("data", exist_ok=True)
            _GUILD_SETTINGS = {}
    except (JSONDecodeError, ValueError, OSError) as e:
        print(f"[WARN] Failed to load guild settings: {e}. Using defaults.")
        _GUILD_SETTINGS = {}



def save_guild_settings() -> None:
    """
    Сохраняет настройки в файл.
    """
    with open("data/guilds.json", "w", encoding="utf-8") as f:
        dump(_GUILD_SETTINGS, f, indent=2, ensure_ascii=False)


def get_guild_language(guild_id: int) -> str:
    """
    Возвращает язык сервера.
    """
    return _GUILD_SETTINGS.get(guild_id, {}).get("language", DEFAULT_LANGUAGE)


def set_guild_language(guild_id: int, lang: str) -> bool:
    """
    Устанавливает язык для сервера. Возвращает True, если успешно.
    """
    if lang not in SUPPORTED_LANGUAGES:
        return False
    if guild_id not in _GUILD_SETTINGS:
        _GUILD_SETTINGS[guild_id] = {}
    _GUILD_SETTINGS[guild_id]["language"] = lang
    save_guild_settings()
    return True