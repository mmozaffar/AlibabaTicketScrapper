# In The Name Of Allah
import pygame
import time
import requests
import random
import datetime

FILE_SECCESSFUL = "suc.wav"
FILE_ERROR = "err.wav"
FILE_INFO = "info.wav"
AUTH_TOKEN = ""
URL_CHEAPSET = "https://ws.alibaba.ir/api/v2/flights/domestic/available/cheapest"
DATE_I_WANNA = "2023-07-24"
DATA_SENDED = {
  "referenceDate":DATE_I_WANNA+"T10:56:10.118Z",
  "forwardDay": 0,
  "backwardDay": 0,
  "origin": "THR",
  "destination": "MHD"
}
TIME_AFTER = datetime.datetime.strptime("12:00:00", "%H:%M:%S").time()

def lazy_exit():
    pygame.mixer.quit()
    exit()

def play_wav_file(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

def send_post_request(url=URL_CHEAPSET, data=DATA_SENDED, auth_token=AUTH_TOKEN):
    try:
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json",
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 429:
            play_wav_file(FILE_ERROR)
            print("IP Banned! Plz go to alibaba.ir")
            lazy_exit()
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
    

def send_get_request(url, auth_token=AUTH_TOKEN):
    try:
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json",
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 429:
            play_wav_file(FILE_ERROR)
            print("IP Banned! Plz go to alibaba.ir")
            lazy_exit()
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    try:
        pygame.mixer.init()
        rep = 0
        while True:
            response_dict = send_post_request()
            if response_dict:
                response_dict = response_dict["result"][0]
                if response_dict["adultPrice"]:
                    reqId = send_post_request(
                        url="https://ws.alibaba.ir/api/v1/flights/domestic/available",
                        data={
                            "origin": "THR",
                            "destination": "MHD",
                            "departureDate": DATE_I_WANNA,
                            "adult": 1,
                            "child": 0,
                            "infant": 0
                        }
                    )["result"]["requestId"]
                    cmp_res = send_get_request(
                        url="https://ws.alibaba.ir/api/v1/flights/domestic/available/"+reqId
                    )["result"]["departing"]
                    for res in cmp_res:
                        lev_dt = res["leaveDateTime"].split("T")[1]
                        sts = res["status"]
                        time_object = datetime.datetime.strptime(lev_dt, "%H:%M:%S").time()
                        if time_object > TIME_AFTER and sts != "C":
                            play_wav_file(FILE_SECCESSFUL)
                            print(res)
                            lazy_exit()
            else:
                play_wav_file(FILE_ERROR)
                print("Failed to get a valid response.")
            delay = random.randint(20, 30)
            rep += 1
            print(f"Next {rep} request will be sent in {delay} seconds...")
            time.sleep(delay)
    except KeyboardInterrupt as ex:
        print("PLZ Wait ..")
        lazy_exit()
