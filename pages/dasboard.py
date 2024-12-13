import streamlit as st
import pandas as pd
from sqlalchemy.orm import sessionmaker
from bd import Cliente, Obra, Programacao, session
from sqlalchemy import func

query1 = (
    session.query(Obra).all()
)
df_obras = pd.DataFrame([obra.__dict__ for obra in query1])
df_obras.drop(columns='_sa_instance_state', errors='ignore', inplace=True)
#st.dataframe(df_obras)


query2 = (
    session.query(Cliente).all()
)
df_cliente = pd.DataFrame([clientes.__dict__ for clientes in query2])
df_cliente.drop(columns='_sa_instance_state', errors='ignore', inplace=True)
#st.dataframe(df_cliente)

query3 = (
    session.query(Programacao).all()
)
df_programacao = pd.DataFrame([programacoes.__dict__ for programacoes in query3])
df_programacao.drop(columns='_sa_instance_state', errors='ignore', inplace=True)
#st.dataframe(df_programacao)

df_obras_qlp = pd.merge(df_obras,df_cliente,how="left",left_on="nota_proj",right_on="projeto")
df_obras_qlp = df_obras_qlp[df_obras_qlp["nota_proj"]!=0]
df_obras_qlp['clientes_qlp']=df_obras_qlp.groupby('nota_proj')['nota_ccs'].transform("count")
df_obras_qlp = df_obras_qlp.drop_duplicates(subset = 'nota_proj')
df_obras_qlp = df_obras_qlp.drop(labels=['id_x','id_y'],axis = 1)
st.dataframe(df_obras_qlp)