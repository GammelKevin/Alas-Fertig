from clean_statistics import reset_all_statistics

print("Statistiken werden zurückgesetzt...")
if reset_all_statistics():
    print("Statistiken wurden erfolgreich auf 0 zurückgesetzt!")
else:
    print("Fehler beim Zurücksetzen der Statistiken.") 