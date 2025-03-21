# -*- coding: utf-8 -*-
"""管理人用メモ
1.東方の新しい原作が出たら「#新しいゲームが出たらここを変更する」を検索にかけてそれぞれ追加する
2.バグはさっさと潰す
"""
#まずはライブラリのインポートから
from tkinter import *
from tkinter import Tk
from tkinter import Listbox
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from pathlib import Path
import subprocess
import json
import os
import codecs
import sys
from time import sleep
import webbrowser
import shutil

#続いていろいろな関数の定義
global dire
global setting
global game_name
dire = []
setting = [[],""]
everyL = {}
def exit_py():
    app = False
    sys.exit()
global languages
languages = []

def setup():
    def set0_w_w():
        set0_w()
        while len(search_dire_k) != 0:
            page3_next['state'] = 'disabled'
        page3_next['state'] = 'normal'
    
    dire = []
    setting = [[],""]
    data = [{},[],[[],""],{}]
    
    def data_json_w():
        setting[1] = language
        data[2] = setting
        data[3] = everyL
        data_json = Path("Appdata\\data.json")
        data_json = data_json.resolve()
        with open(data_json,"w",encoding="utf-8") as f:
            json.dump(data,f)
    
    global setup_w
    setup_w = Tk()
    setup_w.title("TouhouGameLauncher Setup")
    setup_w.geometry("500x500")
    setup_w.iconbitmap(default="icon.ico")
    
    def setup_close():
        setup_w.destroy()
        global app
        app = True
        #direのディレクトリが存在していればスルー、1つでも存在していないものがあれば自動的にリロードするため、dataのdireを初期化。
        for i in dire:
            if os.path.exists(i) == False:
                print(os.path.exists(i))
                print("ディレクトリ：" + i + "、非存在")
                print("リストを初期化")
                dire = []
                data[1] = dire
                data[3] = everyL
                with open("Appdata\\data.json","w") as f:
                    json.dump(data,f)
                break
            else:
                print(os.path.exists(i))
                print("ディレクトリ：" + i + "、存在確認")
        #dataからsettingのlanguageを検出
        global language
        if len(data[2]) == 2:
            if data[2][1] != "":
                language = data[2][1]
            else:
                language = "Japanese"
                setting[1] = language
                data[2] = setting
                data[3] = everyL
                with open("Appdata\\data.json","w") as f:
                    json.dump(data,f)
        else:
            language = "Japanese"
            setting[1] = language
            data[2] = setting
            data[3] = everyL
            with open("Appdata\\data.json","w") as f:
                json.dump(data,f)
        if len(dire) == 0:
            file_load()
            load()
        else:
            global Ingames
            Ingames = []
            for i in dire:
                Ingames.append(i)
            load()
        
        launcher_widget()
    
    
    def next3():
        page2.destroy()
        page3 = Canvas(setup_w,width=500,height=500)
        page3.place(x=0,y=0)
        message2 = Label(page3,text=messages[language][0][51])
        message2.pack()
        setting[0] = search_dire_k
        data_json_w()
        message2['text'] = messages[language][0][52]
        message2.update()
        setup_close_b = Button(page3,text=messages[language][0][53],font=30,command=setup_close)
        setup_close_b.pack(side=BOTTOM)
    
    def next2():
        global page3
        global page3_next
        data_json_w()
        print("言語”" + language + "”を選択")
        print(setting)
        #ページ2：ファイル検索場所を選択
        page2.destroy()
        page3 = Canvas(setup_w,width=500,height=500)
        page3.place(x=0,y=0)
        message1 = Label(page2,text=messages[language][0][49],font=30)
        message1.pack()
        sansho_dire_b = Button(page2,text=messages[language][0][28],font=30,command=set0_w_w)
        sansho_dire_b.pack()
        page3_next = Button(page2,text=messages[language][0][48],font=30,command=next3)
        page3_next.pack(side=BOTTOM)
    
    def sele_fi():
        global search_dire_k
        filet = [("JSON sorce","*.json")]
        file = filedialog.askopenfilename(filetypes=filet,initialdir="PC")
        if file != "":
            if os.path.isfile(file) == False:
                messagebox.showerror(messages[language][0][8],messages[language][0][58])
            else:
                with open(file,"r",encoding="utf-8") as f:
                    data = json.load(f)
                if (len(data) == 4) and (len(data[2]) == 2):
                    shutil.copy(file,"Appdata")
                    setting = data[2]
                    search_dire_k = setting[0]
                    next3()
                else:
                    messagebox.showerror(messages[language][0][8],messages[language][0][59])
    
    def next1():
        global page2
        page1.destroy()
        page2 = Canvas(setup_w,width=500,height=500)
        page2.place(x=0,y=0)
        message1 = Label(page2,text=messages[language][0][55],font=30)
        message1.pack()
        sansyo = Button(page2,text=messages[language][0][56],font=30,command=next2)
        se_fi = Button(page2,text=messages[language][0][57],font=30,command=sele_fi)
        sansyo.pack()
        se_fi.pack()
    
    def sentaku1(event):
        page1_next['state'] = 'normal'
        global language
        sela = language_box.get()
        language = languages[language_h.index(sela)]
        setup_w.title(messages[language][0][50])
        page1_next['text'] = messages[language][0][48]
        Title['text'] = messages[language][0][54]
    
    #ページ1：言語選択
    page1 = Canvas(setup_w,width=500,height=500)
    page1.place(x=0,y=0)
    Title = Label(page1,text="TouhouGameLauncher\nSetup wizard",font=("Engravers MT",20))
    language_h = []
    for i in languages:
        language_h.append(messages[i][1])
    language_box = ttk.Combobox(page1,height=3,width=15,justify="center",state="readonly",values=language_h)
    page1_next = Button(page1,text="Next",command=next1,font=30)
    Title.place(x=250,y=40,anchor=CENTER)
    language_box.place(x=200,y=200)
    page1_next.place(x=440,y=465)
    page1_next['state'] = 'disabled'
    language_box.bind("<<ComboboxSelected>>",sentaku1)
    
    setup_w.mainloop()

