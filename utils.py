from bardapi import Bard
import os
import re
import requests
from KorToBraille.KorToBraille import KorToBraille
import fitz


def get_alternatives(text: str, length:int, token: str) -> list:
    os.environ['_BARD_API_KEY'] = token
    token = token
    session = requests.Session()
    session.headers = {
        "Host": "bard.google.com",
        "X-Same-Domain": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Origin": "https://bard.google.com",
        "Referer": "https://bard.google.com/",
    }
    session.cookies.set("__Secure-1PSID", os.getenv("_BARD_API_KEY"))
    # session.cookies.set("__Secure-1PSID", token)

    bard = Bard(token=token, session=session, timeout=30)
    text = "\"" + text + "\""
    answer = bard.get_answer(text + "라는 문장을 " + str(length // 3 * 2) + "글자 내외의 문장으로 짧게 요약해줘. 요약할 때, 말투는 그대로 남겨줘. 3개 정도 알려주고, 대답할 때는 요약한 문장만 말해줘.")[
        'content'].split("**")
    return [re.sub(r'[^A-Za-z0-9가-힣,!.? %]', '', answer[j]) + " (길이 : " + str(
        len(KorToBraille().korTranslate(answer[j]).strip()) - 1) + ")" for j in range(len(answer)) if j % 2][:3]


class Text:
    def __init__(self, path: str):
        self.korean = []
        self.braille = []
        self.path = path
        doc = fitz.open(self.path)
        for page in doc:
            for sentence in page.get_text().split("\n"):
                sentence = sentence.strip()
                temp = re.sub(r"[^가-힣.,!?0-9 ]", "", sentence).strip()
                b = KorToBraille().korTranslate(temp).strip()[:-1]
                self.korean.append([sentence, len(sentence)])
                self.braille.append([b, len(b)])
        self.korean = [i for i in self.korean if i[0]]
        self.braille = [i for i in self.braille if i[0]]
