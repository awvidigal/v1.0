import datetime
import sqlite3 as sql

dbName = 'agv.db'

class client:
    '''
    This class defines a client for the energy management service.
    Regardless of the proposed solution for reducing energy costs.
    '''
    def __init__(self, personType, document, name, address, city, state, phone=None, mail=None, lead=None, complement=None) -> None:
        '''
        Constructor of the class 'client'.

        :param personType: defines if the client is a natural person or a juridical person
        :param document: store the number of the clients document. CPF if is a natural person or CNPJ if is a juridic person
        :param name: the name of the client or the business name (if juridic person)
        :param address: the street and number of the client. Not necessarily the address of the UC
        :param city: the city of the client. Not necesssarily the city of the UC
        :param state: the state of the client. Not necessarily the state of the UC
        :param phone: the phone number of the client (optional. default is [None])
        :param mail: the mail address of the client (optional. default is [None])
        :param lead: if the client is a juridic person, this parameter stores the name of the person who is talking to us in name of the business (optional. default is [None])
        :param complemet: if the address has a complement, it'll be stored in this parameter {optional. default is [None]}

        :return: None
        '''
        self.document = document
        self.name = name
        self.lead = lead
        self.address = address
        self.complement = complement
        self.city = city
        self.state = state
        self.phone = phone
        self.mail = mail

        self.created_at = datetime.datetime.now()
        personTypes = ['cpf', 'cnpj']

        if personType in personTypes:
            self.personType = personType
        else:
            raise Exception('Not valid person type')

    def verifyRegister(self) -> bool:
        '''
        This method verifies if the client's  document is already registered in the database

        :return: bool
        '''
        existsIndicator = None
        if self.personType == 'pf':
            documentType = 'cpf'
        else:
            documentType = 'cnpj'
        
        # conectar ao db
        conn = sql.connect(self.dbName)
        cursor = conn.cursor()
        
        # verificar se o cpf/cnpj ja existem
        existsIndicator = cursor.execute(
            f'''
                SELECT *
                FROM clientes
                WHERE {documentType} = ?;
            ''', (self.document,)
        ).fetchone()
        conn.close()

        if existsIndicator:
            return 1
        else:
            return 0
    
    def dbInsert(self):
        '''
        This method inserts the new client in the database

        :return: None
        '''
        existsRegister = self.verifyRegister()

        if existsRegister:
            raise Exception('Cliente já cadastrado na base')
        # inserir o registro caso nao exista
        else:
            conn = sql.connect(self.dbName)
            cursor = conn.cursor()

            if self.personType == 'pf':
                cursor.execute(
                    '''
                    INSERT INTO clientes (pessoa, cpf, nome, endereco, complemento, cidade, estado, telefone, email, created_at)
                    VALUES (?,?,?,?,?,?,?,?,?,?)
                    ''', (self.personType, self.document, self.name, self.address, self.complement, self.city, self.state, self.phone, self.mail, self.created_at)
                )
            else:
                cursor.execute(
                    '''
                    INSERT INTO clientes (pessoa, cnpj, razao_social, responsavel, endereco, complemento, cidade, estado, telefone, email, created_at)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?)
                    ''', (self.personType, self.document, self.name, self.lead, self.address, self.complement, self.city, self.state, self.phone, self.mail, self.created_at)
                )

            conn.commit()
            conn.close()
        