def set0_w():
    set0_window = Tk()
    set0_window.geometry("400x400")
    set0_window.title(messages[language][0][28])
    set0_window.iconbitmap("icon.ico")
    
    global search_dire_k
    search_dire_k = []
    if len(setting[0]) != 0:
        for i in setting[0]:
            search_dire_k.append(i)
    print(search_dire_k)
    dire_list_var = StringVar(set0_window,value=search_dire_k)
    dire_list = Listbox(set0_window,width=100,font=30,listvariable=dire_list_var)
    dire_list_var.set(search_dire_k)
    
    def folder_add():
        folder = filedialog.askdirectory(title=messages[language][0][29],initialdir="PC")
        if folder != "":
            search_dire_k.append(folder)
            dire_list_var.set(search_dire_k)
        set0_window.lift()
    def folder_delete():
        try:
            selected_folder = dire_list.get(dire_list.curselection())
            search_dire_k.remove(selected_folder)
            dire_list_var.set(search_dire_k)
        except IndexError as e:
            error = messages[language][0][30] + e
            messagebox.showerror(messages[language][0][8],error)
        except TypeError as e:
            error = messages[language][0][30] + e
            messagebox.showerror(messages[language][0][8],error)
    def close_set0():
        set0_window.destroy()
    
    set0_add = Button(set0_window,text=messages[language][0][31],font=30,command=folder_add)
    set0_delete = Button(set0_window,text=messages[language][0][32],font=30,command=folder_delete)
    set0_close = Button(set0_window,text=messages[language][0][33],font=30,command=close_set0)
    
    dire_list.pack()
    set0_add.pack(side=LEFT)
    set0_delete.pack(side=LEFT)
    set0_close.pack(side=RIGHT)
    
    set0_window.mainloop()

#language.jsonの読み込み（韓国語を直接プログラムに入れない。）
path = Path("Appdata\\language.json")
path = path.resolve()
if os.path.isfile(path):
    try:
        with open(path,"r",encoding="utf-8") as f:
            language_j = json.load(f)
    except TypeError as e:
        messagebox.showerror("Error",f"I couldn't read ”language.json” file.\nDid you change out the contents of ”language.json” file?\nTypeError : {e}")
        exit_py()
else:
    messagebox.showerror("Error","I couldn't find ”language.json” file.\nYou have to install ”language.json” file in ”Appdata” folder.")
    exit_py()

messages = language_j[0]
games = language_j[1]

for i in list(messages):
    languages.append(i)
    print("言語パック”" + i + "”を認識")

#検索をするためのとても重要な関数
def file_load():
    #様々な変数のグローバル化
    global Ingames
    global kensaku
    global data
    
    #data.jsonの読み込み
    data = []
    p = Path('Appdata\\data.json')
    if os.path.isfile(p.resolve()):
        try:
            with open('Appdata\\data.json',mode="r",encoding="utf-8") as f:
                data = json.load(f)
            dire = []
            setting = []
            file_names = data[0]
            dire = data[1]
            setting = data[2]
            language = setting[1]
            everyL = data[3]
        except TypeError as e:
            setup()
    else:
        setup()
    
    if len(setting[0]) == 0:
        setup()
        return
    
    #ディレクトリ検索用のウィンドウを生成する。
    kensaku = Tk()
    kensaku.title("TouhouGameLauncher ver2.2.1")
    kensaku.geometry("300x100")
    kensaku.iconbitmap(default="icon.ico")
    kensakuchu = ttk.Label(kensaku,text=messages[language][0][0],font=30)
    kensakuchu.pack()
    kensaku.update()
    kensaku.lift()
    Ingames = []
    kensaku.update()
    
    for j in setting[0]:
        folder = Path(j)
        print("ディレクトリ「" + str(folder) + "」を探索中")
        for i in folder.glob("**/th[0-9][0-9].exe"):
            Ingames.append(str(i))
        

