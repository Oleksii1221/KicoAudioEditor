from __future__ import annotations

LANGUAGES = {
    "uk": "Українська",
    "en": "English",
    "ja": "日本語",
    "it": "Italiano",
    "pl": "Polski",
}

STRINGS: dict[str, dict[str, str]] = {
    "uk": {
        "open_files": "Відкрити файли",
        "open_folder": "Відкрити папку",
        "save": "Зберегти",
        "save_all": "Зберегти вибрані",
        "settings": "Налаштування",
        "title": "Назва",
        "artist": "Виконавець",
        "album": "Альбом",
        "album_artist": "Артист альбому",
        "genre": "Жанр",
        "year": "Рік",
        "track": "Трек",
        "disc": "Диск",
        "composer": "Композитор",
        "comment": "Коментар",
        "lyrics": "Текст",
        "bpm": "BPM",
        "change_cover": "Змінити обкладинку",
        "export_cover": "Експорт обкладинки",
        "remove_cover": "Прибрати обкладинку",
        "import_json": "Імпорт JSON",
        "export_json": "Експорт JSON",
        "search": "Пошук",
        "batch": "Пакетно",
        "theme": "Тема",
        "language": "Мова",
    },
    "en": {
        "open_files": "Open files",
        "open_folder": "Open folder",
        "save": "Save",
        "save_all": "Save selected",
        "settings": "Settings",
        "title": "Title",
        "artist": "Artist",
        "album": "Album",
        "album_artist": "Album artist",
        "genre": "Genre",
        "year": "Year",
        "track": "Track",
        "disc": "Disc",
        "composer": "Composer",
        "comment": "Comment",
        "lyrics": "Lyrics",
        "bpm": "BPM",
        "change_cover": "Change cover",
        "export_cover": "Export cover",
        "remove_cover": "Remove cover",
        "import_json": "Import JSON",
        "export_json": "Export JSON",
        "search": "Search",
        "batch": "Batch",
        "theme": "Theme",
        "language": "Language",
    },
}

for code in ["ja", "it", "pl"]:
    STRINGS[code] = STRINGS["en"] | {"language": LANGUAGES[code]}


def t(language: str, key: str) -> str:
    return STRINGS.get(language, STRINGS["uk"]).get(key, STRINGS["en"].get(key, key))
