import webbrowser
import requests
import urllib.parse

def Search(query):
    url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
    webbrowser.open(url)

query = "AI"