def load():
    #様々な変数のグローバル化2
    global game_list
    global file_names
    global result_search_index
    global result_search_index_games
    global result_search_index_custom
    global Incustom
    global check_game
    global dire
    global item_game_list
    
    Incustom = []
    check_game = [0 for i in range(26)]
    #AppDataになんか生成される人もいるので除外。なんかバグあり。
    jogai = 0
    for jogai in Ingames:
        if "AppData" in jogai:
            Ingames.pop(Ingames.index(jogai))
    
    
    #custom.exe起動用にリストを作っておく
    #新しいゲームが出たらここを変更する
    for i in Ingames:
        if "th06.exe" in i:
            Incustom.append(i.replace("th06.exe", "custom.exe"))
        if "th07.exe" in i:
            Incustom.append(i.replace("th07.exe", "custom.exe"))
        if "th075.exe" in i:
            Incustom.append(i.replace("th075.exe", "custom.exe"))
        if "th08.exe" in i:
            Incustom.append(i.replace("th08.exe", "custom.exe"))
        if "th09.exe" in i:
            Incustom.append(i.replace("th09.exe", "custom.exe"))
        if "th095.exe" in i:
            Incustom.append(i.replace("th095.exe", "custom.exe"))
        if "th10.exe" in i:
            Incustom.append(i.replace("th10.exe", "custom.exe"))
        if "th105.exe" in i:
            Incustom.append(i.replace("th105.exe", "custom.exe"))
        if "th11.exe" in i:
            Incustom.append(i.replace("th11.exe", "custom.exe"))
        if "th12.exe" in i:
            Incustom.append(i.replace("th12.exe", "custom.exe"))
        if "th123.exe" in i:
            Incustom.append(i.replace("th123.exe", "custom.exe"))
        if "th125.exe" in i:
            Incustom.append(i.replace("th125.exe", "custom.exe"))
        if "th128.exe" in i:
            Incustom.append(i.replace("th128.exe", "custom.exe"))
        if "th13.exe" in i:
            Incustom.append(i.replace("th13.exe", "custom.exe"))
        if "th135.exe" in i:
            Incustom.append(i.replace("th135.exe", "custom.exe"))
        if "th14.exe" in i:
            Incustom.append(i.replace("th14.exe", "custom.exe"))
        if "th143.exe" in i:
            Incustom.append(i.replace("th143.exe", "custom.exe"))
        if "th145.exe" in i:
            Incustom.append(i.replace("th145.exe", "custom.exe"))
        if "th15.exe" in i:
            Incustom.append(i.replace("th15.exe", "custom.exe"))
        if "th155.exe" in i:
            Incustom.append(i.replace("th155.exe", "custom.exe"))
        if "th16.exe" in i:
            Incustom.append(i.replace("th16.exe", "custom.exe"))
        if "th165.exe" in i:
            Incustom.append(i.replace("th165.exe", "custom.exe"))
        if "th17.exe" in i:
            Incustom.append(i.replace("th17.exe", "custom.exe"))
        if "th175.exe" in i:
            Incustom.append(i.replace("th175.exe", "custom.exe"))
        if "th18.exe" in i:
            Incustom.append(i.replace("th18.exe", "custom.exe"))
        if "th19.exe" in i:
            Incustom.append(i.replace("th19.exe", "custom.exe"))
    
    for j in range(len(Ingames)):
        for i in range(len(game_name)):
            if game_name[i] in Ingames[j]:
                check_game[i] = 1
    
    #PCに存在するゲーム名（実行可能ファイル名）の抽出
    item_game_list = []
    for k in range(len(check_game)):
        if check_game[k] == 1:
            item_game_list.append(game_name[k])
    
    #Listbox（GUI）に先ほど検索したものを列挙する
    launch_list = []
    game_list = []
    for item in item_game_list:
        launch_list.append(item)
        try:
            game_list.append(games[language][item])
        except KeyError:
            game_list.append(games["English"][item])
            print("エラー：ゲーム言語パック”" + language + "”が見つからない為、英語を適用")
        else:
            print("ゲーム言語パック”" + language + "”の" + item + "つ目の項目を正常に認識")
    
    result_search_index_games = []
    result_search_index_custom = []
    
    #選択されたゲームのファイルの候補を出す
    #Ingames：見つかったゲームのディレクトリ
    for ll in range(len(launch_list)):
        result_search_index_games.append([])
        for ig in range(len(Ingames)):
            if launch_list[ll] in Ingames[ig]:
                result_search_index_games[ll].append(Ingames[ig])
                
    #選択されたcustom.exeの候補を出す
    for ll in range(len(launch_list)):
        result_search_index_custom.append([])
        for ig in range(len(Ingames)):
            if launch_list[ll] in Ingames[ig]:
                result_search_index_custom[ll].append(Incustom[ig])
    
    #direに要素を追加
    dire = []
    for i in Ingames:
        dire.append(i)
    data[1] = dire
    with open('Appdata\\data.json',"w") as f:
        json.dump(data,f)
    

def reload():
    #ウィンドウlauncherを閉じる
    launcher.destroy()
    #data.jsonの読み込み
    global data
    data = []
    p = Path('Appdata\\data.json')
    if os.path.isfile(p.resolve()):
        try:
            with open('Appdata\\data.json',mode="r",encoding="utf-8") as f:
                data = json.load(f)
            dire = []
            setting = []
            file_names = data[0]
            dire = data[1]
            setting = data[2]
            language = setting[1]
            everyL = data[3]
        except TypeError as e:
            setup()
    else:
        setup()
    
    #ディレクトリ検索
    file_load()
    #インデックス作成
    load()
    #オブジェクト配置
    kensaku.destroy()
    launcher_widget()

