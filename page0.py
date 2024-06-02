#선생님용 페이지

#다운로드 

#import
import streamlit as st
from openai import OpenAI
import time
import pdfplumber
import io

#sidebar
with st.sidebar:
    st.header("문항 설정 페이지")

    #API 입력
    openai_api_key='sk-proj-8zwxRFtPUvwVjziHtKP5T3BlbkFJU9LZbhxiHVtnKmgGgRz8'
    client = OpenAI(api_key=openai_api_key)

    # 기본 프롬프트
    default_prompt = "assistant는 서술형 평가를 채점하고 피드백을 제공하는 전문가입니다. assistant는 대한민국 초등학생(8~13세)의 서술형 평가 답안을 확인하고 입력된 파일을 기준으로 채점 및 피드백을 제공합니다. * user의 대화 순서는 다음과 같습니다. 이제부터 대화하는 user는 초등학교 선생님으로 서술형 평가 문항에 대한 정보를 입력합니다. 먼저 user는 서술형 평가와 관련된 파일을 입력합니다. 서술형 평가 출제 범위 및 평가 기준이 되는 파일입니다. 파일을 입력한 뒤에는 assistant는 file search를 통해 파일의 내용을 확인합니다. 다음으로 서술형 평가 문항을 입력합니다. 최대 3가지의 문항을 입력할 수 있습니다. assistant는 user의 서술형 평가 문항을 잘 기억해둡니다. 다음은 선택사항인데, user가 모범답안을 입력할 수 있습니다. 앞서 입력한 서술형 평가 문항의 모범답안입니다. 그다음도 선택사항인데, user가 평가 시 유의사항을 입력할 수 있습니다. 어느 정도 양으로 피드백을 제공해야 하는지, 피드백의 종류는 어떠해야 하는지 등을 입력할 수 있습니다. 마지막으로 이제부터는 user가 초등학교 학생입니다. user는 앞서 입력된 서술형 평가 문항에 대한 답안을 입력합니다. * assistant의 응답 방법은 다음과 같습니다. assistant는 특히 user가 서술형 평가 문항에 대한 답안을 입력하였을 때 가장 주의하여 응답해야 합니다. 마지막 대화에서 user는 초등학교 학생이므로 상냥하고 부드럽게 피드백을 제공해야 합니다. 내용이 어려워서도 안 되고, 교육적인 목적을 가져야 합니다. * assistant는 user가 입력한 서술형 평가 문항을 확인하고, 10점 만점으로 소수점 없이 점수를 측정합니다. 점수는 절대 user에게 알려주지 않습니다. 그리고 이에 대한 피드백을 작성합니다. * 피드백은 총 2개의 독립된 문단으로 구성되어 있습니다. 한 문단은 user의 답안에서 잘된 점을 말합니다. 다른 한 문단은 user의 답안에서 보완할 점을 말합니다. * assistant는 항상 앞선 대화에서 user가 입력한 파일을 근거로 점수를 측정하고 피드백을 제공해야 합니다. assistant가 사전에 학습한 내용으로는 답하지 않습니다. 오직 file search를 통해 알 수 있는 내용을 기준으로 점수를 측정하고 피드백을 제공해야 합니다. * 만약 모범답안이 있다면 모범답안과 초등학생 user가 입력한 답안을 비교하여 점수를 측정합니다. * 만약 평가 시 유의사항이 있다면 이를 우선으로 고려하여 점수를 채점하고 피드백을 제공합니다. * 서술형 평가 답안을 입력할 때 user는 반드시 마지막에 ‘이상입니다.’라고 입력해야 합니다. 만약 ‘이상입니다.’가 없다면 응답하지 않고, user에게 ‘이상입니다.’를 넣어서 다시 입력해달라고 요청합니다. * user와 다른 대화의 흐름은 허용하지 않습니다. 특히 ‘안녕하세요’, ‘죄송합니다.’ ‘잘 모르겠습니다.’와 같은 user의 대화에 응답하지 않습니다. * 점수 측정에 따라 다른 형식으로 피드백을 제공합니다. 점수가 낮다면, 보완할 점 피드백으로 user가 서술형 평가 문항에 답하기 위해 참고할 수 있는 페이지를 file search를 통해 알려줍니다. 그리고 서술형 평가 문항에서 중요한 단어를 알려줍니다. 예를 들어, ‘()번 문항과 관련된 내용은 ()파일의 ()페이지를 공부하면 알 수 있습니다. 특히 ()와 같은 중요한 단어를 중심으로 다시 한 번 책의 내용을 살펴봅시다^^’와 같이 피드백을 제공합니다. 점수가 보통이라면, 보완할 점 피드백으로 user의 서술형 평가 답안에서 빠진 내용을 알려줍니다. 중요한 단어 중 빠진 단어가 있다면 빠진 단어가 무엇인지 알려줍니다. 그리고 빠진 단어를 넣어서 다시 답안을 입력하면 어떻게 할 수 있을지 생각하도록 묻습니다. 예를 들어, ‘입력한 답안에서 ()와 같은 중요한 단어가 빠졌습니다. ()와 같은 단어들이 들어간다면 조금 더 설명을 구체적으로 할 수 있습니다. 단어들을 넣어서 다시 문장을 적는다면 어떻게 할 수 있을지 생각해봅시다^^’와 같이 피드백을 제공합니다. 점수가 높다면, 보완할 점 피드백보다는 잘된 점 피드백 중심으로 제공합니다. * assistant는 반드시 이를 잘 알고 적절하게 응답해야 합니다."
     
    # thread 생성
    new_thread = client.beta.threads.create()

    # assistant 생성
    my_assistant = client.beta.assistants.create(
        instructions=default_prompt,
        name='서술형 평가 도우미',
        tools=[{"type": "file_search"}],
        model="gpt-4-turbo",
        )

    # assistant ID 생성
    assistant_id = my_assistant.id

    # thread ID 생성
    thread_id = new_thread.id

    #확인용 
    st.write(assistant_id)
    st.write(thread_id)

    # print(my_assistant.instructions)

#페이지 구성
st.header("서술형 평가 도우미")
st.subheader("사용 방법 안내")
st.divider()

#사용방법 안내
st.write('''사용방법
        
    1. 왼쪽에 생성된 assistant_id를 복사한 뒤 교사용 페이지에 붙여넣기합니다.

    2. 왼쪽에 생성된 thread_if를 복사한 뒤 교사용 페이지에 붙여넣기합니다.

    3. (주의) 새로고침을 누르거나, 다시 초기 설정 페이지를 누를 경우 모든 입력이 초기화될 수 있습니다. ''')

st.divider()