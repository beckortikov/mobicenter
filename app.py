import streamlit as st
import pandas as pd
import joblib
import gspread
# Загрузка модели
model = joblib.load('gboost_pipeline_1.0.pkl')

# Ввод данных с использованием инпутов
st.title('Модель скоринга')

age = st.sidebar.number_input(r'$\textsf{\normalsize Ёш}$', value=24, step=1)
gender = st.sidebar.radio(r'$\textsf{\normalsize Жинси}$', ['Эркак', 'Аёл'])
amount = st.sidebar.number_input(r'$\textsf{\normalsize Сумма}$', value=500000, step=10000)
duration = st.sidebar.selectbox(r'$\textsf{\normalsize Муддат}$',[6, 12])
marital_status = st.sidebar.selectbox(r'$\textsf{\normalsize Оилавий статус}$', ['Оилали', 'Уйланмаган/Турмуш курмаган', 'Ажрашган', 'Бошка'])
income = st.sidebar.number_input(r'$\textsf{\normalsize Даромади}$', value=0, step=100000)
dependants = st.sidebar.selectbox(r'$\textsf{\normalsize Карамогидагилар сони}$',[0, 1, 2, 3, 4, 5])
occupation_branch = st.sidebar.selectbox(r'$\textsf{\normalsize Иш сохаси}$', ['Ишлаб чикариш', 'Бошка соха', 'Савдо', 'Банк сохаси', 'Харбий', 'Таълим сохаси', 'Логистика', 'Кишлок хужалиги', 'Медицина сохаси',
                                                                        'Курилиш сохаси', 'ЖКХ', 'Пенсионер'])
occupation = st.sidebar.selectbox(r'$\textsf{\normalsize Лавозими}$', ['Оддий ишчи', 'Юкори малакали мутхассис', 'Пенсионер/Студент', 'Бошлиг/Хужаин'])
exp_cat = st.sidebar.selectbox(r'$\textsf{\normalsize Иш тажрибаси}$', ['3 йилдан 5 гача', '5 йилдан зиёд', '1 йилдан 3 гача', '1 йилдан кам', 'Тажрибаси йук'])


def authenticate_gspread():
    # Load Google Sheets API credentials
    sa = gspread.service_account(filename='credits_mobi.json')
    return sa


# Function to duplicate data to Google Sheets
# Function to duplicate data to Google Sheets
def duplicate_to_gsheet(new_row):
    # Authenticate with Google Sheets
    gc = authenticate_gspread()

    # Create a new Google Sheets spreadsheet
    sh = gc.open("MyTasks")

    # Select the first sheet (index 0)
    worksheet = sh.worksheet("Scoring")

    # Check if there's any content in the worksheet
    existing_data = worksheet.get_all_values()

    # Get existing headers if they exist
    headers = existing_data[0] if existing_data else None

    if not headers:
        headers = ['Возраст', 'Пол', 'Сумма кредита',
                   'Период', 'Семейное положение',	'Доход',
                   'Иждевенцы',	'Сфера занятости',	'Роль',	'Стаж работы',
                   'Результат', 'Вероятность возврата']
        worksheet.append_row(headers)

    # Convert the new_row DataFrame to a list and append it to the worksheet
    new_row_list = new_row.values.tolist()
    worksheet.append_rows(new_row_list)


# Предсказание
if st.sidebar.button('Получить скоринг'):
    input_data = pd.DataFrame({
        'Age': [age],
        'Gender': [1 if gender == 'Мужской' else 0],
        'Amount': [amount],
        'Duration': [duration],
        'MaritalStatus': [marital_status],
        'Income': [income],
        'Dependants': [dependants],
        'OccupationBranch': [occupation_branch],
        'Occupation': [occupation],
        'ExpCat': [exp_cat]
    })

    prediction = model.predict_proba(input_data)[:, 0]
    st.subheader('Результат:')
    st.write(f'Кредит кайтариш эхтимоли: {round(prediction[0]*100, 2)}%')
    # st.write(f'{round(prediction[0]*100, 2)}%')
    if prediction > 1 - 0.05:
        st.success(r'$\textsf{\Large Кредит тасдикланди! 🎉}$')
        st.balloons()
        input_data['Result'] = 'Одобрено'
        input_data['Gender'] = gender
        input_data['Probability'] = f'{round(prediction[0]*100, 2)}%'
        duplicate_to_gsheet(input_data)
    else:
        st.error(r'$\textsf{\Large Рад этилди. 😞}$')
        input_data['Result'] = 'Отказано'
        input_data['Gender'] = gender
        input_data['Probability'] = f'{round(prediction[0]*100, 2)}%'
        duplicate_to_gsheet(input_data)