#data.jsonの読み込み
data = []
p = Path('Appdata\\data.json')
if os.path.isfile(p.resolve()) == False:
    setup()

if os.path.isfile(p.resolve()):
    try:
        with open('Appdata\\data.json',mode="r",encoding="utf-8") as f:
            data = json.load(f)
        global file_names
        file_names = data[0]
        dire = data[1]
        setting = data[2]
        everyL = data[3]
    except TypeError as e:
        file_names = {}
        dire = []
        setting = []
        everyL = {}
        setup()
else:
    file_names = {}
    dire = []
    setting = []
    everyL = {}
    setup()

#新しいゲームが出たらここを変更する
game_name = ["th06.exe","th07.exe","th075.exe","th08.exe","th09.exe","th095.exe","th10.exe","th105.exe","th11.exe","th12.exe","th123.exe","th125.exe","th128.exe","th13.exe","th135.exe","th14.exe","th143.exe","th145.exe","th15.exe","th155.exe","th16.exe","th165.exe","th17.exe","th18.exe","th185.exe","th19.exe"]

#data.jsonの読み込み
data = []
p = Path('Appdata\\data.json')
if os.path.isfile(p.resolve()) == False:
    setup()
else:
    with open(p.resolve(),"r",encoding="utf-8") as f:
        data = json.load(f)


def data_json_update(message):
    data = [{},[],[]]
    data[0] = file_names
    data[1] = dire
    data[2] = setting
    data[3] = everyL
    with open("Appdata\\data.json","w") as f:
        json.dump(data,f)
    if message == "":
        messagebox.showinfo(messages[language][0][6],messages[language][0][7])
    elif message != None:
        messagebox.showinfo(messages[language][0][6],message)
    reload()

#direのディレクトリが存在していればスルー、1つでも存在していないものがあれば自動的にリロードするため、dataのdireを初期化。
for i in dire:
    if os.path.exists(i) == False:
        print(os.path.exists(i))
        print("ディレクトリ：" + i + "、非存在")
        print("リストを初期化")
        dire = []
        data[1] = dire
        data[3] = everyL
        with open("Appdata\\data.json","w") as f:
            json.dump(data,f)
        break
    else:
        print(os.path.exists(i))
        print("ディレクトリ：" + i + "、存在確認")
        

#dataからsettingのlanguageを検出
global language
if len(data[2]) == 2:
    if data[2][1] != "":
        language = data[2][1]
    else:
        language = "Japanese"
        setting[1] = language
        data[2] = setting
        data[3] = everyL
        with open("Appdata\\data.json","w") as f:
            json.dump(data,f)
else:
    language = "Japanese"
    setting[1] = language
    data[2] = setting
    data[3] = everyL
    with open("Appdata\\data.json","w") as f:
        json.dump(data,f)

if os.path.isfile(p.resolve()):
    try:
        with open('Appdata\\data.json',mode="r",encoding="utf-8") as f:
            data = json.load(f)
        file_names = data[0]
        dire = data[1]
        setting = data[2]
        everyL = data[3]
    except TypeError as e:
        file_names = {}
        dire = []
        setting = []
        everyL = {}
        setup()
else:
    file_names = {}
    dire = []
    setting = []
    everyL = {}
    setup()

#ここで読み込み関数実行
try:
    if len(dire) == 0:
        file_load()
        load()
    else:
        global Ingames
        Ingames = []
        for i in dire:
            Ingames.append(i)
        load()
except UnboundLocalError or TclError or NameError:
    exit_py()
except TypeError as e:
    print("TypeError : " + str(e))
    if os.path.isfile("Appdata\\data.json"):
        os.remove("Appdata\\data.json")
    setup()


def selected_index():
    selected_game2 = gamelist.curselection()
    global selected_game
    selected_game = selected_game2[0]
    

def append_quick(event):
    global selected_game4
    selected_game4 = launch_game2_list.curselection()
    everyL[item_game_list[selected_game]] = selected_game4[0]
    data[3] = everyL
    with open("Appdata\\data.json","w",encoding="utf-8") as f:
        json.dump(data,f)
    open_list_h[open_list.index(item_game_list[selected_game])] = "[Q]" + open_list_h[open_list.index(item_game_list[selected_game])]
    launch_game2_list.update()

