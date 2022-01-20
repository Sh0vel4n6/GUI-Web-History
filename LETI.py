#                 Importations
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
from os import path
import os.path
import sqlite3
import csv
import getpass
import tkinter.font as tkFont


#                  FONCTIONS

# crée une fenêtre de taille fixe et la centre par rapport à l'écran et de mettre en place le titre de la fenêtre
def creerFenetre(nomFenetre, titre):
    nomFenetre.title(titre)
    # centre la fenêtre horizontalement
    positionX = int(nomFenetre.winfo_screenwidth() / 2 - 300)
    # centre la fenêtre horizontalement
    positionY = int(nomFenetre.winfo_screenheight() / 2 - 250)
    nomFenetre.geometry("600x500")
    nomFenetre.geometry("+{}+{}".format(positionX, positionY))
    nomFenetre.configure(background='white')


# permet à l'utilisateur d'utiliser l'explorateur windows pour selectionner un dossier
def getFolderPath():
  #  folder_selected = filedialog.askdirectory()
    folderPath.set(filedialog.askdirectory())

# permet d'écrire un fichier csv vers un chemin depuis un fichier source comportant plusieurs lignes de données séparées par des virgules
def ecrireCSV(chemin, source):
    with open(chemin, mode = 'a', encoding='utf-8', newline='') as csvfile:
        csv_ecriture = csv.writer(csvfile, delimiter = ',', quoting=csv.QUOTE_ALL)
        for lignes in source:
            csv_ecriture.writerow(lignes)

#                 Début du script

# récupérer le chemin de l'utilisateur

user_profile = os.environ['USERPROFILE']

# récupérer le nom d'utilisateur

username = getpass.getuser()

# ajout du logo au programme :



# _________________________Premiere fenetre______________________

fenetre1 = Tk()  # création d'une fenêtre
creerFenetre(fenetre1, "LETI - Rappels")  # attribution des paramètres de style à la fenêtre

# Titre
label_titre = Label(fenetre1, text="LETI - Logiciel d'Extraction des Traces Internet")
label_titre.configure(background="white")
label_titre['font'] = tkFont.Font(family='Arial', size=18)
label_titre.pack(pady=10)


# BANNIERE RAPPELS D'USAGES
label_header = Label(fenetre1, text="RAPPELS D'USAGES")  # creation texte et mise en place dans fenetre avec pack
label_header.configure(background="white")
label_header['font'] = tkFont.Font(family='Arial', size=16)
label_header.pack(pady=35)

# ENCART TEXTE EXPLICATIF
label_texte = Label(fenetre1, text="Avez vous pensé :")
label_texte.configure(background='white')
label_texte['font']=tkFont.Font(family='Arial', size=12)
label_texte.pack(pady=2)
label_texte2 = Label(fenetre1,
                     text="- A vérifier la cohérence horraire entre l'heure machine et l'heure réelle ?")
label_texte2.configure(background='white')
label_texte2['font'] = tkFont.Font(family='Arial', size=12)
label_texte2.pack(pady=2)
label_texte3 = Label(fenetre1, text="- A vérifier que la machine soit déconnectée de tout réseau internet ?")
label_texte3.configure(background='white')
label_texte3['font'] = tkFont.Font(family='Arial',size=12)
label_texte3.pack(pady=2)

# BOUTTON CONTINUER
label_texteboutton = Label(fenetre1, text="Si oui :")
label_texteboutton.configure(background='white')
label_texteboutton['font']=tkFont.Font(family='Arial', size=12)
label_texteboutton.pack(pady=2)

boutton = Button(fenetre1, text="Continuer", command=fenetre1.destroy)
boutton.pack(pady=6)

# destroy : boutton ferme la fenêtre en cours au clique

fenetre1.mainloop()

# _________________________Deuxième fenêtre______________________

fenetre2 = Tk()
creerFenetre(fenetre2, "LETI - chemin d'enregistrement")


folderPath = StringVar()
label_textpath = Label(fenetre2, text="Choisir la destination des résultats")
label_textpath.configure(background = 'white')
label_textpath['font']=tkFont.Font(family='Arial', size = 12)
label_textpath.pack(pady=20)
folderPath.set(os.getcwd())

entree = Entry(fenetre2, textvariable=folderPath, width=65).pack()
btn_choisir = Button(fenetre2, text="Choisir", command=getFolderPath, width=25).pack(pady=8)
btn_continuer = Button(fenetre2, text='Démarer le Scan', command=fenetre2.destroy, width=25).pack(pady=20)
fenetre2.mainloop()

# ______________________Troisième fenêtre_______________________
fenetre3 = Tk()
creerFenetre(fenetre3, "LETI - extraction")
label_sess = Label(fenetre3, text='session de : ' + username)
label_sess.configure(background = "white")
label_sess['font'] = tkFont.Font(family='Arial', size=14)
label_sess.pack(pady=10)
label_tache = Label(fenetre3, text='recherche des Navigateurs', background='white').pack()
progress1 = Progressbar(fenetre3, orient=HORIZONTAL, length=400, mode='determinate')
progress1.pack()

