import requests
import json

def get(videoId):
    album_id = ""
    url = "https://music.youtube.com/youtubei/v1/next?key=AIzaSyC9XL3ZjWddXya6X74dJoCTL-WEYFDNX30&prettyPrint=false"

    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0', 'accept': '*/*', 'accept-encoding': 'gzip, deflate', 'content-type': 'application/json', 'content-encoding': 'gzip', 'origin': 'https://music.youtube.com', 'X-Goog-Visitor-Id': 'CgtRS2Z5eHl5bWxJRSjo7YuZBg%3D%3D'}

    params = {
        "videoId": videoId,
        "context": {
            "client": {
                "clientName": "WEB_REMIX",
                "clientVersion": "1.20220907.01.00",
            }
        }
    }
    cookies = {'CONSENT': 'YES+1'}


    response = requests.post(url = url,
                            json=params,
                            headers=headers,
                            cookies=cookies)

    response_json = json.loads(response.text)

    menu = response_json["contents"]\
                           ["singleColumnMusicWatchNextResultsRenderer"]\
                           ["tabbedRenderer"]\
                           ["watchNextTabbedResultsRenderer"]\
                           ["tabs"][0]\
                           ["tabRenderer"]\
                           ["content"]\
                           [ "musicQueueRenderer"]\
                           [ "content"]\
                           ["playlistPanelRenderer"]\
                           ["contents"][0]\
                           ["playlistPanelVideoRenderer"]\
                           ["menu"]\
                           ["menuRenderer"]\
                           ["items"]

    for i in menu:
        try:
            if i["menuNavigationItemRenderer"]\
                ["icon"]\
                ["iconType"] == "ALBUM":
                album_id = i["menuNavigationItemRenderer"]\
                           ["navigationEndpoint"]\
                           ["browseEndpoint"]\
                           ["browseId"]
        except: pass

    return album_id





if __name__ == "__main__":
    print(get("hqVVMJxeBMc"))
    print(get("Xsj_fqOTs5U"))
    print(get("8gqcVAdbepE"))




































