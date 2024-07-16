import streamlit as st
import csv
import random
import os

#csvの読み込み ヘッダーを除いて問題と解答、注記をリストに格納

FILENAME = 'quiz.csv'

#クイズデータをcsvからダウンロード
def load_quiz_data(filename):
    if os.path.exists(filename):
        with open(filename, mode="r", encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            next(reader)
            return [row for row in reader]
    else :
        return None

#クイズを生成する関数
def get_random_quiz(quiz_data, used_questions):
    if quiz_data is None:
        return None
    available_quizzes = [quiz for quiz in quiz_data if quiz[1] not in used_questions]
    if not available_quizzes:
        return None
    selected_quiz = random.choice(available_quizzes)
    question = selected_quiz[1]
    options = selected_quiz[2:6]
    correct_answer = selected_quiz[2]
    note = selected_quiz[6]
    random.shuffle(options)
    return question, options, correct_answer, note

#セッション情報の初期化
if 'remaining_quiz' not in st.session_state:
    st.session_state.remaining_quiz = 15
    st.session_state.score = 0
    st.session_state.incorrect_answers = []
    st.session_state.quiz_data = load_quiz_data(FILENAME)
    st.session_state.used_questions = []
    st.session_state.current_quiz = get_random_quiz(st.session_state.quiz_data, st.session_state.used_questions)
    st.session_state.user_answer = None
    st.session_state.feedback_given = False
    st.session_state.correct = False
    st.session_state.quiz_ended = False
    st.session_state.answer_submitted = False

remaining_quiz = st.session_state.remaining_quiz
score = st.session_state.score
quiz_data = st.session_state.quiz_data
current_quiz = st.session_state.current_quiz
user_answer = st.session_state.user_answer
feedback_given = st.session_state.feedback_given
quiz_ended = st.session_state.quiz_ended
answer_submitted = st.session_state.answer_submitted


#タイトル表示
st.title('Nihongo Kotoba Quiz - Version Prototype')

def end_quiz():
    st.session_state.quiz_ended = True

#クイズ終了後の表示
if quiz_ended or remaining_quiz == 0:
    st.markdown(f'### Votre score est {score} points sur 10')
    st.markdown(f'### Liste des questions et réponses incorrectes')
    for question, correct_answer, note in st.session_state.incorrect_answers:
        st.markdown(f'-{question}  \nRéponse : {correct_answer}  \n{note}')
    
    if st.button('Commancez un nouveau quiz'):
        st.session_state.remaining_quiz = 15
        st.session_state.score = 0
        st.session_state.incorrect_answers = []
        st.session_state.used_questions = []
        st.session_state.quiz_data = load_quiz_data(FILENAME)
        st.session_state.current_quiz = get_random_quiz(st.session_state.quiz_data, st.session_state.used_questions)
        st.session_state.feedback_given = False
        st.session_state.user_answer = None
        st.session_state.correct
        st.session_state.quiz_ended = False
        st.session_state.answer_submitted = False
        st.experimental_rerun()
else:
    if current_quiz is not None:
        question, options, correct_answer, note = current_quiz
        st.markdown(f'#### Nombre de questions restantes : {remaining_quiz}')
        st.markdown(f'##### Retrouvez le mot manquant')
        st.markdown(f'### {question}')
        user_answer = st.radio('',options, key='quiz_radio')

        if st.button('Envoyez la réponse') and not feedback_given and not answer_submitted:
            st.session_state.user_answer = user_answer
            st.session_state.feedback_given = True
            st.session_state.answer_submitted = True
            if user_answer == correct_answer:
                st.session_state.correct = True
                st.session_state.score += 1
            else:
                st.session_state.correct = False
                st.session_state.incorrect_answers.append((question,correct_answer,note))
            st.experimental_rerun()
        
        if feedback_given:
            if st.session_state.correct:
                st.markdown(f'#### Correct ! \n {note}')
            else:
                st.markdown(f'#### Incorrect - Réponse "{correct_answer}" \n {note}')
        
        if feedback_given and st.button('Question suivante'):
            st.session_state.remaining_quiz -= 1
            if st.session_state.remaining_quiz > 0:
                st.session_state.used_questions.append(question)
                st.session_state.current_quiz = get_random_quiz(st.session_state.quiz_data, st.session_state.used_questions)
            st.session_state.feedback_given = False
            st.session_state.user_answer = None
            st.session_state.correct = False
            st.session_state.answer_submitted = False
            st.experimental_rerun()

    if st.button('Terminer le quiz'):
        end_quiz()
        st.experimental_rerun()

st.markdown(f'#### Socore actuel : {score} points')