# rechercher les navigateurs présents
text1 = StringVar()
text1.set('Recherche FIREFOX')
label_recherche = Label(fenetre3, textvariable=text1)
label_recherche.configure(background='white')
label_recherche.pack()
firefox = path.exists(user_profile + "/AppData/Roaming/Mozilla/Firefox/Profiles")
progress1['value'] = 33
fenetre3.update_idletasks()
text1.set('recherche EDGE')
msedge = path.exists(user_profile + "/AppData/Local/Microsoft/Edge")
progress1['value'] = 67
fenetre3.update_idletasks()
text1.set('recherche chrome')
chrome = path.exists(user_profile + "/AppData/Local/Google/Chrome/User Data/Default")
progress1['value'] = 100
fenetre3.update_idletasks()

if firefox and (msedge and chrome):
    text1.set('recherche terminée, les 3 navigateurs sont présents')
elif firefox and (not msedge and chrome):
    text1.set("recherche terminée. Seuls firefox et chrome sont présents")
elif firefox and (msedge and not chrome):
    text1.set("recherche terminée. Seuls firefox et edge sont présents")
elif not firefox and (msedge and chrome):
    text1.set("recherche terminée. Seuls chrome et edge sont présents")
else:
    if firefox:
        text1.set("recherche terminée. Seul firefox est présents")
    if msedge:
        text1.set("recherche terminée. Seul edge est présents")
    if chrome:
        text1.set("recherche terminée. Seul chrome est présents")
    else:
        text1.set("recherche terminée. Aucun navigateur trouvé")

# Sur navigateur présents extraire historique et convertir en CSV :
# Puis stocker le csv dans le dossier choisi par utilisateur :

# création du répertoire dans la destination

chemin_choisi = folderPath.get()
repertoire = os.path.join(chemin_choisi, "extraction_" + username)
os.mkdir(repertoire)
label_rep = Label(fenetre3, text="chemin d'enregistrement des extractions : " + repertoire, background='white').pack(pady=10)

progress2 = Progressbar(fenetre3, orient=HORIZONTAL, length=400, mode='determinate')
progress2.pack()

# pour firefox :
if firefox :
    #on récupère le chemin du fichier places.sqlite :
    firefox_chemin = user_profile + "/AppData/Roaming/Mozilla/Firefox/Profiles"
    firefox_repertoires = os.listdir(firefox_chemin)
    historique_trouve = 0
    for root, dirs, files in os.walk(firefox_chemin):

        if "places.sqlite" in files:
            src = os.path.join(root, "places.sqlite")

            #on récupère l'historique en sql :
            sql_connect = sqlite3.connect(src)
            curseur = sql_connect.cursor()
            _SQL = "SELECT REPLACE(moz_places.url,',', ' '), REPLACE(moz_places.title,',',' ')," \
                   " datetime((moz_historyvisits.visit_date/1000000), 'unixepoch', 'localtime'), (moz_historyvisits.visit_date/1000000) as unixtimestamp" \
                   " FROM moz_historyvisits, moz_places WHERE moz_historyvisits.place_id = moz_places.id ORDER BY visit_date DESC"
            curseur.execute(_SQL)
            resultat = curseur.fetchall()
            historique_trouve = historique_trouve + 1
            histo_count = str(historique_trouve)
            print(histo_count)

            #on écrit le résultat dans un fichier csv à l'emplacement choisi par l'utilisateur :
            ecrireCSV(repertoire + '/historique_firefox_'+histo_count+'.csv', resultat)
if chrome:
    chrome_chemin = user_profile + '/AppData/Local/Google/Chrome/User Data/Default/History'
    sql_connect = sqlite3.connect(chrome_chemin)
    curseur = sql_connect.cursor()
    _SQL = "SELECT REPLACE(url,',',' '), REPLACE(title,',',' '), " \
           "datetime((last_visit_time/1000000) + " \
           "(strftime('%s', '1601-01-01')), 'unixepoch', 'localtime'), " \
           "((last_visit_time/1000000) + (strftime('%s', '1601-01-01'))) as unixtimestamp " \
           "FROM urls ORDER BY last_visit_time DESC"
    curseur.execute(_SQL)
    resultat = curseur.fetchall()
    ecrireCSV(repertoire + '/historique_chrome.csv', resultat)

if msedge:
    msedge_chemin = user_profile + '/AppData/Local/Microsoft/Edge/User Data/Default/History'
    sql_connect = sqlite3.connect(msedge_chemin)
    curseur = sql_connect.cursor()
    _SQL = "SELECT REPLACE(urls.url,',',' '), REPLACE(title,',',' '), " \
           "datetime((visit_time/1000000) - 11644473600, 'unixepoch', 'localtime'), " \
           "((visit_time/1000000) - 11644473600) as unixtimestamp" \
           " FROM urls, visits WHERE visits.url = urls.id ORDER BY visit_time DESC"
    curseur.execute(_SQL)
    resultat = curseur.fetchall()
    ecrireCSV(repertoire + '/historique_edge.csv', resultat)

progress2['value'] = 100
fenetre3.update_idletasks()

label_fin = Label(fenetre3, text='Extraction terminée, vous pouvez quitter', background='white')
label_fin['font'] = tkFont.Font(family='Arial', size=14)
label_fin.pack(pady=10)
boutton_quitter = Button(fenetre3, text='QUIITER', command=fenetre3.destroy, width=25).pack(pady=20)

fenetre3.mainloop()
