# In The Name Of Allah
import pygame
import time
import requests
import random

FILE_SECCESSFUL = "suc.wav"
FILE_ERROR = "err.wav"
FILE_INFO = "info.wav"
AUTH_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IkE2MDk5NjE0MUU5MTJDMDhBRjQyMEFGMjUyNjI2N0Q5NkNGRjUyRjZSUzI1NiIsInR5cCI6ImF0K2p3dCIsIng1dCI6InBnbVdGQjZSTEFpdlFncnlVbUpuMld6X1V2WSJ9.eyJuYmYiOjE2ODk3ODk1NzIsImV4cCI6MTY4OTg3NTk3MiwiaXNzIjoiaHR0cDovL2lkZW50aXR5IiwiYXVkIjoiYXBpMSIsImNsaWVudF9pZCI6InJlLmNsaWVudCIsInN1YiI6IjM4YWYxYmExLWJjOWQtNGRhNy1hN2E2LTEyZTFiYmRlNjI4OSIsImF1dGhfdGltZSI6MTY4OTQ4ODU0NywiaWRwIjoibG9jYWwiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJtbW96ZmZhcnRpemFiaUBnbWFpbC5jb20iLCJlbWFpbCI6Im1tb3pmZmFydGl6YWJpQGdtYWlsLmNvbSIsInBob25lX251bWJlciI6IjA5MzA4NzcyMzQ3IiwicGhvbmVfbnVtYmVyX3ZlcmlmaWVkIjp0cnVlLCJpc19yZXNlbGxlciI6ZmFsc2UsInNhbGVzX2NoYW5uZWwiOiJCMkMiLCJ1c2VyX3VuaXF1ZV9udW1iZXIiOiIxMDExOTk0MzIiLCJqdGkiOiI0QTc2Q0NCNDlDRDU4MEEyNjY5NDI2MjlGNDBFMjBGNSIsImlhdCI6MTY4OTc4OTU3Miwic2NvcGUiOlsiYXBpMSIsIm9mZmxpbmVfYWNjZXNzIl0sImFtciI6WyJvdHAiXX0.p1Ze9FfdVBFo1XSGv6YSkOuw5FHXm9IbgnCFlrQDgNOiql2eZc3ZaKyD7umbS_UhenReN7sPhU6pjO7ZLx0ppbqMmFl7S3_7lnS8P8YlGKWaqbQc-zS2UHe4aW4yrSo2oIoF4JN7DFJDQtGsjtA8J3ZZhXMJSGYuhYhgcHR3475wjriloovk4qVmoTnJfCQF9V7qQuB0iegHMnqPDoQDctYUwVKV9RF32KrewWsm7cizK7kHhtZqS6PKfLPwbTec22nsf2NDLemldvdRby6in7UlV2iApOpbcR-wgZQf9ZMh3VyiX6RJOFmdoMEZcrNC31cfIVkzGok8i22Yoldv8Q"
URL_CHEAPSET = "https://ws.alibaba.ir/api/v2/flights/domestic/available/cheapest"
DATA_SENDED = {
  "referenceDate":"2023-07-20T10:31:16.654Z",
  "forwardDay": 15,
  "backwardDay": 0,
  "origin": "THR",
  "destination": "MHD"
}
DATE_I_WANNA = "2023-07-24"

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
            print(response.headers.get("Retry-After", "-1"))
            print("IP Banned!")
            lazy_exit()
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    try:
        pygame.mixer.init()
        while True:
            response_dict = send_post_request()
            if response_dict:
                response_dict = response_dict["result"]
                for dict in response_dict:
                    req_date = dict["departureDateTime"].split('T')[0]
                    if req_date == DATE_I_WANNA and dict["adultPrice"]:
                        play_wav_file(FILE_SECCESSFUL)
                        print(dict)
                        lazy_exit()
                    elif req_date == DATE_I_WANNA:
                        play_wav_file(FILE_INFO)
                        break
            else:
                play_wav_file(FILE_ERROR)
                print("Failed to get a valid response.")
            delay = random.randint(10, 20)
            print(f"Next request will be sent in {delay} seconds...")
            time.sleep(delay)
    except KeyboardInterrupt as ex:
        print("PLZ Wait ..")
        lazy_exit()