def launch_game():
    #thXX.exeを起動するための処理
    try:
        selected_index()
        if len(result_search_index_games[selected_game]) >= 2:
            #ファイル候補を出す
            global launch_game2
            global launch_game2_list
            global launch_game2_list_var
            global open_list_h
            global open_list
            launch_game2 = Tk()
            launch_game2.geometry("550x200")
            launch_game2.title("TouhouGameLauncher ver2.2.1")
            launch_game2.iconbitmap(default="icon.ico")
            
            open_list = []
            open_list_h = []
            
            def open_game():
                try:
                    global selected_game4
                    selected_game4 = launch_game2_list.curselection()
                    open_games = open_list[selected_game4[0]]
                    result = result_search_index_games[selected_game][open_games]
                    result2 = result
                    #新しいゲームが出たらここを変更する
                    if ("\\th06.exe" in result) == True:
                        result = result.replace('\\th06.exe', '')
                    if ("\\th07.exe" in result) == True:
                        result = result.replace('\\th07.exe', '')
                    if ("\\th075.exe" in result) == True:
                        result = result.replace('\\th075.exe', '')
                    if ("\\th08.exe" in result) == True:
                        result = result.replace('\\th08.exe', '')
                    if ("\\th09.exe" in result) == True:
                        result = result.replace('\\th09.exe', '')
                    if ("\\th095.exe" in result) == True:
                        result = result.replace('\\th095.exe', '')
                    if ("\\th10.exe" in result) == True:
                        result = result.replace('\\th10.exe', '')
                    if ("\\th105.exe" in result) == True:
                        result = result.replace('\\th105.exe', '')
                    if ("\\th11.exe" in result) == True:
                        result = result.replace('\\th11.exe', '')
                    if ("\\th12.exe" in result) == True:
                        result = result.replace('\\th12.exe', '')
                    if ("\\th123.exe" in result) == True:
                        result = result.replace('\\th123.exe', '')
                    if ("\\th125.exe" in result) == True:
                        result = result.replace('\\th125.exe', '')
                    if ("\\th128.exe" in result) == True:
                        result = result.replace('\\th128.exe', '')
                    if ("\\th13.exe" in result) == True:
                        result = result.replace('\\th13.exe', '')
                    if ("\\th135.exe" in result) == True:
                        result = result.replace('\\th135.exe', '')
                    if ("\\th14.exe" in result) == True:
                        result = result.replace('\\th14.exe', '')
                    if ("\\th143.exe" in result) == True:
                        result = result.replace('\\th143.exe', '')
                    if ("\\th145.exe" in result) == True:
                        result = result.replace('\\th145.exe', '')
                    if ("\\th15.exe" in result) == True:
                        result = result.replace('\\th15.exe', '')
                    if ("\\th155.exe" in result) == True:
                        result = result.replace('\\th155.exe', '')
                    if ("\\th16.exe" in result) == True:
                        result = result.replace('\\th16.exe', '')
                    if ("\\th165.exe" in result) == True:
                        result = result.replace('\\th165.exe', '')
                    if ("\\th17.exe" in result) == True:
                        result = result.replace('\\th17.exe', '')
                    if ("\\th175.exe" in result) == True:
                        result = result.replace('\\th175.exe', '')
                    if ("\\th18.exe" in result) == True:
                        result = result.replace('\\th18.exe', '')
                    if ("\\th19.exe" in result) == True:
                        result = result.replace('\\th19.exe', '')
                    launcher.destroy()
                    launch_game2.destroy()
                    print("アプリを開く：「" + result2 + "」、「" + result + "」の上で")
                    subprocess.run(result2,shell=True,cwd=result)
                    exit_py()
                except TypeError as e:
                    error = messages[language][0][9] + e
                    messagebox.showerror(messages[language][0][8],error)
            
            def open_game_cancel():
                launch_game2.destroy()
            
            def rename():
                try:
                    global selected_game4
                    global rename_window
                    selected_game4 = launch_game2_list.curselection()
                    open_games = open_list[selected_game4[0]]
                    result = result_search_index_games[selected_game][open_games]
                    rename_window = Tk()
                    rename_window.geometry("500x100")
                    rename_window.title("TouhouGameLauncher ver2.2.1")
                    rename_window.iconbitmap(default="icon.ico")
                    rename_label = Label(rename_window,text=messages[language][0][10],font=30)
                    rename_label2 = Label(rename_window,text=result)
                    rename_entry = Entry(rename_window,width=490)
                    if result_search_index_games[selected_game][open_games] in file_names:
                        rename_entry.insert(END,file_names[result_search_index_games[selected_game][open_games]])
                    
                    def rename_s():
                        rename_e = rename_entry.get()
                        if len(rename_e) > 0:
                            file_names[result] = rename_e
                            data_json_update("")
                            renames = False
                            rename_window.destroy()
                        elif "\\" in rename_e:
                            messagebox.showerror(messages[language][0][8],messages[language][0][11])
                        elif len(rename_e) == 0:
                            messagebox.showerror(messages[language][0][8],messages[language][0][12])
                    
                    def rename_r():
                        hyouji = open_list_h[open_games]
                        msg = messages[language][0][14] + hyouji
                        question = messagebox.askquestion(messages[language][0][13],msg)
                        if question == 'yes':
                            file_names.pop(result_search_index_games[selected_game][open_games])
                            data_json_update("")
                    
                    def rename_c():
                        renames = False
                        rename_window.destroy()
                    
                    rename_setting = Button(rename_window,text=messages[language][0][16],font=30,command=rename_s)
                    rename_reset = Button(rename_window,text=messages[language][0][17],font=30,command=rename_r)
                    rename_cancel = Button(rename_window,text=messages[language][0][18],font=30,command=rename_c)
                    
                    rename_label.pack()
                    rename_label2.pack()
                    rename_entry.pack()
                    rename_setting.pack(side=LEFT)
                    rename_reset.pack(side=LEFT)
                    rename_cancel.pack(side=RIGHT)
                    rename_window.update()
                    launch_game2.update()
                except IndexError as e:
                    error = messages[language][0][9] + e
                    messagebox.showerror(messages[language][0][8],error)
            
            launch_game2_label = ttk.Label(launch_game2,text=messages[language][0][19],font=30)
            for i in range(len(result_search_index_games[selected_game])):
                if (selected_game,i) in everyL:
                    if result_search_index_games[selected_game][i] in file_names:
                        a = "[Q]" + file_names[result_search_index_games[selected_game][i]]
                        open_list_h.append(a)
                    else:
                        a = "[Q]" + result_search_index_games[selected_game][i]
                        open_list_h.append(a)
                else:
                    if result_search_index_games[selected_game][i] in file_names:
                        a = file_names[result_search_index_games[selected_game][i]]
                        open_list_h.append(a)
                    else:
                        a = result_search_index_games[selected_game][i]
                        open_list_h.append(a)
                open_list.append(i)
            launch_game2_list_var = StringVar(launch_game2,value=open_list_h)
            launch_game2_list = Listbox(launch_game2,width=490,font=20,height=5,listvariable=launch_game2_list_var)
            launch_game2_open = Button(launch_game2,text=messages[language][0][20],font=30,command=open_game)
            launch_game2_rename = Button(launch_game2,text=messages[language][0][21],font=30,command=rename)
            launch_game2_cancel = Button(launch_game2,text=messages[language][0][18],font=30,command=open_game_cancel)
            launch_game2_list.bind("<Button-3>",append_quick)
            launch_game2_label.pack()
            launch_game2_list.pack()
            launch_game2_open.pack(side=LEFT)
            launch_game2_rename.pack(side=LEFT)
            launch_game2_cancel.pack(side=RIGHT)
            launch_game2.update()
        elif len(result_search_index_games[selected_game]) == 1:
            print(result_search_index_games[selected_game][0])
            result = result_search_index_games[selected_game][0]
            result2 = result
            #新しいゲームが出たらここを変更する
            if ("\\th06.exe" in result) == True:
                result = result.replace('\\th06.exe', '')
            if ("\\th07.exe" in result) == True:
                result = result.replace('\\th07.exe', '')
            if ("\\th075.exe" in result) == True:
                result = result.replace('\\th075.exe', '')
            if ("\\th08.exe" in result) == True:
                result = result.replace('\\th08.exe', '')
            if ("\\th09.exe" in result) == True:
                result = result.replace('\\th09.exe', '')
            if ("\\th095.exe" in result) == True:
                result = result.replace('\\th095.exe', '')
            if ("\\th10.exe" in result) == True:
                result = result.replace('\\th10.exe', '')
            if ("\\th105.exe" in result) == True:
                result = result.replace('\\th105.exe', '')
            if ("\\th11.exe" in result) == True:
                result = result.replace('\\th11.exe', '')
            if ("\\th12.exe" in result) == True:
                result = result.replace('\\th12.exe', '')
            if ("\\th123.exe" in result) == True:
                result = result.replace('\\th123.exe', '')
            if ("\\th125.exe" in result) == True:
                result = result.replace('\\th125.exe', '')
            if ("\\th128.exe" in result) == True:
                result = result.replace('\\th128.exe', '')
            if ("\\th13.exe" in result) == True:
                result = result.replace('\\th13.exe', '')
            if ("\\th135.exe" in result) == True:
                result = result.replace('\\th135.exe', '')
            if ("\\th14.exe" in result) == True:
                result = result.replace('\\th14.exe', '')
            if ("\\th143.exe" in result) == True:
                result = result.replace('\\th143.exe', '')
            if ("\\th145.exe" in result) == True:
                result = result.replace('\\th145.exe', '')
            if ("\\th15.exe" in result) == True:
                result = result.replace('\\th15.exe', '')
            if ("\\th155.exe" in result) == True:
                result = result.replace('\\th155.exe', '')
            if ("\\th16.exe" in result) == True:
                result = result.replace('\\th16.exe', '')
            if ("\\th165.exe" in result) == True:
                result = result.replace('\\th165.exe', '')
            if ("\\th17.exe" in result) == True:
                result = result.replace('\\th17.exe', '')
            if ("\\th175.exe" in result) == True:
                result = result.replace('\\th175.exe', '')
            if ("\\th18.exe" in result) == True:
                result = result.replace('\\th18.exe', '')
            if ("\\th19.exe" in result) == True:
                result = result.replace('\\th19.exe', '')
            launcher.destroy()
            print("アプリを開く：「" + result2 + "」、「" + result + "」の上で")
            subprocess.run(result2,shell=True,cwd=result)
            exit_py()
        elif len(result_search_index_games[selected_game]) == 0:
            error = messages[language][0][22]
            for i in setting[0]:
                error = error + i + ",\n"
            messagebox.showerror(messages[language][0][8],error)
    except TypeError as e:
        error = messages[language][0][9] + e
        messagebox.showerror(messages[language][0][8],error)

