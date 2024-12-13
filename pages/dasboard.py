import streamlit as st
import pandas as pd
from sqlalchemy.orm import sessionmaker
from bd import Cliente, Obra, Programacao, session
from sqlalchemy import func


# Query 1: Obras com programações
query1 = (
    session.query(Obra).all()
)
df_obras = pd.DataFrame([obra.__dict__ for obra in query1])
df_obras.drop(columns='_sa_instance_state', errors='ignore', inplace=True)
st.dataframe(df_obras)


query2 = (
    session.query(Cliente).all()
)
df_cliente = pd.DataFrame([clientes.__dict__ for clientes in query2])
df_cliente.drop(columns='_sa_instance_state', errors='ignore', inplace=True)
st.dataframe(df_cliente)

query3 = (
    session.query(Programacao).all()
)
df_programacao = pd.DataFrame([programacoes.__dict__ for programacoes in query3])
df_programacao.drop(columns='_sa_instance_state', errors='ignore', inplace=True)
st.dataframe(df_programacao)