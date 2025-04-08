import base64
from io import BytesIO
from langchain.tools import BaseTool
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from PIL import Image

class AnalisarImagem(BaseTool): # criar uma ferramenta personalizada para analisar imagens
    name: str = "analisador_de_imagens" # nome da ferramenta
    description: str = "Use esta ferramenta para analisar imagens e continuar a interação com o usuário com base nos dados obtidos através dessa análise. O agente deve utilizar esta ferramenta sempre que um caminho de imagem for fornecido, mas somente quando o input for um caminho de imagem."

    def __init__(self):
        super().__init__() # inicializar a classe pai

    def _run(self, imagem_path: str):
        image = Image.open(imagem_path)
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

        instructions = f"""
        Você deve analisar a imagem fornecida e verificar se ela se trata de algo relacionado a investimentos.
        Caso positivo, descreva o que você está vendo na imagem e os detalhes e especificações do que está sendo apresentado.
        Por fim, retorne uma resposta para o usuário dando boas sugestões de investimentos com base na analise da imagem e no que o usuário almeja.
        """  # descrição do que a ferramenta deve fazer
        
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
        message = [HumanMessage( # mensagem para o modelo
            content=[
                {'type': 'text', 'text': instructions},
                {'type': 'image_url', 'image_url': {'url': f"data:image/jpeg;base64,{img_b64}"}}
            ]
        )]
        response = llm.invoke(message)
        return response.content # ou apenas response

    async def _arun(self, image_path: str) -> str:
        raise NotImplementedError("Execução assíncrona não suportada.")