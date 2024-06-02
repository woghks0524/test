#선생님용 페이지

#import
import streamlit as st
from openai import OpenAI
import time
import pdfplumber
import io

#sidebar
with st.sidebar:
    st.header("문항 설정 페이지")

# #기본 id
# # assistant_id='asst_0I9lgAwdlCZ4JtTW5gdIjNgP'
openai_api_key='sk-proj-8zwxRFtPUvwVjziHtKP5T3BlbkFJU9LZbhxiHVtnKmgGgRz8'
client = OpenAI(api_key=openai_api_key)
# # thread_id = 'thread_sfC5BmSfvOnTTUv1fda2tcwN'

# # 기본 프롬프트
# default_prompt = "assistant는 보조하는 역할이고, 주어진 프롬프트에 따라 명령대로 수행해야 한다. assistant는 서술형 문항에 대한 user의 답안을 확인하고 점수 및 피드백을 제공하는 역할이다."

# # thread 생성
# new_thread = client.beta.threads.create()

# # assistant 생성
# my_assistant = client.beta.assistants.create(
#     instructions=default_prompt,
#     name='서술형 평가 도우미',
#     tools=[{"type": "file_search"}],
#     model="gpt-4-turbo",
#     )

# # assistant ID 생성
# assistant_id = my_assistant.id

# # thread ID 생성
# thread_id = new_thread.id

# 입력된 assistant, thread ID
assistant_id = st.text_input('assistant')
thread_id = st.text_input('thread')

# print(my_assistant.instructions)

#페이지 구성
st.header("서술형 평가 도우미")
st.subheader("문항 설정 페이지")
st.divider()

#사용방법 안내
st.write('''사용방법
         
    1. 서술형 평가 범위에 해당하는 교과서 pdf 파일을 입력하세요.

    2. 서술형 평가 문항을 입력하세요. 최대 3문항까지 입력할 수 있습니다.

    3. (선택사항)모범답안을 입력하세요.

    4. (선택사항)답안 점수 및 피드백 제공 시 참고할 점을 적어주세요.''')

st.divider()

#1번 교과서 파일 입력 안내
st.subheader('1. 교과서 파일 입력')
st.caption('200mb 크기 이내(약 20쪽)의 pdf 파일을 입력하세요.')

# 파일 업로더 입력
uploaded_file = st.file_uploader("")

# 파일이 선택되어 있고 업로드 버튼을 누르면 파일 업로드 
run_file_button = st.button('파일 업로드') 

if uploaded_file is not None and run_file_button:
    uploaded_file_response = client.files.create(
    file=uploaded_file,
    purpose="fine-tune"
    )

#vector stores를 생성하는 과정    
    vector_store = client.beta.vector_stores.create(
    name=thread_id
    )

#생성된 파일 id를 vector stores에 입력하는 과정
    vector_store_file = client.beta.vector_stores.files.create(
    vector_store_id=vector_store.id,
    file_id=uploaded_file_response.id
    )

# assistant에 파일 업로드 하도록 수정하기
    my_updated_assistant = client.beta.assistants.update(
    assistant_id,
    tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}}  
    )

    st.success(f'파일이 성공적으로 등록되었습니다.')

st.divider()

#2번 평가 문항 입력 안내
st.subheader('2. 서술형 평가 문항 입력')
st.caption('최대 3문항까지 입력할 수 있습니다.')

question1 = st.text_area("1번 문항")
# thread_message = client.beta.threads.messages.create(
#     thread_id,
#     role="user",
#     content='1번 문항은 <' + question1 + '> 입니다.',
#     )

question2 = st.text_area("2번 문항")
# thread_message = client.beta.threads.messages.create(
#     thread_id,
#     role="user",
#     content='2번 문항은 <' + question2 + '> 입니다.',
#     )

question3 = st.text_area("3번 문항")
# thread_message = client.beta.threads.messages.create(
#     thread_id,
#     role="user",
#     content='3번 문항은 <' + question3 + '> 입니다.',
#     )

# thread_message = client.beta.threads.messages.create(
#     thread_id,
#     role="user",
#     content='1번 문항은 <' + question1 + '> 입니다.' '2번 문항은 <' + question2 + '> 입니다.' '3번 문항은 <' + question3 + '> 입니다.' ,
#     )

