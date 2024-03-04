import streamlit as st
import pandas as pd
import joblib
import gspread
# Загрузка модели
model = joblib.load('gboost_pipeline_2.0.pkl')
# Функция для генерации PDF
from datetime import datetime
from fpdf import FPDF
from PIL import Image
def generate_pdf(data, document_number, date):
    # Create instance of FPDF class
    pdf = FPDF()

    # Add a page
    pdf.add_page()

    # Set font for the title
    pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font('DejaVu', '', 14)

    pdf.image('Logo.png', x=15, y=15, w=40)
    pdf.ln(20)
    # Title
    pdf.cell(200, 10, txt="Скоринг рассрочки",  ln=True, align='C')
    pdf.ln(10)  # Add a little space after the title


    # Define the variables list on the left side
    # Mapping between internal variable names and human-readable names
    variable_mapping = {
        'Region': 'Филиал',
        'Name': 'Имя',
        'Surname': 'Фамилия',
        'Phone': 'Телефон номер',
        'Age': 'Ёши',
        'Gender': 'Жинси',
        'Amount': 'Сумма',
        'Duration': 'Муддат',
        'MaritalStatus': 'Оилавий статус',
        'Income': 'Даромади',
        'Dependants': 'Карамогидагилар сони',
        "OccupationBranch": 'Иш сохаси',
        "Occupation": "Лавозими",
        "ExpCat": 'Иш тажрибаси',
        'Result': 'Результат',
        'Probability': 'Вероятность возврата',
        'Date': 'Дата',
        'DocumentNumber': 'Номер документа'
    }

    var = ['Region', 'Name', 'Surname', 'Phone', 'Age', 'Gender', 'Amount', 'Duration', 'MaritalStatus',
        'Income', 'Dependants', 'OccupationBranch', 'Occupation', 'ExpCat', 'Result', 'Probability', 'Date', 'DocumentNumber']

    # Add content to the PDF using a table
    pdf.set_fill_color(255, 255, 255)  # Set white fill color
    col_width = 80
    row_height = 10
    x_position = (pdf.w - col_width * 2) / 2  # Calculate x position to center the table
    y_position = pdf.get_y()
    for var_name in var:
        # Get the human-readable name corresponding to the internal variable name
        variable = variable_mapping.get(var_name, '')
        value = data.get(var_name, [''])[0]  # Get the value from data or empty string if not found
        pdf.set_xy(x_position, y_position)
        pdf.cell(col_width, row_height, txt=variable, border=1, fill=False)
        pdf.cell(col_width, row_height, txt=str(value), border=1, fill=False)
        pdf.ln(row_height)
        y_position = pdf.get_y()
    pdf.set_xy(x_position, pdf.get_y() + 20)  # Move down 10 units
    pdf.cell(col_width, row_height, txt="Подпись: _____________________", border=0, fill=False)
    # pdf.cell(col_width, row_height, txt="Директор:", border=0, fill=False)

    # current_x = pdf.get_x()  # Get current X position
    # current_y = pdf.get_y()  # Get current Y position

    # # Calculate new positions with desired margins
    # new_x = current_x -100 # Add 20mm to the right
    # new_y = current_y + 15   # Subtract 5mm from the top (moving upwards)

    # # Set new position
    # pdf.set_xy(new_x, new_y)
    # pdf.cell(0, 10, 'Менеджер:', 0, 0, 'L')
    # pdf.cell(0, 10, 'Директор:', 0, 0, 'C')
    # Output the cell
    # pdf.cell(0, 10, txt="Подпись: ______________________", ln=True, align='R')

    # Save the PDF to a file
    pdf.output("result.pdf")

    # Return the PDF file name or content depending on your requirement
    with open("result.pdf", "rb") as pdf_file:
        PDFbyte = pdf_file.read()

    st.download_button(label="Скачать документ",
                       data=PDFbyte,
                       file_name="test.pdf",
                       mime='application/octet-stream')

# st.sidebar.image("Logo.png", use_column_width=False, width=200, height=10)

