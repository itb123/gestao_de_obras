import streamlit as st
import pandas as pd
from io import BytesIO
from sqlalchemy.orm import sessionmaker
from bd import Cliente, Obra, Programacao, session

st.write("Upload de arquivo para Banco de Dados")

# Função para validar se as colunas necessárias estão presentes
def validar_colunas(df, colunas_necessarias):
    return all(col in df.columns for col in colunas_necessarias)

# Função para verificar se o registro já existe
def registro_existe(model, **kwargs):
    return session.query(model).filter_by(**kwargs).first() is not None

# Função para gerar o relatório Excel
def gerar_relatorio_excel(registros_salvos, registros_nao_salvos):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        pd.DataFrame(registros_salvos).to_excel(writer, sheet_name='Registros Salvos', index=False)
        pd.DataFrame(registros_nao_salvos).to_excel(writer, sheet_name='Registros Não Salvos', index=False)
    output.seek(0)
    return output

# Função genérica para processar e salvar registros
def processar_e_salvar(df, colunas_necessarias, modelo, campos_mapeados, chave_unica, nome_arquivo):
    registros_salvos = []
    registros_nao_salvos = []

    # Validar colunas
    if not validar_colunas(df, colunas_necessarias):
        st.error(f"O arquivo não contém todas as colunas obrigatórias para {nome_arquivo}.")
        return

    # Loop para salvar os registros
    for i, row in df.iterrows():
        try:
            if not registro_existe(modelo, **{chave_unica: row[chave_unica]}):
                registro = modelo(**{campo: row[excel_coluna] for campo, excel_coluna in campos_mapeados.items()})
                session.add(registro)
                registros_salvos.append(row.to_dict())
            else:
                registros_nao_salvos.append({**row.to_dict(), "motivo": "Registro já existe no banco."})
        except Exception as e:
            registros_nao_salvos.append({**row.to_dict(), "motivo": f"Erro: {str(e)}"})

    # Commit no banco de dados
    try:
        session.commit()
        st.success(f"Processamento de {nome_arquivo} concluído!")
    except Exception as e:
        session.rollback()
        st.error(f"Erro ao salvar os dados no banco para {nome_arquivo}: {str(e)}")
        return

    # Gerar relatório Excel
    output = gerar_relatorio_excel(registros_salvos, registros_nao_salvos)
    st.download_button(
        label=f"Baixar relatório de {nome_arquivo}",
        data=output,
        file_name=f"relatorio_{nome_arquivo.lower()}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# Processamento do arquivo de Clientes
file_clientes = st.file_uploader("Arquivo Clientes", type=["xlsx"])
if file_clientes:
    df_clientes = pd.read_excel(file_clientes)
    df_clientes = df_clientes.astype({'data_solicitacao': 'str', 'data_aceite': 'str', 'prazo_nota': 'str', 'data_ligacao': 'str'})
    st.dataframe(df_clientes.head())

    colunas_clientes = [
        'nota_ccs', 'status_ccs', 'projeto', 'data_solicitacao', 
        'data_aceite', 'cidade', 'prazo_nota', 'motivo_susp', 
        'reclamacao', 'ouvidoria', 'data_ligacao', 'status_projeto', 
        'motivo_expurgo', 'dias_susp'
    ]
    campos_clientes = {
        'nota_ccs': 'nota_ccs',
        'status_ccs': 'status_ccs',
        'projeto': 'projeto',
        'data_solicitacao': 'data_solicitacao',
        'data_aceite': 'data_aceite',
        'cidade': 'cidade',
        'prazo_nota': 'prazo_nota',
        'motivo_susp': 'motivo_susp',
        'reclamacao': 'reclamacao',
        'ouvidoria': 'ouvidoria',
        'data_ligacao': 'data_ligacao',
        'status_projeto': 'status_projeto',
        'motivo_expurgo': 'motivo_expurgo',
        'dias_susp': 'dias_susp'
    }
    if st.button("Salvar Clientes"):
        processar_e_salvar(df_clientes, colunas_clientes, Cliente, campos_clientes, 'nota_ccs', "Clientes")

# Processamento do arquivo de Obras
file_obras = st.file_uploader("Arquivo Obras", type=["xlsx"])
if file_obras:
    df_obras = pd.read_excel(file_obras)
    df_obras = df_obras.astype({
        'data_criacao_pep': 'str', 'data_aber_log': 'str', 
        'data_lib_log': 'str', 'data_lib_atec': 'str', 
        'data_lib_ener': 'str', 'data_envio_validacao': 'str', 
        'data_retorno_validacao': 'str'
    })
    st.dataframe(df_obras.head())

    colunas_obras = [
        'nota_proj', 'pep', 'status_pep', 'parceira_execucao', 'descricao',
        'valor', 'trafo', 'rede_mt', 'rede_bt', 'poste', 'tipo_de_obra', 
        'estudo_ambiental', 'data_criacao_pep', 'data_aber_log', 
        'data_lib_log', 'data_lib_atec', 'data_lib_ener', 'data_envio_validacao', 
        'data_retorno_validacao', 'parceira_validacao', 'retorno_validacao'
    ]
    campos_obras = {
        'nota_proj': 'nota_proj',
        'pep': 'pep',
        'status_pep': 'status_pep',
        'parceira_execucao': 'parceira_execucao',
        'descricao': 'descricao',
        'valor': 'valor',
        'trafo': 'trafo',
        'rede_mt': 'rede_mt',
        'rede_bt': 'rede_bt',
        'poste': 'poste',
        'tipo_de_obra': 'tipo_de_obra',
        'estudo_ambiental': 'estudo_ambiental',
        'data_criacao_pep': 'data_criacao_pep',
        'data_aber_log': 'data_aber_log',
        'data_lib_log': 'data_lib_log',
        'data_lib_atec': 'data_lib_atec',
        'data_lib_ener': 'data_lib_ener',
        'data_envio_validacao': 'data_envio_validacao',
        'data_retorno_validacao': 'data_retorno_validacao',
        'parceira_validacao': 'parceira_validacao',
        'retorno_validacao': 'retorno_validacao'
    }
    if st.button("Salvar Obras"):
        processar_e_salvar(df_obras, colunas_obras, Obra, campos_obras, 'nota_proj', "Obras")

# Processamento do arquivo de Programação
file_programacao = st.file_uploader("Arquivo Programação", type=["xlsx"])
if file_programacao:
    df_programacao = pd.read_excel(file_programacao)
    df_programacao = df_programacao.astype({'data_programacao': 'str', 'retorno_programacao': 'str'})
    st.dataframe(df_programacao.head())

    colunas_programacao = ['nota_proj', 'data_programacao', 'retorno_programacao']
    campos_programacao = {
        'nota_proj': 'nota_proj',
        'data_programacao': 'data_programacao',
        'retorno_programacao': 'retorno_programacao'
    }
    if st.button("Salvar Programação"):
        processar_e_salvar(df_programacao, colunas_programacao, Programacao, campos_programacao, 'nota_proj', "Programação")
