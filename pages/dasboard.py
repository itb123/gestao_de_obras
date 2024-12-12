import streamlit as st
import pandas as pd
from sqlalchemy.orm import sessionmaker
from bd import Cliente, Obra,Programacao, session

query = (
    session.query(Obra,Programacao)
    .outerjoin(Programacao, Programacao.nota_proj == Obra.nota_proj)
    .filter(Programacao.data_programacao.isnot(None))
)
resultados = query.all()

# Transformar o resultado em um DataFrame
df_query = pd.DataFrame(
    [
        {**o.__dict__, **(p.__dict__ if p else {})}
        for o, p in resultados
    ]
)

# Remover a coluna _sa_instance_state
df_query.drop(columns='_sa_instance_state', errors='ignore', inplace=True)

# Exibir no Streamlit
st.write('Obras com programações')
st.dataframe(df_query)

query2 = (
    session.query(Obra,Cliente)
    .outerjoin(Cliente, Obra.nota_proj == Cliente.projeto)
    .group_by(Obra.nota_proj)
)
# Remover a coluna _sa_instance_state

resultados2 = query2.all()

# Transformar o resultado em um DataFrame
df_query2 = pd.DataFrame(
    [
        {**o.__dict__, **(p.__dict__ if p else {})}
        for o, p in resultados2
    ]
)

df_query2.drop(columns='_sa_instance_state', errors='ignore', inplace=True)
# Exibir no Streamlit
st.write('Obras QLP')
st.dataframe(df_query2)