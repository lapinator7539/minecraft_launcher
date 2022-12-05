import os
import subprocess
from tkinter import *
from functools import partial
import tkinter.font as font
from PIL import Image, ImageTk
import webbrowser
import minecraft_launcher_lib
from dotenv import load_dotenv
import sys
import shutil
import urllib.request
import ast


def main():
    def update_forge(arg):
        forge_update_text = PhotoImage(file="assets/forge_update.png")
        image5 = cancan.create_image(400, 200, image=forge_update_text)
        window.update_idletasks()
        # télécharge la version de forge
        version = arg
        print("The forge version is not downloaded")
        print(f"Forge download in progress...({version})")
        print("This may take several minutes.")
        minecraft_launcher_lib.forge.install_forge_version(version, minecraft_directory)
        version = minecraft_launcher_lib.forge.find_forge_version(vanilla_version)
        full_name_forge_version = version.replace("-", "-forge-")
        cancan.delete(image5)
        print("Update completed")

    def widget_place():
        cancan.delete(image2)
        logout_button.place_forget()
        code_url.place(x=210, y=270)
        link.place(x=288, y=100)
        bouton.place(x=300, y=200)

    def logout():
        print("try to disconnect...")
        with open("config", "w") as obj:
            obj.write("REMEMBER=0\n")
            obj.close()
        widget_place()
        reload_status(0)

    def update_mods():

        # créé le repertoire mods s'il n'y est pas
        if not os.path.exists(f'{minecraft_directory}\\mods'):
            os.makedirs(f'{minecraft_directory}\\mods')

        # liste tous les fichiers dans le dossier mods
        fichiers = [f for f in os.listdir(f"{minecraft_directory}\\mods")]
        for file in fichiers:
            # vérifie si un des fichiers n'est pas un autre mod
            if file != mods_list[1] and file != mods_list[0]:
                try:
                    # créer un repertoire pour les mods déplacés
                    os.makedirs(f"{minecraft_directory}/moved_mods")
                    print("Folder created")
                except FileExistsError:
                    # évite un message d'erreur dans la console
                    pass
                finally:
                    # Déplace le mod concerné dans le dossier moved_mods pour pas que le mod soit exécuté
                    shutil.move(f"{minecraft_directory}/mods/{file}",
                                f"{minecraft_directory}/moved_mods/{file}")
                    print(f"Moved file : {file} in the folder : /moved_mods")

        # check if mods are already downloaded
        if mods_list == fichiers:
            print("already downloaded mods")
        else:
            print("downloading mods...")
            # obfuscate
            url1 = 'https://4d2a096c-ed43-4627-a525-cdcf1eacad66.usrfiles.com/archives' \
                   '/4d2a09_d71ca86687604f7fb2f4bb2416db4082.jar '
            urllib.request.urlretrieve(url1, f'{minecraft_directory}/mods/{mods_list[1]}')

            # cgm
            url2 = 'https://4d2a096c-ed43-4627-a525-cdcf1eacad66.usrfiles.com/archives' \
                   '/4d2a09_f5f614ba2307460b813c53265dc89a38.jar '
            urllib.request.urlretrieve(url2, f'{minecraft_directory}/mods/{mods_list[0]}')

    def launch():
        update_mods()
        remember = int(os.getenv("REMEMBER"))
        if remember == 0:
            cancan.moveto(image3, 0, -30)
            cancan.moveto(image4, 0, -30)
            if code_url.get() == "":
                print('code empty')
                cancan.moveto(image3, 235, 250)
            else:
                print(f"Verification code : {code_url.get()}")
                if not minecraft_launcher_lib.microsoft_account.url_contains_auth_code(code_url.get()):
                    cancan.moveto(image4, 315, 250)
                    print("The url isn't valid")
                else:
                    window.withdraw()

                    # Get the code from the url
                    auth_code = minecraft_launcher_lib.microsoft_account.get_auth_code_from_url(code_url.get())

                    # Get the login data
                    login_data = minecraft_launcher_lib.microsoft_account.complete_login(client_id, secret,
                                                                                         redirect_url, auth_code)

                    options = {"username": login_data["name"],
                               "uuid": login_data["id"],
                               "token": login_data["access_token"],
                               "executablePath": 'javaw',
                               "launcherName": 'KipikCube Launcher'

                               }

                    command = minecraft_launcher_lib.command.get_minecraft_command(full_name_forge_version,
                                                                                   minecraft_directory,
                                                                                   options)
                    if statu == 1:
                        with open("config", "w") as obj:
                            obj.write("REMEMBER=1\n")
                            obj.write(f"COMMAND={command}")
                            obj.close()

                    print(f"auth_code : {auth_code}")
                    print(f"login_data : {login_data}")
                    print(f"options : {options}")
                    print(f'command  : {command}')

                    subprocess.call(command)
                    sys.exit(0)

        elif remember == 1:
            window.withdraw()
            command = os.getenv("COMMAND")
            command.split(",")
            command = ast.literal_eval(command)
            subprocess.call(command)
            sys.exit(0)

    load_dotenv(dotenv_path="config")
    mods_list = ['cgm-1.1.0-1.16.5.jar', 'obfuscate-0.6.2-1.16.3.jar']
    vanilla_version = "1.16.5"
    launcher_title = "KipikCube Launcher"
    dimension = "720x480"

    # liens réseaux
    lien_twitch = r""
    lien_youtube = r""
    lien_site = r""
    lien_discord = r""

    # client id ; secret ; uri de redirection de l'app azure
    client_id = ""
    secret = ""
    redirect_url = ""

    # paramètre de la fenêtre principal
    window = Tk()
    window.title(launcher_title)
    window.iconphoto(True, PhotoImage(file="assets/KIPIKCUBE1.png"))
    window.geometry(dimension)
    window.resizable(width=False, height=False)

    window.update_idletasks()

    # image de fond du launcher
    fond = PhotoImage(file="assets/fond2.png")
    cancan = Canvas(window, height=900, width=900, )
    cancan.create_image(0, 0, anchor=NW, image=fond)
    cancan.place(x=-20, y=0)

    # texte démarrage du launcher
    text_starting = PhotoImage(file="assets/launcher_start.png")
    image1 = cancan.create_image(380, 80, image=text_starting)

    window.update_idletasks()

    minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()

    def etat():
        reload_status(v.get())

    # checkbutton (remember me)
    v = IntVar()
    bouton = Checkbutton(window, command=etat, variable=v, text="Remember me")

    # création de la zone pour entrer l'URL de connexion
    code_url = Entry(window, width=50)

    # création des polices d'écriture
    f1 = font.Font(family='Impact', size=25, weight="bold")
    f2 = font.Font(family='Impact', size=10)
    # création du bouton PLAY
    launch_button = Button(window, text="PLAY", width=10, height=1, bg='green', command=launch, borderwidth=1)
    # application de la police d'écriture au bouton
    launch_button['font'] = f1

    def on_click(arg):
        webbrowser.open_new(arg)
        print("redirect to discord...")

    # définit les 4 icons en haut à gauche pour aller sur discord, site, etc.
    image_discord = Image.open("assets/discord.png")
    photo_discord = ImageTk.PhotoImage(image_discord)
    a = Button(window, image=photo_discord, command=partial(on_click, lien_discord), borderwidth=0)

    image_youtube = Image.open("assets/youtube.png")
    photo_youtube = ImageTk.PhotoImage(image_youtube)
    b = Button(window, image=photo_youtube, command=partial(on_click, lien_youtube), borderwidth=0)

    image_twitch = Image.open("assets/twitch.png")
    photo_twitch = ImageTk.PhotoImage(image_twitch)
    c = Button(window, image=photo_twitch, command=partial(on_click, lien_twitch), borderwidth=0)

    image_web = Image.open("assets/www.png")
    photo_web = ImageTk.PhotoImage(image_web)
    d = Button(window, image=photo_web, command=partial(on_click, lien_site), borderwidth=0)

    # bouton de déconnection
    logout_button = Button(window, text="LOGOUT", width=15, height=1, command=logout, bg='red', borderwidth=0)
    # appliquer la police à l'étiquette du bouton
    logout_button['font'] = f2

    # créer le texte avec l'hyper lien
    link = Label(window, text="Click to open login link", fg="blue", cursor="hand2")

    # image texte 'merci de rentrer le code de vérification'
    error_code_text = ImageTk.PhotoImage(Image.open("assets/erreur_code.png"))
    image3 = cancan.create_image(0, -10, image=error_code_text)

    # image texte 'code invalide'
    error_invalid_code_text = ImageTk.PhotoImage(Image.open("assets/erreur_code_invalide.png"))
    image4 = cancan.create_image(0, -10, image=error_invalid_code_text)

    def reload_status(i):
        global statu
        if i == 0:
            statu = 0
            print("status = 0 = deselected")
            bouton.deselect()

        elif i == 1:
            statu = 1
            print("status = 1 = selected")
            bouton.select()

    t = int(os.getenv("REMEMBER"))
    reload_status(t)

    # créer l'URL de redirection
    texte = minecraft_launcher_lib.microsoft_account.get_login_url(client_id, redirect_url)
    liste = list(texte)
    for x in range(10):
        del liste[-1]
    texte = ''.join(liste)
    print(f"Login link : {texte}")

    # Trouve la dernière version de forge en fonction de la version vanilla (1.16.5)
    forge_version = minecraft_launcher_lib.forge.find_forge_version(vanilla_version)
    print(f"forge version : {forge_version}")
    # Get Minecraft directory
    print(f"Minecraft directory : {minecraft_directory}")
    # reformat le nom de la dernière version pour qu'elle fonctionne (ex : 1.16.5-1.68.3 -> 1.16.5-forge-1.16.3)
    full_name_forge_version = forge_version.replace("-", "-forge-")
    print(f"Full name forge version : {full_name_forge_version}")
    # Vérification si la version existe, mais pas si elle est déjà téléchargée
    is_valid = minecraft_launcher_lib.forge.is_forge_version_valid(forge_version)
    print(f"Is forge version valid : {is_valid}")
    # Affiche les versions d'installées
    installed_version = minecraft_launcher_lib.utils.get_installed_versions(minecraft_directory)
    print(f"Installed versions : {installed_version}")

    def callback(_):
        webbrowser.open_new(fr"{texte}")
        reload_status(0)

    download_forge = True
    for x in installed_version:
        if x["id"] == full_name_forge_version:
            download_forge = False
    if download_forge:
        update_forge(forge_version)
    else:
        print("Valid forge version")

    a.place(x=70, y=35)
    b.place(x=110, y=35)
    c.place(x=150, y=35)
    d.place(x=190, y=35)
    launch_button.place(x=280, y=300)
    code_url.place(x=210, y=270)
    bouton.place(x=300, y=200)
    link.place(x=288, y=100)
    link.bind("<Button-1>", callback)

    if t == 1:
        code_url.place_forget()
        link.place_forget()
        bouton.place_forget()
        photo_text1 = ImageTk.PhotoImage(Image.open("assets/test.png"))
        image2 = cancan.create_image(375, 130, image=photo_text1)
        logout_button.place(x=320, y=400)

    cancan.delete(image1)

    mainloop()


if __name__ == "__main__":
    main()
