import sqlite3
import os

# Verbindung zur Datenbank herstellen
conn = sqlite3.connect('restaurant.db')
cursor = conn.cursor()

# Alle Bildpfade abrufen
cursor.execute('SELECT id, image_path FROM gallery_image')
images = cursor.fetchall()

# Zähle, wie viele Einträge aktualisiert wurden
updated_count = 0

for image_id, image_path in images:
    if '\\' in image_path:
        # Ersetze Backslashes durch reguläre Slashes
        new_path = image_path.replace('\\', '/')
        cursor.execute('UPDATE gallery_image SET image_path = ? WHERE id = ?', (new_path, image_id))
        print(f"Pfad aktualisiert: {image_path} -> {new_path}")
        updated_count += 1

# Änderungen speichern
conn.commit()

# Überprüfe, ob die Änderungen erfolgreich waren
cursor.execute('SELECT id, image_path FROM gallery_image')
images_after = cursor.fetchall()

print(f"\nAktualisierte Bildpfade: {updated_count}")
print("\nAktualisierte Bildpfade in der Datenbank:")
for image_id, image_path in images_after:
    print(f"ID: {image_id}, Pfad: {image_path}")

conn.close()
print("\nSkript erfolgreich abgeschlossen.") 