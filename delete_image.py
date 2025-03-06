from app import app, db, GalleryImage

with app.app_context():
    image = GalleryImage.query.filter_by(filename='wallpaperflare.com_wallpaper_1.jpg').first()
    if image:
        db.session.delete(image)
        db.session.commit()
        print("Bild wurde erfolgreich aus der Datenbank entfernt.")
    else:
        print("Bild wurde nicht in der Datenbank gefunden.") 