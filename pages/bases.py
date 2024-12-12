import streamlit as st
import pandas as pd
from sqlalchemy.orm import sessionmaker, joinedload, aliased
from bd import Cliente, Obra,Programacao, session

clientes = session.query(Cliente).all()
df_clientes = pd.DataFrame([c.__dict__ for c in clientes])
df_clientes.drop(columns='_sa_instance_state', inplace=True) 

st.write('Base clientes')
st.dataframe(df_clientes)


obras = session.query(Obra).all()
df_obras=pd.DataFrame([o.__dict__ for o in obras])
df_obras.drop(columns='_sa_instance_state', inplace=True)
st.write('Base obras')
st.dataframe(df_obras)

#ClienteAlias = aliased(Cliente)
#ProgramacaoAlias = aliased(Programacao)

query = (
    session.query(Obra, Cliente, Programacao)
    .outerjoin(Cliente, Cliente.projeto == Obra.nota_proj)
    .outerjoin(Programacao, Programacao.nota_proj == Obra.nota_proj)
)
resultados = query.all()

# Transformar o resultado em um DataFrame
df_query = pd.DataFrame(
    [
        {**o.__dict__, **(c.__dict__ if c else {}), **(p.__dict__ if p else {})}
        for o, c, p in resultados
    ]
)

# Remover a coluna _sa_instance_state
df_query.drop(columns='_sa_instance_state', errors='ignore', inplace=True)

# Exibir no Streamlit
st.write('Programações')
st.dataframe(df_query)