# Ввод данных с использованием инпутов
st.title('Модель скоринга')
region = st.sidebar.selectbox(r'$\textsf{\normalsize Филиал}$', ["Жомбой", "Жума", "Тайлок", "Согдиана", "Гагарин"])
name = st.sidebar.text_input(r'$\textsf{\normalsize Исм}$', '')
surname = st.sidebar.text_input(r'$\textsf{\normalsize Фамилия}$', '')
phone = st.sidebar.number_input(r'$\textsf{\normalsize Телефон номер}$', value=0, placeholder="Номер теринг")
age = st.sidebar.number_input(r'$\textsf{\normalsize Ёш}$', value=24, step=1)
gender = st.sidebar.radio(r'$\textsf{\normalsize Жинси}$', ['Эркак', 'Аёл'])
amount = st.sidebar.number_input(r'$\textsf{\normalsize Сумма}$', value=0, placeholder="Телефон нархи")
duration = st.sidebar.selectbox(r'$\textsf{\normalsize Муддат}$', [3, 6, 9, 12])
marital_status = st.sidebar.selectbox(r'$\textsf{\normalsize Оилавий статус}$', ['Оилали', 'Уйланмаган/Турмуш курмаган', 'Ажрашган', 'Бошка'])
income = st.sidebar.number_input(r'$\textsf{\normalsize Даромади}$', value=0, placeholder="Ойлик даромади")
dependants = st.sidebar.selectbox(r'$\textsf{\normalsize Карамогидагилар сони}$', [0, 1, 2, 3, 4, 5])
occupation_branch = st.sidebar.selectbox(r'$\textsf{\normalsize Иш сохаси}$', ['Ишлаб чикариш', 'Бошка соха', 'Савдо', 'Банк сохаси', 'Харбий', 'Таълим сохаси', 'Логистика', 'Кишлок хужалиги', 'Медицина сохаси',
                                                                        'Курилиш сохаси', 'ЖКХ', 'Пенсионер'])
occupation = st.sidebar.selectbox(r'$\textsf{\normalsize Лавозими}$', ['Оддий ишчи', 'Юкори малакали мутхассис', 'Пенсионер/Студент', 'Бошлиг/Хужаин'])
exp_cat = st.sidebar.selectbox(r'$\textsf{\normalsize Иш тажрибаси}$', ['3 йилдан 5 гача', '5 йилдан зиёд', '1 йилдан 3 гача', '1 йилдан кам', 'Тажрибаси йук'])

def authenticate_gspread():
    # Load Google Sheets API credentials
    sa = gspread.service_account(filename='credits_mobi.json')
    return sa

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
        headers = ['Филиал', 'Телефон номер', 'Имя', 'Фамилия', 'Возраст', 'Пол', 'Сумма кредита', 'Период', 'Семейное положение', 'Доход',
                   'Иждевенцы', 'Сфера занятости', 'Роль', 'Стаж работы', 'Результат', 'Вероятность возврата', 'Дата', 'Номер документа']
        worksheet.append_row(headers)

    # Convert the new_row DataFrame to a list and append it to the worksheet
    new_row = new_row[['Region', 'Phone', 'Name', 'Surname', 'Age', 'Gender', 'Amount', 'Duration', 'MaritalStatus', 'Income',
                       'Dependants', 'OccupationBranch', 'Occupation', 'ExpCat', 'Result', 'Probability', 'Date', 'DocumentNumber']]
    new_row_list = new_row.values.tolist()
    worksheet.append_rows(new_row_list)

# Предсказание
if st.sidebar.button('Получить скоринг'):
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    document_number = f'Doc_{current_date.replace(" ", "_").replace(":", "_")}'

    input_data = pd.DataFrame({
        'Age': [age],
        'Gender': [1 if gender == 'Эркак' else 0],
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
    input_data['Region'] = region
    input_data['Name'] = name
    input_data['Surname'] = surname
    input_data['Phone'] = phone
    input_data['Result'] = 'Одобрено' if prediction > 1 - 0.05 else 'Отказано'
    input_data['Gender'] = gender
    input_data['Probability'] = f'{round(prediction[0]*100, 2)}%'
    input_data['Date'] = current_date
    input_data['DocumentNumber'] = document_number

    if prediction > 1 - 0.05:
        st.success(r'$\textsf{\Large Кредит тасдикланди! 🎉}$')

        st.balloons()
        duplicate_to_gsheet(input_data)
    else:
        st.error(r'$\textsf{\Large Рад этилди. 😞}$')
        duplicate_to_gsheet(input_data)

    generate_pdf(input_data, document_number, current_date)