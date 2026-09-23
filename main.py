import os
import re
from mutagen.mp3 import MP3

work_dir = "./input"

def rename_mp3(file_path):
    audio = MP3(file_path)
    tags = audio.tags or {}


    title = tags.get('TIT2', tags.get('title', [None]))[0]
    artist: str = tags.get('TPE1', tags.get('artist', [None]))[0]
    if title or artist:
        safe_title = re.sub(r'[\\/*?:"<>|]', "", str(title)) if title else "Неизвестный трек"
        if artist:
            artist = artist.replace("/",", ", -1)
            safe_artist = re.sub(r'[\\/*?:"<>|]', "", str(artist))
        else:
            safe_artist = "Неизвестный исполнитель"
        
        new_name = f"{safe_title} - {safe_artist}.mp3"
        new_path = os.path.join(os.path.dirname(file_path), new_name)

        os.rename(file_path, new_path)
        print(f"Переименовано: {new_name}")
    else:
        print("Имя не изменилось. Нет данных.")

if __name__=="__main__":
    if not os.path.exists(work_dir):
        os.makedirs(work_dir)
        print(f"Папка {work_dir} создана. Положите MP3-файлы.")
    else:
        files = os.listdir(work_dir)
        mp3_files = [f for f in files if f.lower().endswith('.mp3')]
        
        if not mp3_files:
            print(f"В {work_dir} нет MP3-файлов.")
        else:
            print(f"Найдено MP3-файлов: {len(mp3_files)}\n")
            
            success, errors = 0, 0
            for filename in mp3_files:
                file_path = os.path.join(work_dir, filename)
                try:
                    rename_mp3(file_path)
                    success += 1
                except Exception as e:
                    print(f"Ошибка с {filename}: {e}")
                    errors += 1
            
            print(f"\nГотово. Успешно: {success}, ошибок: {errors}")