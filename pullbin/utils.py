import re, os, requests, json

# TODO: improve extesion detection
def parse_extension(ext):
    download_languages()
    return getID(ext)

def download_languages():
    if not os.path.exists(".languages") or not os.stat(".languages").st_size: # not exist or is empty
        request = requests.get("https://ghostbin.co/languages.json", stream=True)
        with open(".languages", 'wb') as file:
            for chunk in request.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
                    file.flush()

def getID(language):
    json_data = json.load(open(".languages", "rb"))
    for index in range(len(json_data)):
        for lang in json_data[index]['languages']:
            if lang['name'].lower() == language.lower():
                return lang['id']

    return 'txt'