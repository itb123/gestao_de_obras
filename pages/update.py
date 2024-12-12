import streamlit as st
import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy import update
from bd import Cliente, Obra, session


def atualizar_status_em_lote(df):
    erros = []
    registros_atualizados = 0
    for _, row in df.iterrows():
        nota_ccs = row['nota_ccs']
        novo_status = row['status_ccs']
        try:
            # Localizar o cliente pelo `nota_ccs`
            cliente = session.query(Cliente).filter_by(nota_ccs=nota_ccs).first()
            if cliente:
                cliente.status_ccs = novo_status  # Atualizar o status
                registros_atualizados += 1
            else:
                erros.append(f"Nota CCS {nota_ccs} não encontrada.")
        except Exception as e:
            erros.append(f"Erro ao atualizar a Nota CCS {nota_ccs}: {str(e)}")

    try:
        session.commit()
    except Exception as e:
        session.rollback()
        st.error(f"Erro ao salvar alterações no banco: {str(e)}")

    return registros_atualizados, erros


def atualizar_pep_ou_status(df, campo, valor, campo_condicao, tabela):
    if campo not in df.columns or valor not in df.columns:
        st.error(f"O arquivo Excel deve conter as colunas '{campo}' e '{valor}'.")
        return

    try:
        for _, row in df.iterrows():
            campo_valor = row[campo]  # PEP ou Status
            valor_atualizado = row[valor]  # Novo status ou valor

            # Construir a query de atualização
            stmt = (
                update(tabela)
                .where(getattr(tabela, campo_condicao) == campo_valor)
                .values(**{valor: valor_atualizado})
            )
            # Executar a atualização
            session.execute(stmt)

        # Confirmar as alterações
        session.commit()
        st.success(f"Atualizações realizadas com sucesso para {campo}!")
    except Exception as e:
        st.error(f"Erro ao atualizar os dados: {e}")
        session.rollback()

def atualizar_datas(df, tabela, campo_condicao):
    colunas_obrigatorias = ["data_criacao_pep", "data_aber_log", "data_lib_log", "data_lib_atec", "data_lib_ener"]
    campos_presentes = [col for col in colunas_obrigatorias if col in df.columns]

    if not campos_presentes:
        st.error(f"O arquivo Excel deve conter pelo menos uma das colunas: {colunas_obrigatorias}")
        return

    try:
        for _, row in df.iterrows():
            condicao_valor = row[campo_condicao]
            valores_atualizados = {
                campo: row[campo] for campo in campos_presentes if pd.notna(row[campo])
            }

            # Construir a query de atualização
            if valores_atualizados:
                stmt = (
                    update(tabela)
                    .where(getattr(tabela, campo_condicao) == condicao_valor)
                    .values(**valores_atualizados)
                )
                # Executar a atualização
                session.execute(stmt)

        # Confirmar as alterações
        session.commit()
        st.success(f"Atualizações realizadas com sucesso para as datas!")
    except Exception as e:
        st.error(f"Erro ao atualizar os dados: {e}")
        session.rollback()

def atualizar_validacao(df,tabela,campo_condicao):
    colunas_obrigatorias = ["nota_proj","parceira_validacao","data_envio_validacao","retorno_validacao","data_retorno_validacao"]
    campos_presentes = [col for col in colunas_obrigatorias if col in df.columns]
    if not campos_presentes:
        st.error(f"O arquivo Excel deve conter pelo menos uma das colunas: {colunas_obrigatorias}")
        return
    try:
        for _, row in df.iterrows():
            condicao_valor = row[campo_condicao]
            valores_atualizados = {
                campo: row[campo] for campo in campos_presentes if pd.notna(row[campo])
            }

            # Construir a query de atualização
            if valores_atualizados:
                stmt = (
                    update(tabela)
                    .where(getattr(tabela, campo_condicao) == condicao_valor)
                    .values(**valores_atualizados)
                )
                # Executar a atualização
                session.execute(stmt)

        # Confirmar as alterações
        session.commit()
        st.success(f"Atualizações realizadas com sucesso para as datas!")
    except Exception as e:
        st.error(f"Erro ao atualizar os dados: {e}")
        session.rollback()


