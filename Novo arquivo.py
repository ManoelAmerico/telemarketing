import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image

from warnings import simplefilter
simplefilter(action='ignore')

st.set_page_config(page_title = 'Telemarketing analisys', \
                   page_icon = 'telmarketing_icon.png',
                   layout="wide",
                   initial_sidebar_state='expanded'
                   )

custom_params = {"axes.spines.right": False, "axes.spines.top": False}
sns.set_theme(style="ticks", rc=custom_params)

def load_data(file_data):
    try:
        return pd.read_csv(file_data, sep=';')
    except:
        return pd.read_excel(file_data)


def multiselect_filter(relatorio, col, selecionados):
    if 'all' in selecionados:
        return relatorio
    else:
        return relatorio[relatorio[col].isin(selecionados)].reset_index(drop=True)


def main():
    st.write('# Telemarketing analisys')
    st.markdown("---")

    image = Image.open("Bank-Branding.jpg")
    st.sidebar.image(image)

    st.sidebar.write("## Suba o arquivo")
    data_file_1 = st.sidebar.file_uploader("Bank marketing data", type = ['csv', 'xlsx'])

    if (data_file_1 is not None):
        bank_raw = load_data(data_file_1)
        bank = bank_raw.copy()

        st.write('## Antes dos filtros')
        st.write(bank_raw.head())

        with st.sidebar.form(key='my form'):

            graph_type = st.radio('Tipo de gráfico:', ('Bars', 'Pie'))

            max_age = int(bank.age.max())
            min_age = int(bank.age.min())
            idades = st.slider(label='Idade',
                                min_value = min_age,
                                max_value = max_age,
                                value = (min_age, max_age),
                                step = 1)
            
            jobs_list = bank.job.unique().tolist()
            jobs_list.append('all')
            jobs_selected = st.multiselect("Profissão", jobs_list, ['all'])


            marital_list = bank.marital.unique().tolist()
            marital_list.append('all')
            marital_selected = st.multiselect("Estado Civil", marital_list, ['all'])

            default_list = bank.default.unique().tolist()
            default_list.append('all')
            default_selected = st.multiselect("Default", default_list, ['all'])

            housing_list = bank.housing.unique().tolist()
            housing_list.append('all')
            housing_selected = st.multiselect("Tem financiamento imobiliario?", housing_list, ['all'])

            loan_list = bank.loan.unique().tolist()
            loan_list.append('all')
            loan_selected = st.multiselect("Tem empréstimo?", loan_list, ['all'])

            contact_list = bank.contact.unique().tolist()
            contact_list.append('all')
            contact_selected = st.multiselect("Meio de contato", contact_list, ['all'])

            month_list = bank.month.unique().tolist()
            month_list.append('all')
            month_selected = st.multiselect("Mês de contato", month_list, ['all'])

            day_of_week_list = bank.day_of_week.unique().tolist()
            day_of_week_list.append('all')
            day_of_week_selected = st.multiselect("Dia da semana", day_of_week_list, ['all'])



            bank = (bank.query("age >= @idades[0] and age <= @idades[1]")
                        .pipe(multiselect_filter, 'job', jobs_selected)
                        .pipe(multiselect_filter, 'marital', marital_selected)
                        .pipe(multiselect_filter, 'default', default_selected)
                        .pipe(multiselect_filter, 'housing', housing_selected)
                        .pipe(multiselect_filter, 'loan', loan_selected)
                        .pipe(multiselect_filter, 'contact', contact_selected)
                        .pipe(multiselect_filter, 'month', month_selected)
                        .pipe(multiselect_filter, 'day_of_week', day_of_week_selected)
                        )
            
            submit_button = st.form_submit_button(label='Aplicar')

        fig, axes = plt.subplots(1, 2, figsize=(10, 5))

        contagem = bank_raw.y.value_counts().reset_index()
        contagem.columns = ['Resposta', 'contagem']
        contagem['porcentagem'] = (contagem['contagem']/contagem['contagem'].sum()) * 100
        contagem['porcentagem'] = contagem['porcentagem'].round(2)

        contagem_filtrado = bank.y.value_counts().reset_index()
        contagem_filtrado.columns = ['Resposta', 'contagem']
        contagem_filtrado['porcentagem'] = (contagem_filtrado['contagem']/contagem_filtrado['contagem'].sum()) * 100
        contagem_filtrado['porcentagem'] = contagem_filtrado['porcentagem'].round(2)

        if graph_type == 'Bars':
            sns.barplot(x='Resposta', y='porcentagem', data=contagem, ax=axes[0], palette={'yes': 'skyblue', 'no': 'lightcoral'})
            axes[0].set_title('Total Chart')
            axes[0].set_xlabel("")
            axes[0].set_ylabel("")

            sns.barplot(x='Resposta', y='porcentagem', data=contagem_filtrado, ax=axes[1], palette={'yes': 'skyblue', 'no': 'lightcoral'})
            axes[1].set_title('Filtered Chart')
            axes[1].set_xlabel("")
            axes[1].set_ylabel("")

        else:
            axes[0].pie(x='porcentagem', data=contagem)
            axes[0].set_title('Total Chart')

            axes[1].pie(x='porcentagem', data=contagem_filtrado)
            axes[1].set_title('Filtered Chart')

        st.pyplot(plt)

if __name__ == '__main__':
    main()