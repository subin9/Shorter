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
    pattern = r"{(.*?)}"
    few_shot="예시 1) 병원비가 1천만원이어도 1억원이어도 본인은 1백만원만 부담토록 하겠습니다.\n요약 1) {병원비가 얼마든지 본인은 1백만원만 부담토록 하겠습니다.}\n예시 2) 공동주택 및 마을발전소에 태양광 무상 설치로 1가구 1태양광 시대\n요약 2) {주택 및 마을발전소에 태양광 무상 설치}\n예시 3) 무한 개발, 무한 경쟁, 성장 중심의 체제를 공존의 체제로 전환해야 합니다.\n요약 3) {경쟁, 성장 위주의 체제를 공존의 체제로 만들어야 합니다.}\n예시 4) 병사 최저임금과 모병제를 통한 군 장병이 행복한 병영\n요약 4) {최저임금, 모병제로 병사 처우 개선}"
    answer = bard.get_answer(text + "라는 글을 " + str(length // 3 * 2) + "글자 내외로 요약하십시오. 세 개의 요약을 만드시오. 당신은 요약된 세 개의 결과를 \"중괄호 안에\" 들어있는 텍스트 형태로 대답할 것입니다. 올바르게 요약된 네 가지 예시는 다음과 같습니다.\n"+few_shot)[
        'content']
    answer = re.findall(pattern, answer)
    return [re.sub(r'[^A-Za-z0-9가-힣,!.? %]', '', answer[j]) + " (길이 : " + str(
        len(KorToBraille().korTranslate(answer[j]).strip()) - 1).zfill(3) + ")" for j in range(len(answer))][:3]


class Pdf:
    def __init__(self, path: str):
        self.korean = []
        self.braille = []
        self.images = []
        self.path = path
        doc = fitz.open(self.path)
        for page in doc:
            self.images.append(page.get_pixmap())
            for sentence in page.get_text().split("\n"):
                sentence = sentence.strip()
                temp = re.sub(r"[^가-힣.,!?0-9 ]", "", sentence).strip()
                b = KorToBraille().korTranslate(temp).strip()[:-1]
                self.korean.append([sentence, len(sentence)])
                self.braille.append([b, len(b)])
        self.korean = [i for i in self.korean if i[0]]
        self.braille = [i for i in self.braille if i[0]]
        self.images = [i for i in self.images if i]