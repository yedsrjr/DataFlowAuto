from auth import busca_sap_api_query
from database import get_session
from models import Animal, LogInsercaoAnimais
from datetime import datetime

def request_database():
    query = """
        SELECT
            an.DocEntry as docentry,
            an.U_CodigoLocalizacao baia,
            an.U_Lote lote,
            an.U_IdadeManejo idade_mes,
            an.U_Chip chip_bosch,
            an.U_NumeroSisbov num_sisbov, 
            an.U_Sexo sexo,
            rc.Name raca,
            an.U_Status status,
            ds.U_DataChegada data_entrada_fazenda,
            ma.U_Peso peso_balancinha,
            me.U_Data data_processamento,
            msn.U_Data data_saida,
            ms.U_Peso peso_saida,
            an.U_CodigoFornecedor proprietario            
        FROM [@PECU_ANML] an
        LEFT JOIN [@PECU_RACA] rc ON rc.DocEntry = an.U_CodigoRaca
        LEFT JOIN [@PECU_MEAA] ma ON ma.U_CodAnimal = an.DocEntry 
        LEFT JOIN [@PECU_MEAN] me ON me.DocEntry = ma.DocEntry 
        LEFT JOIN [@PECU_GTAC] gta ON gta.DocEntry = ma.U_CodigoGTA 
        LEFT JOIN [@PECU_DSAN] ds ON ds.U_CodigoGTA = gta.DocEntry
        LEFT JOIN [@PECU_MSAA] ms ON ms.U_CodAnimal = an.DocEntry
        LEFT JOIN [@PECU_MSAN] msn ON msn.DocEntry = ms.DocEntry
        WHERE cast(ds.U_DataChegada as DATE) > '2024-01-01'
        ORDER BY an.DocEntry DESC
    """
    dados = busca_sap_api_query(query)
    return dados[0]

def formata_dados(dados):
    print(f'Formantando dados - {datetime.now().replace(microsecond=0)}')
    for gado in dados:
        if gado['chip_bosch'] == '':
            gado['chip_bosch'] = None

        if gado['data_entrada_fazenda']:
            gado['data_entrada_fazenda'] = datetime.fromisoformat(gado['data_entrada_fazenda']).strftime("%Y-%m-%d")
        else:
            gado['data_entrada_fazenda'] = None

        if gado['data_processamento']:
            gado['data_processamento'] = datetime.fromisoformat(gado['data_processamento']).strftime("%Y-%m-%d")
        else:
            gado['data_processamento'] = None

        if gado['data_saida']:
            gado['data_saida'] = datetime.fromisoformat(gado['data_saida']).strftime("%Y-%m-%d")
        else:
            gado['data_saida'] = None
        
        if gado['sexo'] == 'F':
            gado['sexo'] = 'Fêmea'
        elif gado['sexo'] == 'M':
            gado['sexo'] = 'Macho'
        
        if gado['status'] == 'A':
            gado['status'] = 'Ativo'
        elif gado['status'] == 'V':
            gado['status'] = 'Vendido'
        elif gado['status'] == 'I':
            gado['status'] = 'Inativo'
        elif gado['status'] == 'T':
            gado['status'] = 'Em Transferência'
    print(f'Formatação de dados concluída - {datetime.now().replace(microsecond=0)}')
    return dados

def add_animal():
    with get_session() as session:
        response = request_database()
        dados = formata_dados(response)
        print(f'Inserindo dados na base - {datetime.now().replace(microsecond=0)}')
        for i, gado in enumerate(dados):
            if not isinstance(gado, dict):
                log = LogInsercaoAnimais(
                docentry=None,
                status='ERRO',
                mensagem=f"Objeto ignorado, tipo inesperado: {str(gado)}",
                data_log=datetime.now()
                )
                session.add(log)
                session.commit()
                print('ERRO DICT GADo')
                continue

            try:
                animal = Animal(
                    docentry=gado['docentry'],
                    baia=gado['baia'],
                    lote=gado['lote'],
                    idade_mes=gado['idade_mes'],
                    chip_bosch=gado['chip_bosch'],
                    num_sisbov=gado['num_sisbov'],
                    sexo=gado['sexo'],
                    raca=gado['raca'],
                    status=gado['status'],
                    data_entrada_fazenda=gado['data_entrada_fazenda'],
                    peso_balancinha=gado['peso_balancinha'],
                    data_processamento=gado['data_processamento'],
                    data_saida=gado['data_saida'],
                    peso_saida=gado['peso_saida'],
                    proprietario=gado['proprietario']
                )
                session.merge(animal)
                session.commit()

            except Exception as e:
                session.rollback()
                log = LogInsercaoAnimais(
                    docentry=gado.get('docentry'),
                    status='ERRO',
                    mensagem=f"Erro SQLAlchemy: {str(e)}",
                    data_log=datetime.now()
                )
                session.add(log)
                session.commit()
                continue  

        log = LogInsercaoAnimais(
                    docentry=200,
                    status='SUCESSO',
                    mensagem=f"Animais inseridos/atualizados com sucesso.",
                    data_log=datetime.now()
        )
        session.add(log)
        session.commit()
        print(f'Inserção de dados concluída - {datetime.now().replace(microsecond=0)}')
        #print(f'automation log-file {datetime.now().replace(microsecond=0)}\n--------------------------\n{datetime.now().replace(microsecond=0)}: Finalizado.\n')

add_animal()


