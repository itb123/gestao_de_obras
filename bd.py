from sqlalchemy import create_engine, Column, String, Integer, Float,ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.event import listens_for

db = create_engine("sqlite:///teste.db") #criação do banco
Session = sessionmaker(bind=db)#criação da sessao
session = Session()#instanciação da sessao

Base = declarative_base()

class Obra(Base):
    __tablename__ = "obras"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nota_proj = Column("nota_proj",String)
    pep = Column("pep",String,nullable=True)
    status_pep = Column("status_pep",String,nullable=True)
    parceira = Column("parceira",String,nullable=True)
    descricao = Column("descricao",String)
    valor = Column("valor",Float)
    trafo = Column("trafo", Integer)
    rede_mt = Column("rede_mt",Float)
    rede_bt = Column("rede_bt",Float)
    poste = Column("poste", Integer)
    tipo_de_obra = Column("tipo_de_obra", Integer)
    estudo_ambiental = Column("estudo_ambiental",String,nullable=True)
    data_criacao_pep = Column("data_criacao_pep",String,nullable=True)
    data_aber_log = Column("data_aber_log",String,nullable=True)
    data_lib_log = Column("data_lib_log",String,nullable=True)
    data_lib_atec = Column("data_lib_atec",String,nullable=True)
    data_lib_ener = Column("data_lib_ener",String,nullable=True)
    data_envio_validacao = Column("data_envio_validacao",String,nullable=True)
    parceira_validacao=Column("parceira_validacao",String,nullable=True)
    retorno_validcao=Column("retorno_validacao",String,nullable=True)
    data_retorno_validacao = Column("data_retorno_validacao",String,nullable=True)


class Programacao(Base):
    __tablename__ = "programacoes"

    id = Column("id", Integer,primary_key=True, autoincrement=True)
    nota_proj=Column("projeto",String, ForeignKey("obras.nota_proj"))
    data_programacao=Column("data_programacao",String)
    retorno_programacao=Column("retorno_programacao", String,nullable=True)

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column("id", Integer, primary_key=True,autoincrement=True)
    nota_ccs=Column("nota_ccs",String,unique=True)
    status_ccs=Column("status_ccs", String)
    projeto=Column("projeto",String, ForeignKey("obras.nota_proj"))
    status_projeto=Column("status_projeto",String,)
    data_solicitacao=Column("data_solicitacao",String)
    data_aceite=Column("data_aceite",String,nullable=True)
    data_ligacao=Column("data_ligacao",String,nullable=True)
    dias_susp=Column('dias_susp',Integer,nullable=True)
    cidade=Column("cidade", String)
    prazo_nota=Column("prazo_nota",String,nullable=True)
    motivo_susp=Column("motivo_susp", String,nullable=True)
    motivo_expurgo=Column("motivo_expurgo",String,nullable=True)
    reclamacao=Column("reclamacao", String,nullable=True)
    ouvidoria=Column("ouvidoria", String,nullable=True)

Base.metadata.create_all(bind=db)

#CRUD - CREATE READ UPDATE DELETE
#CREATE
'''
obra = Obra(nota_proj='420126468',pep='AL-2401112UNR1.2.1441',status_pep='LIB/LOG',parceira='DINAMO',cidade='PAO DE ACUCAR',descricao='ME-UNR-PDA-CC-3003063819-VALDIRAN-OLIVEIRA',
            valor=18853.4,trafo=1,rede_mt=0,rede_bt=0.191,poste=6,tipo_de_obra=1,
            estudo_ambiental=None,data_criacao_pep=None,data_aber_log=None,data_lib_log=None,data_lib_atec=None,data_lib_ener=None,data_envio_validacao=None,data_retorno_validacao=None)

session.add(obra)
session.commit()
'''
#READ
