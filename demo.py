import gradio as gr
from utils import *
import argparse
import numpy as np
import gradio as gr
from pywebio.input import *
from pywebio.output import *


def main():
    parser = argparse.ArgumentParser(description='Demo code for executing ⠠⠨⠂⠃⠈⠝')
    parser.add_argument('--pdf_path', help='요약할 pdf 파일 경로')
    parser.add_argument('--bard_token', help='Bard 실행 후 F12->application->Cookies에서 __Secure-1PSID 값')  # 필요한 인수를 추가
    parser.add_argument('--audible')
    args = parser.parse_args()

    texts = Text(args.pdf_path)
    put_markdown("# ⠨⠂⠃⠈⠝ : 선거 공보물, 점자로 짧게 바꿔보세요.")
    put_markdown("### 진행 상황")
    put_progressbar('Progress')
    put_markdown("___")
    ts=texts.korean[200:202]
    bs=texts.braille

    original_bs='\n'.join([i[0] for i in bs])
    shorten_kr=""
    shorten_bs=""
    cnt=0
    for text,length in ts:
        set_progressbar('Progress', cnt / len(ts))
        b_len=len(KorToBraille().korTranslate(text).strip()[:-1])
        with use_scope('first', clear=True):
            put_markdown("* **\""+text + "\" 라는 문장을 어떤 문장으로 요약해드릴까요? (점자 길이 : " + str(b_len) + ", 목표 길이 : " + str(b_len // 3 * 2) + ")**")
            put_markdown("* 앞, 뒤 문장은 다음과 같습니다.")
            put_markdown("* > "+'\n'.join([i[0] for i in ts[max(cnt - 5, 0):min(len(ts), cnt + 5)]]))
            outputs = get_alternatives(text, len(text), args.bard_token.strip())
            sel=radio("요약된 문장을 선택해주세요.", outputs+["그대로 점역할게요.", "이 문장은 뺄게요.","직접 변경할래요."])
            if sel==outputs[0]:
                shorten_kr+=outputs[0]+"\n"
                shorten_bs+=KorToBraille().korTranslate(outputs[0]).strip()[:-1]+"\n"
            elif sel==outputs[1]:
                shorten_kr+=outputs[1]+"\n"
                shorten_bs+=KorToBraille().korTranslate(outputs[1]).strip()[:-1]+"\n"
            elif sel==outputs[2]:
                shorten_kr+=outputs[2]+"\n"
                shorten_bs+=KorToBraille().korTranslate(outputs[2]).strip()[:-1]+"\n"
            elif sel=="그대로 점역할게요.":
                shorten_kr+=text+"\n"
                shorten_bs+=KorToBraille().korTranslate(text).strip()[:-1]+"\n"
            elif sel=="이 문장은 뺄게요.":
                pass
            else:
                put_markdown("* **원래 문장 : \"" + text + "\" (길이 : " + str(b_len) +")**")
                done=input("변경 사항을 입력해주세요.")
                shorten_kr+=done+"\n"
                shorten_bs+=KorToBraille().korTranslate(done).strip()[:-1]+"\n"
            cnt+=1
    with open("result.txt","w",encoding="utf-8") as f:
        f.write(shorten_kr)
    with open("result_braille.txt","w",encoding="utf-8") as f:
        f.write(shorten_bs)
    put_markdown("# 요약 결과")
    put_markdown("* **기존 공약본은 "+str(len(original_bs))+"글자, 요약본은 "+str(len(shorten_bs))+"글자입니다.**")
    result = open('result.txt', 'rb').read()
    result_braille = open('result_braille.txt', 'rb').read()
    put_markdown("# 원본 공약본 파일")
    put_file("원본 공약본",result)
    put_markdown("# 요약본 파일")
    put_file("요약본",result_braille)


if __name__ == "__main__":
    main()