run_button = st.button('문항 입력')

if run_button:
    thread_message = client.beta.threads.messages.create(
    thread_id,
    role="user",
    content='1번 문항은 <' + question1 + '> 입니다.' '2번 문항은 <' + question2 + '> 입니다.' '3번 문항은 <' + question3 + '> 입니다.' ,
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

# 문항 입력이 완료 되었다는 문구 생성
    st.success('문항 입력이 완료되었습니다.')

st.divider()

#3번 모범답안 입력 안내 
st.subheader('(선택)3.모범답안 입력')
st.caption('모범답안을 입력하지 않으면 모델이 스스로 모범답안을 작성하여 평가에 활용합니다.')

sample_answer1 = st.text_area("1번 모범답안")
# thread_message = client.beta.threads.messages.create(
#     thread_id,
#     role="user",
#     content='1번 모범답안은 <' + sample_answer1 + '> 입니다.',
#     )

sample_answer2 = st.text_area("2번 모범답안")
# thread_message = client.beta.threads.messages.create(
#     thread_id,
#     role="user",
#     content='2번 모범답안은 <' + sample_answer2 + '> 입니다.',
#     )

sample_answer3 = st.text_area("3번 모범답안")
# thread_message = client.beta.threads.messages.create(
#     thread_id,
#     role="user",
#     content='3번 모범답안은 <' + sample_answer3 + '> 입니다.',
#     )

run_button = st.button('모범답안 입력')

if run_button:
    thread_message = client.beta.threads.messages.create(
        thread_id,
        role="user",
        content='1번 모범답안은 <' + sample_answer1 + '> 입니다.' '2번 모범답안은 <' + sample_answer2 + '> 입니다.' '3번 모범답안은 <' + sample_answer3 + '> 입니다.',
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

# 문항 입력이 완료 되었다는 문구 생성
    st.success('모범답안 입력이 완료되었습니다.')

st.divider()

#4번 고려할 점 입력 안내 
st.subheader('(선택)4.평가 시 참고할 점 입력')
st.caption('(예시를 입력할 계획입니다.)')

consider_points = st.text_area("평가 시 참고할 점")
# thread_message = client.beta.threads.messages.create(
#     thread_id,
#     role="user",
#     content='평가 시 참고할 점은 <' + consider_points + '> 입니다.',
#     )

run_button = st.button('평가 시 고려할 점 입력')

if run_button:
    thread_message = client.beta.threads.messages.create(
    thread_id,
    role="user",
    content='평가 시 참고할 점은 <' + consider_points + '> 입니다.',
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

# 문항 입력이 완료 되었다는 문구 생성
    st.success('평가 시 고려한 점 입력이 완료되었습니다.')

st.divider()

# 주고받은 thread 확인하기 
# if "messages" not in st.session_state:
#     st.session_state["messages"] = [{"role": "assistant", "content": "서술형 평가 문제에 대한 답을 입력해주세요."}]

# for msg in st.session_state.messages:
#     st.chat_message(msg["role"]).write(msg["content"])

# if prompt := st.chat_input():
#     if not openai_api_key:
#         st.info("Please add your OpenAI API key to continue.")
#         st.stop()

#     if not thread_id:
#         st.info("Please add your thread ID to continue.")
#         st.stop()

#     st.session_state.messages.append({"role": "user", "content": prompt})
#     st.chat_message("user").write(prompt)

#     response = client.beta.threads.messages.create(
#         thread_id,
#         role="user",
#         content=prompt,
#         )
    
#     print(response)

#     run = client.beta.threads.runs.create(
#         thread_id=thread_id,
#         assistant_id=assistant_id
#         )
#     print(run)

#     run_id = run.id

#     while True:
#         run = client.beta.threads.runs.retrieve(
#             thread_id=thread_id,
#             run_id=run_id
#             )   
#         if run.status == "completed":
#             break
#         else:
#             time.sleep(2)
#         print(run)

#     thread_messages = client.beta.threads.messages.list(thread_id)
#     print(thread_messages.data)

#     msg = thread_messages.data[0].content[0].text.value
#     print(msg)

#     st.session_state.messages.append({"role": "assistant", "content": msg})
#     st.chat_message("assistant").write(msg)