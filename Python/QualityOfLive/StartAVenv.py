import subprocess
import os
import sys
import shutil

def create_venv():
    """Erstellt eine virtuelle Python-Umgebung mit einem Namen."""
    print("\n" + "="*50)
    print(" Python Venv Manager")
    print("="*50)
    
    while True:
        print("\nOptionen:")
        print("1. Neue venv erstellen")
        print("2. Vorhandene venvs anzeigen")
        print("3. Venv löschen")
        print("4. Beenden")
        
        wahl = input("\nWähle eine Option (1-4): ").strip()
        
        if wahl == '1':
            neue_venv_erstellen()
        elif wahl == '2':
            venvs_anzeigen()
        elif wahl == '3':
            venv_loeschen()
        elif wahl == '4':
            print("\nAuf Wiedersehen!")
            break
        else:
            print("Ungültige Eingabe! Bitte 1-4 wählen.")

def neue_venv_erstellen():
    """Erstellt eine neue virtuelle Umgebung."""
    print("\n--- Neue venv erstellen ---")
    
    name = input("\nName der venv (z.B. 'mein_projekt'): ").strip()
    
    if not name:
        print("FEHLER: Name darf nicht leer sein!")
        input("\nEnter drücken zum Fortfahren...")
        return
    
    # Prüfe auf ungültige Zeichen
    if not name.replace('_', '').replace('-', '').isalnum():
        print("FEHLER: Nur Buchstaben, Zahlen, _ und - erlaubt!")
        input("\nEnter drücken zum Fortfahren...")
        return
    
    venv_pfad = os.path.join(os.getcwd(), name)
    
    # Prüfe ob Verzeichnis existiert
    if os.path.exists(venv_pfad):
        print(f"\nWARNUNG: '{name}' existiert bereits!")
        überschreiben = input("Überschreiben? (j/n): ").strip().lower()
        
        if überschreiben == 'j':
            try:
                shutil.rmtree(venv_pfad)
                print("Altes Verzeichnis gelöscht.")
            except OSError as e:
                print(f"FEHLER beim Löschen: {e}")
                input("\nEnter drücken zum Fortfahren...")
                return
        else:
            print("Abgebrochen.")
            input("\nEnter drücken zum Fortfahren...")
            return
    
    # Erstelle venv
    print(f"\nErstelle venv '{name}'...")
    try:
        subprocess.run([sys.executable, "-m", "venv", name], check=True)
        print(f"ERFOLG: Venv '{name}' erfolgreich erstellt!")
        
        # Erstelle Aktivierungs-Batch-Datei
        bat_datei = f"activate_{name}.bat"
        bat_inhalt = f"""@echo off
echo Aktiviere venv '{name}'...
call {name}\\Scripts\\activate.bat
echo.
echo Venv '{name}' ist aktiv!
echo Zum Beenden: deactivate eingeben
echo.
cmd /k
"""
        with open(bat_datei, "w") as f:
            f.write(bat_inhalt)
        
        print(f"ERFOLG: Batch-Datei '{bat_datei}' erstellt!")
        print(f"\nHINWEIS: Doppelklick auf '{bat_datei}' zum Aktivieren")
        
    except subprocess.CalledProcessError as e:
        print(f"FEHLER beim Erstellen: {e}")
    
    input("\nEnter drücken zum Fortfahren...")

def venvs_anzeigen():
    """Zeigt alle gefundenen venvs im aktuellen Verzeichnis."""
    print("\n--- Vorhandene venvs ---")
    
    gefunden = False
    for item in os.listdir('.'):
        if os.path.isdir(item):
            python_exe = os.path.join(item, "Scripts", "python.exe")
            if os.path.exists(python_exe):
                print(f"  - {item}")
                gefunden = True
    
    if not gefunden:
        print("  Keine venvs gefunden.")
    
    input("\nEnter drücken zum Fortfahren...")

def venv_loeschen():
    """Löscht eine virtuelle Umgebung."""
    print("\n--- Venv löschen ---")
    
    name = input("\nName der zu löschenden venv: ").strip()
    
    if not name:
        print("FEHLER: Name darf nicht leer sein!")
        input("\nEnter drücken zum Fortfahren...")
        return
    
    venv_pfad = os.path.join(os.getcwd(), name)
    
    if not os.path.exists(venv_pfad):
        print(f"FEHLER: '{name}' existiert nicht!")
        input("\nEnter drücken zum Fortfahren...")
        return
    
    print(f"\nWARNUNG: '{name}' wird unwiderruflich gelöscht!")
    bestätigung = input("Zum Bestätigen 'LÖSCHEN' eingeben: ").strip()
    
    if bestätigung == "LÖSCHEN":
        try:
            shutil.rmtree(venv_pfad)
            print(f"ERFOLG: '{name}' erfolgreich gelöscht!")
            
            # Lösche auch die Batch-Datei falls vorhanden
            bat_datei = f"activate_{name}.bat"
            if os.path.exists(bat_datei):
                os.remove(bat_datei)
                print(f"ERFOLG: '{bat_datei}' gelöscht!")
                
        except OSError as e:
            print(f"FEHLER beim Löschen: {e}")
    else:
        print("Abgebrochen.")
    
    input("\nEnter drücken zum Fortfahren...")

if __name__ == "__main__":
    create_venv()
