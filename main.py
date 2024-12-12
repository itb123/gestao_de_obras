import streamlit as st
import pandas as pd
from sqlalchemy.orm import sessionmaker
from bd import Cliente, Obra,Programacao, session

st.write("Upload de arquivo para Banco de Dados")
#funcao para verificar as colunas obrigatorias
def validar_colunas(df,colunas_necessarias): 
    return all(col in df.columns for col in colunas_necessarias)
# Função para verificar se o registro já existe
def registro_existe(model, **kwargs):
    return session.query(model).filter_by(**kwargs).first() is not None
# Componente para upload de arquivo
file = st.file_uploader("Arquivo Clientes", type=["xlsx"])
if file:
    # Ler o arquivo Excel no Pandas DataFrame
    df = pd.read_excel(file)
    st.write("Pré-visualização")
    #exibir as 10 primeiras linhas
    st.dataframe(df.head())
    #colunas obrigatorias
    colunas_clientes = [
        'nota_css', 'status_ccs', 'projeto', 'data_solicitacao', 
        'data_aceite', 'cidade', 'prazo_nota', 'motivo_susp', 
        'reclamacao', 'ouvidoria','data_ligacao','status_projeto','motivo_expurgo',
        'dias_susp'
        ]
    for _ in ['data_solicitacao','data_aceite','prazo_nota','data_ligacao']:
        df  = df.astype({_:'str'})
    #inova a funcao de validação de colunas e verificar com as colunas do arquivo
    if not validar_colunas(df,colunas_clientes):
        st.error("o arquivo não contém as colunas obrigatórias!")
    # Botão para salvar os dados no banco de dados
    elif st.button("Salvar no Banco Cliente"):
        erros =[]
        try:
            # Loop para inserir cada linha no banco
            for i, row in df.iterrows():
                if not registro_existe(Cliente, nota_ccs=row['nota_css']):
                    cliente = Cliente(
                        nota_ccs=row['nota_css'],
                        status_ccs=row['status_ccs'],
                        projeto=row['projeto'],
                        status_projeto=row['status_projeto'],
                        data_solicitacao=row['data_solicitacao'],
                        data_aceite=row['data_aceite'],
                        data_ligacao=row['data_ligacao'],
                        dias_susp=row['dias_susp'],
                        cidade=row['cidade'],
                        prazo_nota=row['prazo_nota'],
                        motivo_susp=row['motivo_susp'],
                        motivo_expurgo=row['motivo_expurgo'],
                        reclamacao=row['reclamacao'],
                        ouvidoria=row['ouvidoria']
                    )
                    session.add(cliente)  # Adicionar o objeto à sessão
                else:
                    st.info(f"Cliente já existe: Nota CSS {row['nota_css']}")
        except Exception as e:
            erros.append((i,e))
        try:
            session.commit()  # Confirmar as mudanças no banco
            if erros:
                st.warning(f"{len(erros)} registros falharam {erros}")
            else:
                st.success("Todos os dados de Clientes foram salvos com sucesso!")
        except Exception as e:
            session.rollback()
            st.error(f"Erro ao salvar no banco: {str(e)}")

file2 = st.file_uploader("Arquivo Obras", type=["xlsx"])

if file2:
        # Ler o arquivo Excel no Pandas DataFrame
        df2 = pd.read_excel(file2)
        st.write("Pré-visualização")
        st.dataframe(df2.head())
            # Botão para salvar os dados no banco de dados
        colunas_obras = [
            'nota_proj', 'pep', 'status_pep', 'parceira_execucao', 'descricao',
            'valor', 'trafo', 'rede_mt', 'rede_bt', 'poste', 'tipo_de_obra', 
            'estudo_ambiental', 'data_criacao_pep', 'data_aber_log','data_lib_log',
            'data_lib_atec', 'data_lib_ener', 'data_envio_validacao', 
            'data_retorno_validacao','parceira_validacao','retorno_validacao'
        ]
        for _ in ['data_criacao_pep', 'data_aber_log','data_lib_log',
            'data_lib_atec', 'data_lib_ener', 'data_envio_validacao', 
            'data_retorno_validacao']:
            df2 = df2.astype({_:'str'})           
        if not validar_colunas(df2, colunas_obras):
            st.error("O arquivo não contém todas as colunas obrigatórias.")
        else:
            if st.button("Salvar no Banco Projetos"):
                erros = []
                for i, row in df2.iterrows():
                    if not registro_existe(Obra, nota_proj=row['nota_proj']):
                        try:
                            obra = Obra(
                                nota_proj=row['nota_proj'],
                                pep=row['pep'],
                                status_pep=row['status_pep'],
                                parceira_execucao=row['parceira_execucao'],
                                descricao=row['descricao'],
                                valor=row['valor'],
                                trafo=row['trafo'],
                                rede_mt=row['rede_mt'],
                                rede_bt=row['rede_bt'],
                                poste=row['poste'],
                                tipo_de_obra=row['tipo_de_obra'],
                                estudo_ambiental=row['estudo_ambiental'],
                                data_criacao_pep = row['data_criacao_pep'],
                                data_aber_log=row['data_aber_log'],
                                data_lib_log=row['data_lib_log'],
                                data_lib_atec=row['data_lib_atec'],
                                data_lib_ener=row['data_lib_ener'],
                                data_envio_validacao=row['data_envio_validacao'],
                                data_retorno_validacao=row['data_retorno_validacao'],
                                parceira_validacao=row['parceira_validacao'],
                                retorno_validacao=row['retorno_validacao']
                            )
                            session.add(obra)  # Adicionar o objeto à sessão
                        except Exception as e:
                            erros.append((i, e))
                    else:
                        st.info(f"Obra já existe: Nota Projeto {row['nota_proj']}")
                try:        
                    session.commit()
                    if erros:
                        st.warning(f"{len(erros)} registros falharam: {erros}")
                    else:
                        st.success("Todos os dados de Obras foram salvos com sucesso!")
                except Exception as e:
                    session.rollback()
                    st.error(f"Erro ao salvar no banco: {str(e)}")  

file3 = st.file_uploader("Arquivo Programação", type=["xlsx"])
if file3:
        # Ler o arquivo Excel no Pandas DataFrame
        df3 = pd.read_excel(file3)
        df3 = df3.astype({'nota_proj':'str'})
        df3 = df3.astype({'retorno_programacao':'str'})
        st.write("Pré-visualização")
        st.dataframe(df3.head())
        # Botão para salvar os dados no banco de dados
        colunas_obras = ['nota_proj','data_programacao','retorno_programacao']
        df3=df3.astype({'data_programacao':'str'})              
        if not validar_colunas(df3, colunas_obras):
            st.error("O arquivo não contém todas as colunas obrigatórias.")
        else:
            if st.button("Salvar no Banco Projetos"):
                erros = []
                for i, row in df3.iterrows():
                    try:
                        programacao = Programacao(
                            nota_proj=row['nota_proj'],
                            data_programacao=row['data_programacao'],
                            retorno_programacao=row['retorno_programacao']
                        )
                        session.add(programacao)  # Adicionar o objeto à sessão
                    except Exception as e:
                        erros.append((i, e))
                try:
                    session.commit()
                    if erros:
                        st.warning(f"{len(erros)} registros falharam ao serem inseridos.")
                    else:
                        st.success("Todos os dados de Obras foram salvos com sucesso!")
                except Exception as e:
                    session.rollback()  # Reverter a transação em caso de erro
                    st.error(f"Erro ao salvar no banco: {str(e)}")

