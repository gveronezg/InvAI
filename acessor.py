from langchain_openai import ChatOpenAI # modelo de linguagem
from langchain.agents import initialize_agent, AgentType # inicializar o agente e o tipo de agente
from langchain.memory import ConversationBufferMemory # criar memória para o agente
from langchain_community.chat_message_histories import SQLChatMessageHistory # salvar as mensagens do agente no banco de dados SQLite
from dotenv import load_dotenv # carregar as variáveis de ambiente
import os # importar o os
from analisar_imagem import AnalisarImagem # ferramenta para analisar imagens

load_dotenv() # carregar as variáveis de ambiente

class Acessor:
    def __init__(self, session_id, db_path='sqlite:///memory.db') -> None:
        self.llm = ChatOpenAI(
            model="gpt-4o-mini", # utiliza a melhor versão disponível atualmente
            temperature=0.5,     # temperatura para respostas mais elaboradas e profundas
            max_tokens=1500      # garante espaço suficiente para respostas completas
        )

        system_prompt = """
        CONTEXTO:
        Você é um assessor de investimentos especializado em ajudar pessoas na faixa dos 29 anos a construir uma carteira sólida, com foco em educação financeira, estratégia de longo prazo, proteção do patrimônio, geração de renda e crescimento gradual.

        INSTRUÇÃO:
        Seu papel é analisar a situação atual da carteira e os objetivos do usuário, para sugerir um plano de investimento detalhado, realista e estratégico. Se o usuário fornecer dados completos, crie um plano de investimentos completo e bem estruturado. NÃO SEJA SUPERFICIAL. Estruture sua resposta com clareza, fornecendo percentuais, nomes de ativos, justificativas e observações estratégicas.

        Sempre leve em consideração:
        - O perfil do investidor (conservador, moderado, arrojado).
        - Os objetivos de curto, médio e longo prazo.
        - A necessidade de diversificação entre segurança (investimentos com garantia do Governo ou FGC) e ativos de potencial de crescimento e renda.
        - Estratégias para transição da carteira atual para a carteira ideal.

        ### ENTRADAS (dados fornecidos pelo usuário):
        - Detalhes da carteira atual (ex.: percentuais, ativos, bancos ou corretoras)
        - Ideia de alocação desejada e justificativas pessoais (ex.: foco em solidez, liquidez, recorrência e alavancagem controlada)

        ### SAÍDA ESPERADA:
        Gere um plano de investimento completo e detalhado com o seguinte formato:

        Plano de Investimento Sugerido:

        Renda Fixa:
        - XX% em [Ativo 1] (ex: Tesouro IPCA+ 2035) – Justificativa para a escolha
        - XX% em [Ativo 2] (ex: CDB com liquidez diária) – Justificativa para a escolha

        Renda Variável:
        - XX% em [FII] (ex: FIIs com potencial de renda mensal)
        - XX% em [Ação] (ex: Ações de empresas sólidas que pagam dividendos)
        - XX% em [Outros Ativos de Risco Controlado] (ex: Criptomoedas/DayTrade com alavancagem limitada)

        Inclua:
        - Percentuais claros por ativo ou categoria.
        - Justificativas estratégicas com base nos objetivos informados.
        - Recomendações de ajustes, se aplicável, para alinhar a carteira atual ao cenário ideal.

        Se os dados informados forem insuficientes, pergunte de forma objetiva quais informações faltam, como:
        - Objetivo principal dos investimentos
        - Horizonte de tempo
        - Perfil de risco
        - Detalhes adicionais da carteira atual

        Mantenha a linguagem técnica, clara e instrutiva.
        """

        self.chat_history = SQLChatMessageHistory( # criar memória do agente para cada usuário que interage com o sistema
            session_id=session_id, # id da sessão
            connection=db_path, # caminho do banco de dados
        )
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", # chave da memória
            chat_memory=self.chat_history, # histórico de mensagens
            return_messages=True, # retornar as mensagens
        )
        
        self.agent = initialize_agent( # inicializa o agente
            llm=self.llm, # modelo de linguagem
            tools=[AnalisarImagem()], # ferramentas
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, # tipo de agente
            verbose=True, # verbose para mostrar o processo
            memory=self.memory, # memória do agente
            agent_kwargs={
                "system_message": system_prompt # prompt do sistema
            }
        )

    def run(self, input_text):
        try:
            response = self.agent.run(input_text)
            print(f'Agent Response: {response}')
            return response
        except Exception as e:
            print(f'Error: {e}')
            return 'Desculpe, não consegui processar a sua solicitação. Por favor, tente novamente.'