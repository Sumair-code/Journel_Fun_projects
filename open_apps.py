import webbrowser
import os

def open_app(name):

    web_apps = {
        "youtube": "https://www.youtube.com", 
        "google": "https://www.google.com", 
        "github": "https://www.github.com",
        "leetcode": "https://www.leetcode.com"
    }

    for app in name:
        if app in web_apps:
            webbrowser.open(web_apps[app])
        elif(app == "vscode") or (app == "VS code") or (app == "vs code") or (app == "visual studio code"):
            os.system("code")
        elif(app == "calculator"):
            os.system("calc")
        elif app not in web_apps:
            try:
                os.system(app)
            except Exception as e:
                print("No app Found name...",app)
