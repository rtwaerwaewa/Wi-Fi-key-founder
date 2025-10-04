import subprocess, re, pymsgbox, sys
import os
import platform
import time
import threading

ag_adlari = []

def listele_wifi_aglari() -> str:
    result = subprocess.run(
        ["netsh", "wlan", "show", "networks", "mode=bssid"],
        capture_output=True,
        text=True
    )

    wifi_names = re.findall(r"SSID \d+ : (.+)", result.stdout)
    return wifi_names

def wifi_bul():
    anahtar = ""
    flag = False

    while True:
        wifi_sayisi = input()
        try:
            wifi_sayisi = int(wifi_sayisi)
            for ag in ag_adlari:
                if str(ag).startswith(str(wifi_sayisi) + "."):
                    ag = str(ag).split()[1]

                    os.system("cls")
                    result = subprocess.run(
                        ["netsh", "interface", "show", "interface"],
                        capture_output=True,
                        text=True
                    )

                    lines = result.stdout.splitlines()
                    for line in lines:
                        part = line.split()
                        if len(part) < 4:
                            continue
                        if part[3] == "Wi-Fi":
                            if part[1].lower() != "connected":
                                pymsgbox.alert("Lütfen ağa bağlı olduğunuzdan emin olunuz", "Wi-Fi_sifre_bulucu - Hata", icon=16)
                                return wifi_bul()
                            
                            result = subprocess.run(
                                ["netsh", "wlan", "show", "profile", ag, "key=clear"],
                                capture_output=True,
                                text=True
                            ).stdout
                            print(ag)
                            for line in result.splitlines():
                                if "Key Content" in line:
                                    idx = line.find(":")
                                    if idx != -1:
                                        anahtar = line[idx + 1:].strip()
                                        print(f"{ag} adlı agin sifresi bulundu : {anahtar}")
                                    else:
                                        anahtar = None

                                    pymsgbox.alert(f"ag adi -> {ag}  :  sifre -> {anahtar}", "Wi-Fi_sifre_bulucu - Bilgi", icon=64)

                    if flag == True:
                        break

            if flag == True:
                flag = False
                break

                
        except ValueError:
            pymsgbox.alert("Lütfen sadece sayı giriniz", "Wi-Fi_sifre_bulucu - Hata", icon=16)

if __name__ == '__main__':
    OS_SYSTEM = platform.system()
    aglar = listele_wifi_aglari()
    thread =threading.Thread(target=wifi_bul)
    thread.daemon = True
    thread.start()

    while True:
        print("sifresini ogrenmek istediginiz wifinin basinda bulunan sayiyi girip entera basiniz...")
        print("-------------------------------------------- --------------------------------------------\n\n")
        ag_adlari.clear()
        for i, ad in enumerate(aglar, start=1):
            ag_adlari.append(f"{i}. {ad}")
            print(f"{i}. {ad}")

        time.sleep(10)
        
        if OS_SYSTEM.lower() == 'windows': os.system("cls")
        else: sys.exit(1)