def launch_custom():
    try:
        selected_index()
        if len(result_search_index_custom[selected_game]) >= 2:
            #ファイル候補を出す
            global launch_custom2
            launch_custom2 = Tk()
            launch_custom2.geometry("550x200")
            launch_custom2.title("TouhouGameLauncher ver2.2.1")
            launch_custom2.iconbitmap(default="icon.ico")
            open_list = []
            open_list_h = []
            
            def open_custom():
                try:
                    global selected_game4
                    selected_game4 = launch_custom2_list.curselection()
                    open_games = open_list[selected_game4[0]]
                    result = result_search_index_custom[selected_game][open_games]
                    result2 = result
                    result = result.replace("\\custom.exe","")
                    launch_custom2.destroy()
                    print("アプリを開く：「" + result2 + "」、「" + result + "」の上で")
                    if os.path.isfile(result2):
                        print("アプリを開く：「" + result2 + "」、「" + result + "」の上で")
                        subprocess.run(result2,shell=True,cwd=result)
                    else:
                        error = messages[language][0][23] + result
                        messagebox.showerror(messages[language][0][8],error)
                except IndexError as e:
                    error = messages[language][0][9] + e
                    messagebox.showerror(messages[language][0][8],error)
            
            def open_custom_cancel():
                launch_custom2.destroy()
            
            launch_custom2_label = ttk.Label(launch_custom2,text=messages[language][0][24],font=30)
            launch_custom2_list = Listbox(launch_custom2,width=490,font=20,height=5)
            for i in range(len(result_search_index_games[selected_game])):
                if result_search_index_games[selected_game][i] in file_names:
                    launch_custom2_list.insert(END,file_names[result_search_index_games[selected_game][i]])
                    open_list_h.append(file_names[result_search_index_games[selected_game][i]])
                else:
                    launch_custom2_list.insert(END,result_search_index_games[selected_game][i])
                    open_list_h.append(result_search_index_games[selected_game][i])
                open_list.append(i)
            launch_custom2_open = Button(launch_custom2,text=messages[language][0][25],font=30,command=open_custom)
            launch_custom2_cancel = Button(launch_custom2,text=messages[language][0][18],font=30,command=open_custom_cancel)
            launch_custom2_label.pack()
            launch_custom2_list.pack()
            launch_custom2_open.pack(side=LEFT)
            launch_custom2_cancel.pack(side=RIGHT)
            launch_custom2.mainloop()
        elif len(result_search_index_custom[selected_game]) == 1:
            result = result_search_index_custom[0][0]
            result2 = result
            result = result.replace("\\custom.exe","")
            if os.path.isfile(result2):
                print("アプリを開く：「" + result2 + "」、「" + result + "」の上で")
                subprocess.run(result2,shell=True,cwd=result)
            else:
                error = messages[language][0][23] + result
                messagebox.showerror(messages[language][0][8],error)
        elif len(result_search_index_custom[selected_game]) == 0:
            error = messages[language][0][26]
            for i in setting[0]:
                error = error + i + ",\n"
            messagebox.showerror(messages[language][0][8],error)
    except TypeError as e:
        error = messages[language][0][9] + e
        messagebox.showerror(messages[language][0][8],error)
        

