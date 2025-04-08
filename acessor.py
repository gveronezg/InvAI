from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from dotenv import load_dotenv
import os

load_dotenv()

class Acessor:
    def __init__(self) -> None:
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
        
        self.agent = initialize_agent( # inicializa o agente
            llm=self.llm, # modelo de linguagem
            tools=[], # ferramentas
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, # tipo de agente
            verbose=True, # verbose para mostrar o processo
            agent_kwargs={
                "system_message": system_prompt # prompt do sistema
            }
        )

    def run(self, input_text):
        try:
            response = self.agent.run({input_text})
            print(f'Agent Response: {response}')
            return response
        except Exception as e:
            print(f'Error: {e}')
            return 'Desculpe, não consegui processar a sua solicitação. Por favor, tente novamente.'