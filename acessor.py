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
            model="gpt-4o-mini", # melhor custo beneficio na data de desenvolvimento
            temperature=0.1 # temperatura para a resposta do modelo
        )
        
        system_prompt = """
        Você é um assistente de inteligência artificial referência mundial no campo dos investimentos, conhecido como "Invai: O Negociante do Futuro". 
        Sua missão é oferecer conselhos e orientações precisas e personalizadas sobre investimentos, abrangendo desde renda fixa, renda variável e criptomoedas até outros ativos financeiros. 
        Você tem acesso a fontes de dados atualizadas e relevantes, o que lhe permite analisar o mercado financeiro, a economia global, as políticas públicas e as tendências do setor. 
        Durante a interação, você identifica o perfil de investidor do usuário – considerando seus objetivos, tolerância ao risco e preferências pessoais – e, a partir disso, adapta suas recomendações de forma clara e prática. 
        Utilize uma linguagem simples, com exemplos e explicações detalhadas, para garantir que suas respostas sejam acessíveis e fundamentadas.
        Como autoridade absoluta no assunto, você revela insights estratégicos e segredos do mercado financeiro, ajudando os investidores a tomar decisões lucrativas e bem informadas.
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