def settings():
    setting_window = Tk()
    setting_window.geometry("400x400")
    setting_window.title(messages[language][0][27])
    setting_window.iconbitmap("icon.ico")
    
    def save_setting():
        setting[0] = search_dire_k
        setting_window.destroy()
        data_json_update(messages[language][0][34])
    
    def cancel_setting():
        setting_window.destroy()
    
    def set0_w2():
        set0_w()
        setting_window.lift()
    
    set0_button = Button(setting_window,text=messages[language][0][35],font=30,command=set0_w2)
    setting_save = Button(setting_window,text=messages[language][0][36],font=30,command=save_setting)
    setting_cancel = Button(setting_window,text=messages[language][0][18],font=30,command=cancel_setting)
    
    set0_button.pack(side=LEFT)
    setting_cancel.pack(side=RIGHT,anchor=S)
    setting_save.pack(side=RIGHT,anchor=S)
    
    setting_window.mainloop()

def app_info():
    info_window = Tk()
    info_window.geometry("500x300")
    info_window.iconbitmap("icon.ico")
    info_window.title("TouhouGameLauncher ver2.2.1")
    
    info_title = Label(info_window,text="Touhou Game Launcher",font=50)
    info_version = Label(info_window,text="ver2.2.1\nProgramed by Gottsudayo\n2025-2025",font=20)
    
    def close_info():
        info_window.destroy()
        
    info_ok = Button(info_window,text="ok",font=30,command=close_info)
    
    info_title.pack()
    info_version.pack()
    info_ok.pack(side=BOTTOM)
    
    info_window.mainloop()

class Gengo():
    def setlang(self,lang):
        self.lang2 = lang
    def change(self):
        global language
        language = self.lang2
        setting[1] = language
        data_json_update("Complete change language\nApplication will be restarted.")
    
    def addCommand(self):
        hyouji_me = messages[self.lang2][1]
        menu_language.add_command(label=hyouji_me,command=Gengo.change)

def open_sorce():
    webbrowser.open("https://github.com/gottsudayo/TouhouGameLauncher-Python-")

def open_wiki():
    webbrowser.open("https://github.com/gottsudayo/TouhouGameLauncher-Python-/wiki")

def open_otoiawase():
    webbrowser.open("https://github.com/gottsudayo/TouhouGameLauncher-Python-/wiki/%E3%81%8A%E5%95%8F%E3%81%84%E5%90%88%E3%82%8F%E3%81%9B")

