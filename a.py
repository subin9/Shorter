import gradio as gr

# 선택지 세 가지
choices = ["옵션 1", "옵션 2", "옵션 3"]

# 선택지를 표시할 함수
def choose_option():
    choice = input("옵션을 선택하세요 (1, 2, 3): ")
    try:
        choice = int(choice)
        if 1 <= choice <= 3:
            return choices[choice - 1]
        else:
            return "잘못된 선택입니다."
    except ValueError:
        return "잘못된 선택입니다."

# Gradio 인터페이스 생성
iface = gr.Interface(fn=choose_option, inputs=None, outputs="text")

# 인터페이스 실행 (10번 반복)
iface.launch(share=False, repeat=True, loop_max=10)