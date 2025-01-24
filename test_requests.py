import requests


headers = {
    "User-Agent": "com.google.android.apps.youtube.vr.oculus/1.60.19 (Linux; U; Android 12L; eureka-user Build/SQ3A.220605.009.A1) gzip",
    "accept-language": "en-US,en",
    "Content-Type": "application/json",
    "X-Youtube-Client-Name": "28",
}
data = {
    "context": {
        "client": {
            "clientName": "ANDROID_VR",
            "clientVersion": "1.60.19",
            "deviceMake": "Oculus",
            "deviceModel": "Quest 3",
            "osName": "Android",
            "osVersion": "12L",
            "androidSdkVersion": "32",
        }
    },
    "videoId": "1yvBqasHLZs",
    "contentCheckOk": "true",
}

url = "https://www.youtube.com/youtubei/v1/player?prettyPrint=false"


res = requests.post(
    url, headers=headers, json=data, proxies=dict(https="http://127.0.0.1:8118")
)
_data = res.json()

stream_data = _data["streamingData"]

formats = []
if "formats" in stream_data.keys():
    formats.extend(stream_data["formats"])
if "adaptiveFormats" in stream_data.keys():
    formats.extend(stream_data["adaptiveFormats"])

bitrate = float("inf")
audio_url = None
file_size = 0

for format in formats:
    if format["mimeType"].startswith("audio"):
        if format["bitrate"] < bitrate:
            bitrate = format["bitrate"]
            audio_url = format["url"]
            file_size = int(format["contentLength"])


if audio_url is not None:
    base_headers = {"User-Agent": "Mozilla/5.0", "accept-language": "en-US,en"}
    downloaded = 0
    default_range_size = 1024 * 1024 * 9
    with open("sample1.webm", "wb") as f:
        while downloaded < file_size:
            stop_pos = min(downloaded + default_range_size, file_size) - 1

            response = requests.get(
                f"{audio_url}&range={downloaded}-{stop_pos}",
                headers=base_headers,
                proxies=dict(https="http://127.0.0.1:8118"),
            )
            for chunk in response.iter_content(chunk_size=1024 * 1024 * 9):
                if chunk:
                    f.write(chunk)

            downloaded += len(response.content)