def quick_launch(event):
    selected_index()
    if item_game_list[selected_game] in everyL:
        result = everyL[item_game_list[selected_game]]
        result2 = result
        #新しいゲームが出たらここを変更する
        if ("\\th06.exe" in result) == True:
            result = result.replace('\\th06.exe', '')
        if ("\\th07.exe" in result) == True:
            result = result.replace('\\th07.exe', '')
        if ("\\th075.exe" in result) == True:
            result = result.replace('\\th075.exe', '')
        if ("\\th08.exe" in result) == True:
            result = result.replace('\\th08.exe', '')
        if ("\\th09.exe" in result) == True:
            result = result.replace('\\th09.exe', '')
        if ("\\th095.exe" in result) == True:
            result = result.replace('\\th095.exe', '')
        if ("\\th10.exe" in result) == True:
            result = result.replace('\\th10.exe', '')
        if ("\\th105.exe" in result) == True:
            result = result.replace('\\th105.exe', '')
        if ("\\th11.exe" in result) == True:
            result = result.replace('\\th11.exe', '')
        if ("\\th12.exe" in result) == True:
            result = result.replace('\\th12.exe', '')
        if ("\\th123.exe" in result) == True:
            result = result.replace('\\th123.exe', '')
        if ("\\th125.exe" in result) == True:
            result = result.replace('\\th125.exe', '')
        if ("\\th128.exe" in result) == True:
            result = result.replace('\\th128.exe', '')
        if ("\\th13.exe" in result) == True:
            result = result.replace('\\th13.exe', '')
        if ("\\th135.exe" in result) == True:
            result = result.replace('\\th135.exe', '')
        if ("\\th14.exe" in result) == True:
            result = result.replace('\\th14.exe', '')
        if ("\\th143.exe" in result) == True:
            result = result.replace('\\th143.exe', '')
        if ("\\th145.exe" in result) == True:
            result = result.replace('\\th145.exe', '')
        if ("\\th15.exe" in result) == True:
            result = result.replace('\\th15.exe', '')
        if ("\\th155.exe" in result) == True:
            result = result.replace('\\th155.exe', '')
        if ("\\th16.exe" in result) == True:
            result = result.replace('\\th16.exe', '')
        if ("\\th165.exe" in result) == True:
            result = result.replace('\\th165.exe', '')
        if ("\\th17.exe" in result) == True:
            result = result.replace('\\th17.exe', '')
        if ("\\th175.exe" in result) == True:
            result = result.replace('\\th175.exe', '')
        if ("\\th18.exe" in result) == True:
            result = result.replace('\\th18.exe', '')
        if ("\\th19.exe" in result) == True:
            result = result.replace('\\th19.exe', '')
        launcher.destroy()
        print("アプリを開く：「" + result2 + "」、「" + result + "」の上で")
        subprocess.run(result2,shell=True,cwd=result)
        exit_py()

def launcher_widget():
    global launcher
    global gamelist
    global menu_language
    launcher = Tk()
    launcher.title("TouhouGameLauncher ver2.2.1")
    launcher.geometry("500x410")
    launcher.iconbitmap(default="icon.ico")
    launcherLabel = ttk.Label(launcher,text=messages[language][0][2],font=30)
    
    #存在するゲームの候補を出すListBox
    gamelist_var = StringVar(launcher,value=game_list)
    gamelist = Listbox(launcher,width=490,font=20,height=15,listvariable=gamelist_var)
    gamelist_var.set(game_list)
    
    game_exe = Button(launcher,text=messages[language][0][38],command=launch_game,font=20)
    custom_exe = Button(launcher,text=messages[language][0][39],command=launch_custom,font=20)
    list_update = Button(launcher,text=messages[language][0][40],command=reload,font=20)
    menubar = Menu(launcher)
    launcher.config(menu=menubar)
    
    menu_file = Menu(menubar,tearoff=0)
    menu_file.add_command(label=messages[language][0][27],command=settings)
    menu_file.add_separator()
    menu_file.add_command(label=messages[language][0][41],command=exit_py)
    menubar.add_cascade(label=messages[language][0][47],menu=menu_file)
    
    language_ob = []
    menu_language = Menu(menubar,tearoff=0)
    for i in range(len(languages)):
        language_ob.append(Gengo())
    for i in language_ob:
        i.setlang(languages[language_ob.index(i)])
        i.addCommand()
    menubar.add_cascade(label="languages",menu=menu_language)
    
    menu_help = Menu(menubar,tearoff=0)
    menu_help.add_command(label=messages[language][0][42],command=app_info)
    menu_help.add_separator()
    menu_help.add_command(label=messages[language][0][43],command=open_sorce)
    menu_help.add_command(label=messages[language][0][44],command=open_wiki)
    menu_help.add_command(label=messages[language][0][45],command=open_otoiawase)
    menubar.add_cascade(label=messages[language][0][46],menu=menu_help)
    
    gamelist.bind("<Button-3>",quick_launch)
    
    launcherLabel.pack()
    gamelist.pack()
    game_exe.pack(side=LEFT)
    custom_exe.pack(side=LEFT)
    list_update.pack(side=LEFT)
    
    launcher.update()
    launcher.lift()
    
    launcher.mainloop()

global app
app = True

launcher_widget()