# Título da aplicação
st.title("Atualização de Dados no Banco de Dados")

# Abas para diferentes funcionalidades
aba = st.radio("Selecione a função", ["Atualizar Status CCS", "Atualizar PEP", 
                                      "Inserir PEP","Atualizar Datas"
                                      ,"Validações"])

if aba == "Atualizar Status CCS":
    # Upload do arquivo Excel para atualização de Status CCS
    file = st.file_uploader("Selecione o arquivo Excel com as atualizações", type=["xlsx"])
    if file:
        # Ler o arquivo Excel no DataFrame
        df = pd.read_excel(file)

        # Pré-visualização
        st.write("Pré-visualização dos dados:")
        st.dataframe(df.head())

        # Verificar colunas obrigatórias
        colunas_obrigatorias = ['nota_ccs', 'status_ccs']
        if all(col in df.columns for col in colunas_obrigatorias):
            if st.button("Atualizar Status"):
                registros_atualizados, erros = atualizar_status_em_lote(df)
                st.success(f"{registros_atualizados} registros atualizados com sucesso!")
                if erros:
                    st.warning(f"Ocorreram {len(erros)} erros:")
                    st.write(erros)
        else:
            st.error(f"O arquivo deve conter as colunas obrigatórias: {colunas_obrigatorias}")

elif aba == "Atualizar PEP":
    # Upload do arquivo Excel para atualização do PEP
    uploaded_file = st.file_uploader("Faça o upload do arquivo Excel com os peps", type=["xlsx"])
    if uploaded_file:
        # Carregar o Excel no DataFrame
        df = pd.read_excel(uploaded_file)

        # Mostrar os dados carregados
        st.write("Pré-visualização dos dados:")
        st.dataframe(df)

        # Botão para iniciar a atualização
        if st.button("Atualizar Status PEP"):
            atualizar_pep_ou_status(df, "pep", "status_pep", "pep", Obra)

elif aba == "Inserir PEP":
    # Upload do arquivo Excel para inserção de PEP
    uploaded_file2 = st.file_uploader("Faça o upload do arquivo Excel os status dos peps", type=["xlsx"])
    if uploaded_file2:
        # Carregar o Excel no DataFrame
        df2 = pd.read_excel(uploaded_file2)

        # Mostrar os dados carregados
        st.write("Pré-visualização dos dados:")
        st.dataframe(df2)

        # Botão para iniciar a atualização
        if st.button("Inserir PEP no Banco de Dados"):
            atualizar_pep_ou_status(df2, "nota_proj", "pep", "nota_proj", Obra)

elif aba == "Atualizar Datas":
    # Upload do arquivo Excel para atualização de datas
    file = st.file_uploader("Selecione o arquivo Excel com as atualizações de datas", type=["xlsx"])
    if file:
        # Ler o arquivo Excel no DataFrame
        df = pd.read_excel(file)

        # Pré-visualização
        st.write("Pré-visualização dos dados:")
        st.dataframe(df.head())

        # Verificar se a coluna de condição existe
        if "pep" in df.columns:
            if st.button("Atualizar Datas"):
                atualizar_datas(df, Obra, "pep")
        else:
            st.error("O arquivo deve conter a coluna 'pep' para identificar os registros.")
elif aba == "Validações":
    # Upload do arquivo Excel para atualização de datas
    file = st.file_uploader("Selecione o arquivo Excel com as atualizações das validações", type=["xlsx"])
    if file:
        # Ler o arquivo Excel no DataFrame
        df = pd.read_excel(file)

        # Pré-visualização
        st.write("Pré-visualização dos dados:")
        st.dataframe(df.head())

        # Verificar se a coluna de condição existe
        if "pep" in df.columns:
            if st.button("Atualizar Validações"):
                atualizar_validacao(df, Obra, "nota_proj")
        else:
            st.error("O arquivo deve conter a coluna 'nota_proj' para identificar os registros.")