class UC:
    '''
    This class defines a consumption unit
    '''
    def __init__(self, utilityCompany, clientID, ucNumber, subGroup, modality, demand=None, peakDemand=None, offpeakDemand=None):
        '''
        Constructor of the class UC

        :param utilityCompany: the energy utility that serves the consumption unity
        :param clientID: the client's id associated to the consumption unit
        :param ucNumber: the number of the consumption unit
        :param subGroup: the subgroup of the consumption unit. It accepts the following values:
            - 'A1'
            - 'A2'
            - 'A3'
            - 'A3a'
            - 'A4'
            - 'A5'
        :param modality: defines the taxes modality of the consumption unity. It accepts the following values:
            - Azul
            - Verde
            - Branca
            - Convencional
        : param demand: the contracted demand (optional. default[None])

        '''
        self.utilityCompany = utilityCompany
        self.clientID = clientID
        self.ucNumber = ucNumber
        self.demand = demand
        self.peakDemand = peakDemand
        self.offpeakDemand = offpeakDemand
        self.created_at = datetime.datetime.now()
        
        conn = sql.connect(dbName)
        cursor = conn.cursor()

        subGroupsList = cursor.execute(
            '''
            SELECT suggrupo
            FROM subgrupos;
            '''
        ).fetchall()

        modalitiesList = cursor.execute(
            '''
            SELECT modalidade
            FROM modalidades;
            '''
        ).fetchall()
        conn.close()

        if subGroup in subGroupsList:
            self.subGroup = subGroup
        else:
            raise Exception('Not valid subgroup')
        
        if modality in modalitiesList:
            self.modality = modality
        else:
            raise Exception('Not valid modality')
        
    def verifyRegister(self):
        existsIndicator = None
        
        conn = sql.connect(dbName)
        cursor = conn.cursor()

        existsIndicator = cursor.execute(
            '''
            SELECT *
            FROM ucs
            WHERE uc = ?;
            ''', (self.ucNumber)
        ).fetchone()
        conn.close()

        if existsIndicator:
            return 1
        else:
            return 0
    
    def insertRegister(self):
        registerExists = self.verifyRegister()
        if registerExists:
            raise Exception('Client already exists in database')
        else:
            conn = sql.connect(dbName)
            cursor = conn.cursor()

            cursor.execute(
                '''
                INSERT INTO ucs (concessionaria, cliente_id, uc, subgrupo, modalidade, demanda_contratada, demanda_contratada_ponta, demanda_contratada_fora_ponta, created_at)
                VALUES (?,?,?,?,?,?,?,?,?);
                ''', (self.utilityCompany, self.clientID, self.ucNumber, self.subGroup, self.modality, self.demand, self.peakDemand, self.offpeakDemand, self.created_at)
            )
            conn.close()

class monthlyRates:
    def __init__(self, ucID, type='consumption', **kwargs):
        self.ucID = ucID
        self.created_at = datetime.datetime.now()
        self.consumption = kwargs

        typesDict = {
            'consumption':'consumos',
            'peakConsumption':'consumos_ponta',
            'offpeakConsumprion':'consumos_fora_ponta',
            'demand':'demandas',
            'peakDemand':'demandas_ponta',
            'offpeakDemands':'demandas_fora_ponta'
        }

        if type in typesDict:
            self.type = typesDict[type]
        else:
            raise Exception('Not valid type')
        
        if not self.consumption:
            raise Exception('No values passed')


    def verifyRegister(self):
         # verifica se na tabela correspondente ao tipo já existe consumo
        existsRegister = None
        conn = sql.connect(dbName)
        cursor = conn.cursor()

        existsRegister = cursor.execute(
            '''
            SELECT *
            FROM ?
            WHERE uc_id = ?;
            ''', (self.type, self.ucID)
        ).fetchone()
        conn.close()

        if existsRegister:
            return 1
        else:
            return 0

        

    def insertRegister(self):
        valuesList = [self.type]
        keysList = self.consumption.keys()
        valuesList.append(list(keysList))
        valuesList.append(self.ucID)

        existsRegister = None
        existsRegister = self.verifyRegister()

        if existsRegister:
            setClause = ', '.join(f'{column} = ?' for column in self.consumption)
                        
            conn = sql.connect(dbName)
            cursor = conn.cursor()
            cursor.execute(
                f'''
                UPDATE ?
                {setClause}
                WHERE uc_id = ?;
                ''', valuesList
            )
            conn.commit()
            conn.close()
        
        else:            
            insertClause = ', '.join(month for month in list(self.consumption.keys()))
            monthsConsumption = list(self.consumption.values())
            
            conn = sql.connect(dbName)
            cursor = conn.cursor()

            cursor.execute(
                f'''
                INSERT INTO ? ({insertClause}) 
                VALUES ({monthsConsumption});
                ''', (self.type,)
            )
            conn.commit()
            conn.close()