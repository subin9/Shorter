from utils import *
import argparse
from PIL import Image
import io
from pywebio.input import *
from pywebio.output import *


def main():
    parser = argparse.ArgumentParser(description='Demo code for executing ⠠⠨⠂⠃⠈⠝')
    parser.add_argument('--path', help='요약할 pdf 파일 경로')
    parser.add_argument('--psid', help='Bard 실행 후 F12->application->Cookies에서 __Secure-1PSID 값')  # 필요한 인수를 추가
    parser.add_argument('--audible')
    args = parser.parse_args()

    pages = Pdf(args.path)
    put_markdown("# ⠨⠂⠃⠈⠝ : 선거 공보물, 점자로 쉽고, 짧게 번역하기")
    put_markdown("<br/>")
    put_markdown("### 진행 상황")
    put_progressbar('Progress')
    put_markdown("<br/>")
    put_markdown("___")
    ts = pages.korean
    bs = pages.braille
    images = pages.images
    deletion=[]
    for i in range(len(ts)):
        if not re.sub(r'[^A-Za-z0-9가-힣,!.? %]', '', ts[i][0]):
            deletion.append(i)

    ts=[ts[i] for i in range(len(ts)) if i not in deletion]
    bs=[bs[i] for i in range(len(bs)) if i not in deletion]
    imgs=[]
    for i in range(len(images)):
        img = Image.frombytes("RGB", [images[i].width, images[i].height], images[i].samples)
        imgs.append(img)
    contents = [put_image(src=imgs[i]) for i in range(len(imgs))]
    original_bs = '\n'.join([i[0] for i in bs])
    shorten_kr = ""
    shorten_bs = ""
    cnt = 0
    next = None
    for cnt in range(len(ts)):
        set_progressbar('Progress', cnt / len(ts))

        if next:
            ts[cnt - 1][0] = "삭제됨"
            ts[cnt][0] = next + ts[cnt][0]
            next = None

        b_len = len(KorToBraille().korTranslate(ts[cnt][0]).strip()[:-1])

        with use_scope('first', clear=True):
            put_markdown(
                "**\"" + re.sub(r'[^A-Za-z0-9가-힣,!.? %]', '', ts[cnt][0]) + "\" 라는 문장을 어떤 문장으로 요약해드릴까요? (점자 길이 : " + str(
                    b_len) + ", 목표 길이 : " + str(b_len // 3 * 2) + ")**")
            put_markdown("<br/>")
            put_button("원본 확인하기", onclick=lambda: popup('사진 보기', contents), color='success', outline=True)
            put_markdown("<br/>")
            put_markdown("앞, 뒤 문장은 다음과 같습니다.")

            temp = ts[max(cnt - 3, 0):min(len(ts), cnt + 4)]
            for i in range(len(temp)):
                if cnt < 3:
                    if i == cnt:
                        put_markdown("> **> " + re.sub(r'[^A-Za-z0-9가-힣,!.? %]', '', temp[i][0]) + "**")
                    else:
                        put_markdown("> " + re.sub(r'[^A-Za-z0-9가-힣,!.? %]', '', temp[i][0]))
                elif cnt < len(ts) - 3:
                    if i == 3:
                        put_markdown("> **>" + re.sub(r'[^A-Za-z0-9가-힣,!.? %]', '', temp[i][0]) + "**")
                    else:
                        put_markdown("> " + re.sub(r'[^A-Za-z0-9가-힣,!.? %]', '', temp[i][0]))
                else:
                    if i == len(temp) - cnt:
                        put_markdown("> **>" + re.sub(r'[^A-Za-z0-9가-힣,!.? %]', '', temp[i][0]) + "**")
                    else:
                        put_markdown("> " + re.sub(r'[^A-Za-z0-9가-힣,!.? %]', '', temp[i][0]))
            put_markdown("___")

            sel1=radio("이 문장을 어떻게 할까요?" , ["요약할게요.", "그대로 점역할게요.", "다음 문장과 함께 점역할게요.", "이 문장은 뺄게요.", "직접 변경할래요."])
            if sel1 == "그대로 점역할게요.":
                shorten_kr += ts[cnt][0] + "\n"
                shorten_bs += KorToBraille().korTranslate(ts[cnt][0]).strip()[:-10] + "\n"
            elif sel1 == "이 문장은 뺄게요.":
                ts[cnt][0] = "삭제됨"
                pass
            elif sel1 == "다음 문장과 함께 점역할게요.":
                next = ts[cnt][0] + " "
            elif sel1 == "직접 변경할래요.":
                put_markdown("* **원래 문장 : \"" + ts[cnt][0] + "\" (길이 : " + str(b_len) + ")**")
                done = input("변경 사항을 입력해주세요.")
                shorten_kr += done + "\n"
                shorten_bs += KorToBraille().korTranslate(done).strip()[:-1] + "\n"
                ts[cnt][0] = done
            else:
                outputs = get_alternatives(ts[cnt][0], len(ts[cnt][0]), args.psid.strip())
                sel2 = radio("요약된 문장을 선택해주세요.", outputs+["그대로 점역할게요."])
                try:
                    if sel2 == outputs[0]:
                        shorten_kr += outputs[0] + "\n"
                        shorten_bs += KorToBraille().korTranslate(outputs[0]).strip()[:-10] + "\n"
                        ts[cnt][0]=outputs[0][:-10]
                    elif sel2 == outputs[1]:
                        shorten_kr += outputs[1] + "\n"
                        shorten_bs += KorToBraille().korTranslate(outputs[1]).strip()[:-10] + "\n"
                        ts[cnt][0] = outputs[1][:-10]
                    elif sel2 == outputs[2]:
                        shorten_kr += outputs[2] + "\n"
                        shorten_bs += KorToBraille().korTranslate(outputs[2]).strip()[:-10] + "\n"
                        ts[cnt][0] = outputs[2][:-10]
                    elif sel2 == "그대로 점역할게요.":
                        shorten_kr += ts[cnt][0] + "\n"
                        shorten_bs += KorToBraille().korTranslate(ts[cnt][0]).strip()[:-10] + "\n"
                except:
                    put_markdown("마땅한 요약 문장이 없어요. 그대로 점역할게요.")
                    shorten_kr += ts[cnt][0] + "\n"
                    shorten_bs += KorToBraille().korTranslate(ts[cnt][0]).strip()[:-10] + "\n"

            cnt += 1

    with use_scope('second', clear=True):
        set_progressbar('Progress', cnt / cnt)
        with open("result.txt", "w", encoding="utf-8") as f:
            f.write(shorten_kr)
        with open("result_braille.txt", "w", encoding="utf-8") as f:
            f.write(shorten_bs)
        put_markdown("# 요약 결과")
        put_markdown("* **기존 공약본은 " + str(len(original_bs)) + "글자, 요약본은 " + str(len(shorten_bs)) + "글자입니다.**")
        result = open('result.txt', 'rb').read()
        result_braille = open('result_braille.txt', 'rb').read()
        put_markdown("# 원본 공약본 파일")
        put_file("원본 공약본.txt", result)
        put_markdown("# 요약본 파일")
        put_file("요약본.txt", result_braille)


if __name__ == "__main__":
    main()