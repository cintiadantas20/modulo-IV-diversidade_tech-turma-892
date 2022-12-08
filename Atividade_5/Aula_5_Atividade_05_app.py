import numpy as np
import pandas as pd
import seaborn as sns
import plotly.express as px
import streamlit as st
from funcoes import carrega_dataset


# CORPO
## CORPO - Título da Aplicação
st.markdown("""
            # iNalyze
            ### *A sua ferramenta de análise de dados*
            ---
            """)


## CORPO - Carregando o dataset
nome_dataset = \
    st.text_input('Qual o nome do dataset?',
                  value='penguins')
   
if nome_dataset: 
    df = carrega_dataset(nome_dataset)
    
        
# SIDEBAR
## SIDEBAR - Filtro dos campos
with st.sidebar:
    st.title('Filtros')
    cols_selected = \
        st.multiselect('Filtre os campos que deseja para a análise:',
                   options=list(df.columns),
                   default=list(df.columns))

# filtra os campos selecionados
df_selected = df[cols_selected]
    
## SIDEBAR - Filtro de amostra
with st.sidebar:
    st.title('Amostra')


    amostra = \
        st.slider('Selecione a porcentagem da amostra desejada:', 
                  min_value=1, max_value=100, step=1)
    amostra = amostra/100
    df_selected = df_selected.sample(frac = amostra)


## CORPO - Info do dataset

with st.expander('Dados do Dataset'):
    st.header('Dados do Dataset')
    st.subheader('Primeiros Registros')
    st.dataframe(df_selected.head(), width=600)

    st.subheader('Colunas')
    for col in df_selected.columns:
        st.markdown(f'- {col}')
        
    st.subheader('Dados Faltantes')
    st.write(df_selected.isna().sum()[df_selected.isna().sum() > 0])

    st.subheader('Tamanho do dataset')
    st.write(f'{len(df_selected)} linhas')
    st.write(f'{len(df_selected.columns)} colunas')

    st.subheader('Estatísticas Descritivas')
    st.write(df_selected.describe())


## CORPO - Análise Univariada
st.header('Análise Univariada')
univar_campo = \
    st.selectbox('Selecione um campo númerico para avaliar sua distribuição:',
                 options=list(df_selected.select_dtypes(include=np.number).columns))
    
st.plotly_chart(px.histogram(data_frame=df_selected, x=univar_campo))
st.plotly_chart(px.box(data_frame=df_selected, y=univar_campo))


## CORPO - Análise Bivariada
st.header('Análise Bivariada')
bivar_graf_option = \
    st.radio('Escolha um tipo de gráfico:',
             options=['dispersão', 'boxplot', 'pairplot'],
             key = 'escolha_bivar')

### CORPO - Análise Bivariada - gráfico de dispersão
if bivar_graf_option == 'dispersão':
    campo_dispersao_1 =  \
        st.selectbox('Selecione primeira variável numérica:',
                     options=list(df_selected.select_dtypes(include=np.number)),
                     key = 'dispersao1_bivar')
        
    campo_dispersao_2 =  \
        st.selectbox('Selecione segunda variável numérica:',
                     options=list(df_selected.select_dtypes(include=np.number)),
                     key = 'dispersao2_bivar')
        
    st.plotly_chart(
        px.scatter(data_frame=df_selected, 
                   x=campo_dispersao_1, 
                   y=campo_dispersao_2)
    )


### CORPO - Análise Bivariada - gráfico de boxplot       
elif bivar_graf_option == 'boxplot':
    campo_boxplot_num =  \
        st.selectbox('Selecione uma variável numérica:',
                     options=list(df_selected.select_dtypes(include=np.number)),
                     key = 'boxplot1_bivar')
        
    campo_boxplot_cat =  \
        st.selectbox('Selecione uma variável categórica:',
                     options=list(df_selected.select_dtypes(exclude=np.number)),
                     key = 'boxplot1_bivar')
        
    st.plotly_chart(
        px.box(data_frame=df_selected, 
                   x=campo_boxplot_cat, 
                   y=campo_boxplot_num)
    )

