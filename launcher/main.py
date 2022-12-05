import minecraft_launcher_lib
import subprocess
import sys
import os
import wget
import shutil
import zipfile


minecraft_version= "1.7.10"
minecraft_dir = "launcher/minecraft"
forge_version = "https://maven.minecraftforge.net/net/minecraftforge/forge/1.7.10-10.13.4.1614-1.7.10/forge-1.7.10-10.13.4.1614-1.7.10-universal.jar"
current_max = 0
launch_wrapper= "https://libraries.minecraft.net/net/minecraft/launchwrapper/1.12/launchwrapper-1.12.jar"

def set_status(status: str):
    print(status)

def set_progress(progress: int):
    if current_max != 0:
        print(f"{progress}/{current_max}")

def set_max(new_max: int):
    global current_max
    current_max = new_max

callback = {
    "setStatus": set_status,
    "setProgress": set_progress,
    "setMax": set_max
}

def basic_check():
    if not os.path.isdir(minecraft_dir):
        os.makedirs(minecraft_dir)
    if not os.listdir(minecraft_dir):
        minecraft_launcher_lib.install.install_minecraft_version(minecraft_version, minecraft_dir, callback=callback)
        return True
    else:
        return True

def donwload_forge():
    if not os.path.exists("launcher/minecraft/forge.jar"):
        wget.download(forge_version, "launcher/minecraft/forge.jar")
        return True
    else :
        return True

def install_forge():
    if not os.path.isdir("launcher/minecraft/versions/1.7.10-forge/"):
        os.makedirs("launcher/minecraft/versions/1.7.10-forge/")
    if not os.listdir("launcher/minecraft/versions/1.7.10-forge/"):
        shutil.copy("launcher/minecraft/versions/1.7.10/1.7.10.jar", "launcher/minecraft/versions/1.7.10-forge/1.7.10-Forge10.13.4.1614-1.7.10.jar")
    if not os.path.exists("launcher/minecraft/versions/1.7.10-forge/1.7.10-forge.json"):
        with zipfile.ZipFile("launcher/minecraft/forge.jar", mode="r") as archive:
            for file in archive.namelist():
                if file.endswith(".json"):
                    archive.extract(file, "launcher/minecraft/versions/1.7.10-forge/")
        os.rename("launcher/minecraft/versions/1.7.10-forge/version.json","launcher/minecraft/versions/1.7.10-forge/1.7.10-forge.json")
    if not os.path.exists("launcher/minecraft/libraries/net/minecraftforge/1.7.10-forge/1.7.10-10.13.4.1614/"):
        os.makedirs("launcher/minecraft/libraries/net/minecraftforge/1.7.10-forge/1.7.10-10.13.4.1614/")
        shutil.copy("launcher/minecraft/forge.jar", "launcher/minecraft/libraries/net/minecraftforge/1.7.10-forge/1.7.10-10.13.4.1614/forge-1.7.10-10.13.4.1614.jar")
    if not os.path.exists("laucnher/minecraft/libraries/net/minecraft/launchwrapper/1.12.2"):
        os.makedirs("laucnher/minecraft/libraries/net/minecraft/launchwrapper/1.12.2")
        wget.download(launch_wrapper, "laucnher/minecraft/libraries/net/minecraft/launchwrapper/1.12.2")

        

if __name__ == "__main__":
    if not basic_check():
        print("can't install minecraft please report this as a bug")
    if not donwload_forge():
        print("can't install forge please report this as a bug")
    if donwload_forge():
        install_forge()
    if install_forge():
        dir_list = os.listdir(os.path.join(minecraft_dir, "versions"))
        print (os.listdir(os.path.join(minecraft_dir, "versions")))
        for i in dir_list:
            if not os.path.isfile(os.path.join(minecraft_dir, "versions", i, i + ".json")):
                print(i)

        forge = minecraft_launcher_lib.utils.get_installed_versions(minecraft_dir)
        print(forge)
        options = minecraft_launcher_lib.utils.generate_test_options()
        minecraft_command = minecraft_launcher_lib.command.get_minecraft_command("1.7.10-forge", minecraft_dir, options)
        subprocess.call(minecraft_command)
    
    
    

