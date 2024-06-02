# 학생용 페이지

# 라이브러리
import streamlit as st
from openai import OpenAI
import time
import pdfplumber
import io

# 기본 API
openai_api_key='sk-proj-8zwxRFtPUvwVjziHtKP5T3BlbkFJU9LZbhxiHVtnKmgGgRz8'
client = OpenAI(api_key=openai_api_key)

# 입력된 assistant, thread ID
assistant_id = st.text_input('assistant')
thread_id = st.text_input('thread')

# sidebar
with st.sidebar:
    st.header("답안 작성 페이지")

# 페이지 구성
st.header("서술형 평가 도우미")
st.subheader("답안 작성 페이지")
st.divider()

# 사용방법 안내
st.write('''사용방법
         
    1. 문항을 잘 읽고 답안을 작성합니다.

    2. 문항과 관련 없는 내용을 적을 경우 응답하지 않습니다.  
    예를 들어, '죄송합니다.', '잘 모르겠습니다.' 등의 내용에는 응답하지 않습니다.

    3. 답안 맨 마지막은 항상 '이상입니다.'로 끝마칩니다.

    4. 모든 문항에 답안을 작성한 뒤 맨 아래 <제출> 버튼을 누르면 답안이 제출됩니다.''')

st.divider()

# 답안 작성하기 

# # 제출 버튼 생성 
# submit = st.button("답안 제출하기")

if assistant_id is not None and thread_id is not None:

    # 1번 문항 답안 작성
    st.caption('1번 문항')

    thread_message = client.beta.threads.messages.create(
    thread_id,
    role="user",
    content='입력한 1번 문항이 무엇인지 보여줘. 앞 뒤에 아무 말도 붙이지 않고, 그냥 입력한 문항만 그대로 보여줘. 만약에 없다면, 1번 문항은 없습니다. 라고 말해줘.',
    )

    run = client.beta.threads.runs.create(
    thread_id=thread_id,
    assistant_id=assistant_id
    )
    run_id = run.id

    while True:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
            )   
        if run.status == "completed":
            break
        else:
            time.sleep(2)

    thread_messages = client.beta.threads.messages.list(thread_id)
    msg = thread_messages.data[0].content[0].text.value
    st.write(msg)

    answer1 = st.text_area("1번 문항 답안")

    st.divider()

    # 2번 문항 답안 작성
    st.caption('2번 문항')

    thread_message = client.beta.threads.messages.create(
    thread_id,
    role="user",
    content='입력한 2번 문항이 무엇인지 보여줘. 앞 뒤에 아무 말도 붙이지 않고, 그냥 입력한 문항만 그대로 보여줘. 만약에 없다면, 2번 문항은 없습니다. 라고 말해줘.',
    )

    run = client.beta.threads.runs.create(
    thread_id=thread_id,
    assistant_id=assistant_id
    )
    run_id = run.id

    while True:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
            )   
        if run.status == "completed":
            break
        else:
            time.sleep(2)

    thread_messages = client.beta.threads.messages.list(thread_id)
    msg = thread_messages.data[0].content[0].text.value
    st.write(msg)

    answer2 = st.text_area("2번 문항 답안")

    st.divider()

    # 3번 문항 답안 작성
    st.caption('3번 문항')

    thread_message = client.beta.threads.messages.create(
    thread_id,
    role="user",
    content='입력한 3번 문항이 무엇인지 보여줘. 앞 뒤에 아무 말도 붙이지 않고, 그냥 입력한 문항만 그대로 보여줘. 만약에 없다면, 3번 문항은 업습니다. 라고 말해줘.',
    )

    run = client.beta.threads.runs.create(
    thread_id=thread_id,
    assistant_id=assistant_id
    )
    run_id = run.id

    while True:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
            )   
        if run.status == "completed":
            break
        else:
            time.sleep(2)

    thread_messages = client.beta.threads.messages.list(thread_id)
    msg = thread_messages.data[0].content[0].text.value
    st.write(msg)

    answer3 = st.text_area("3번 문항 답안")

    st.divider()

    # 점수 및 피드백 작성
    st.subheader('점수 및 피드백')

    submit = st.button("답안 제출하기")
    if submit:
        #1번 문항
        st.caption('1번 문항')
        thread_message = client.beta.threads.messages.create(
        thread_id,
        role="user",
        content=answer1,
        )

        run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
        )
        run_id = run.id

        while True:
            run = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run_id
                )   
            if run.status == "completed":
                break
            else:
                time.sleep(2)
            # print(run)
            # st.write(run)

        thread_messages = client.beta.threads.messages.list(thread_id)
        # print(thread_messages.data)
        # st.write(thread_messages.data)

        msg = thread_messages.data[0].content[0].text.value
        st.write(msg)

        st.divider()

        #2번 문항 점수 및 피드백
        st.caption('2번 문항')
        thread_message = client.beta.threads.messages.create(
        thread_id,
        role="user",
        content=answer2,
        )

        run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
        )
        run_id = run.id

        while True:
            run = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run_id
                )   
            if run.status == "completed":
                break
            else:
                time.sleep(2)
            # print(run)
            # st.write(run)

        thread_messages = client.beta.threads.messages.list(thread_id)
        # print(thread_messages.data)
        # st.write(thread_messages.data)

        msg = thread_messages.data[0].content[0].text.value
        st.write(msg)

        st.divider()

        #3번 문항 점수 및 피드백
        st.caption('3번 문항')
        thread_message = client.beta.threads.messages.create(
        thread_id,
        role="user",
        content=answer3,
        )

        run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
        )
        run_id = run.id

        while True:
            run = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run_id
                )   
            if run.status == "completed":
                break
            else:
                time.sleep(2)
            # print(run)
            # st.write(run)

        thread_messages = client.beta.threads.messages.list(thread_id)
        # print(thread_messages.data)
        # st.write(thread_messages.data)

        msg = thread_messages.data[0].content[0].text.value
        st.write(msg)