### CORPO - Análise Bivariada - gráfico de pairplot  
else:
    pairplot = sns.pairplot(df_selected)
    st.pyplot(pairplot)

    
#-----------------------------------------------

## CORPO - Análise Multivariada
st.header('Análise Multivariada')
multivar_graf_option = \
    st.radio('Escolha um tipo de gráfico:',
             options=['dispersão', 'boxplot', 'pairplot'],
             key = 'escolha_multivar')

### CORPO - Análise Multivariada - gráfico de dispersão
if multivar_graf_option == 'dispersão':
    multivar_campo_dispersao_1 =  \
        st.selectbox('Selecione primeira variável numérica:',
                     options=list(df_selected.select_dtypes(include=np.number)),
                     key = 'dispersao1_multivar')
        
    multivar_campo_dispersao_2 =  \
        st.selectbox('Selecione segunda variável numérica:',
                     options=list(df_selected.select_dtypes(include=np.number)),
                     key = 'dispersao2_multivar')
        
    multivar_campo_dispersao_3 =  \
        st.selectbox('Selecione uma variável categórica para segmentação:',
                     options=list(df_selected.select_dtypes(exclude=np.number)),
                     key = 'dispersao3_multivar')

    multivar_campo_dispersao_4 = \
        st.checkbox('Adicionar linha de tendência',
                    key = 'dispersao4_multivar')

    if multivar_campo_dispersao_4:
        st.plotly_chart( 
            px.scatter(data_frame=df_selected, 
                    x=multivar_campo_dispersao_1, 
                    y=multivar_campo_dispersao_2,
                    color=multivar_campo_dispersao_3,
                    trendline='ols'))

    else:
        st.plotly_chart( 
            px.scatter(data_frame=df_selected, 
                    x=multivar_campo_dispersao_1, 
                    y=multivar_campo_dispersao_2,
                    color=multivar_campo_dispersao_3)
    )

### CORPO - Análise Multivariada - gráfico de boxplot       
elif multivar_graf_option == 'boxplot':
    multivar_campo_boxplot_num =  \
        st.selectbox('Selecione uma variável numérica:',
                     options=list(df_selected.select_dtypes(include=np.number)),
                     key = 'boxplot1_multivar')
        
    multivar_campo_boxplot_cat =  \
        st.selectbox('Selecione uma variável categórica:',
                     options=list(df_selected.select_dtypes(exclude=np.number)),
                     key = 'boxplot2_multivar')
        
    multivar_campo_boxplot_seg =  \
        st.selectbox('Selecione uma variável categórica para segmentação:',
                     options=list(df_selected.select_dtypes(exclude=np.number)),
                     key = 'boxplot3_multivar')

    st.plotly_chart(
        px.box(data_frame=df_selected, 
                   x=multivar_campo_boxplot_cat, 
                   y=multivar_campo_boxplot_num,
                   color=multivar_campo_boxplot_seg)
    )

### CORPO - Análise Multivariada - gráfico de pairplot  
else:
    multivar_campo_pairplot_seg =  \
        st.selectbox('Selecione uma variável categórica para segmentação:',
                     options=list(df_selected.select_dtypes(exclude=np.number)),
                     key = 'pairplot_multivar')

    multivar_pairplot = sns.pairplot(df_selected, hue = multivar_campo_pairplot_seg)
    st.pyplot(multivar_pairplot)


# ATIVIDADES
# Refatore o código, aplicando as modificações:

# 1 - Modularize o código passando a função "carrega_dataset" para um módulo

# 2 - Crie um slider no sidebar que permita filtrar uma amostra do dataset.
#     Para realizar amostragem, utilize o método sample do dataframe pandas.

# 3 - Adicione a informação do tamanho do dataset na seção 
#     de 'Dados do Dataset'

# 4 - Adicione uma seção de análise multivariada:
#   4.1 - Adicione a possibilidade de segmentação no gráfico de dispersao
#   4.2 - Adicione checkbox que permita incluir linha de tendência 
#         no gráfico de dispersão
#   4.3 - Adicione a possibilidade de segmentação no gráfico de boxplot
#   4.4 - Adicione a possibilidade de segmentação no gráfico de pairplot

