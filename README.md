# InvAI 🤖

InvAI é um robô de inteligência artificial desenvolvido para auxiliar investidores na tomada de decisões no mercado financeiro. Com base em dados atualizados, estratégias consolidadas e análise comportamental, o InvAI oferece sugestões inteligentes e personalizadas para aplicação de recursos, respeitando o perfil e os objetivos de cada investidor.

## 📋 Descrição

O InvAI é um assistente virtual que utiliza inteligência artificial avançada para fornecer orientações personalizadas sobre investimentos. O sistema é capaz de:

- Analisar o perfil do investidor
- Fornecer recomendações personalizadas de investimentos
- Monitorar o mercado financeiro em tempo real
- Avaliar riscos e oportunidades
- Sugerir estratégias de diversificação
- Analisar imagens e extrair insights financeiros

## 🚀 Funcionalidades

- **Análise de Perfil**: Avaliação personalizada do perfil do investidor
- **Recomendações Inteligentes**: Sugestões baseadas em dados do mercado
- **Monitoramento em Tempo Real**: Acompanhamento de ativos e indicadores
- **Gestão de Riscos**: Análise de risco-retorno
- **Planejamento Financeiro**: Estratégias de longo prazo

## 🛠️ Tecnologias Utilizadas

- Python 3.x
- LangChain
- OpenAI GPT-4
- APIs de Mercado Financeiro
- SQLite (para armazenamento de dados)
- Pandas (para análise de dados financeiros)

## ⚙️ Configuração

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/InvAI.git
cd InvAI
```

2. Crie e ative o ambiente virtual com o pip venv:
- Crie um ambiente virtual:
```bash
python -m venv venv
```
- Ative o ambiente virtual:
```bash
venv/Scripts/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
```bash
TELEGRAM_API_ID=seu_api_id
TELEGRAM_API_HASH=seu_api_hash
TELEGRAM_TOKEN=seu_token
OPENAI_API_KEY=sua_chave_api
```

5. Execute o sistema:
```bash
python app.py
```

## 📱 Como Usar

1. Inicie uma conversa com o bot no Telegram usando /start
2. Configure seu perfil de investidor
3. Receba recomendações personalizadas
4. Monitore seus investimentos
5. Ajuste suas estratégias conforme necessário

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor, siga estes passos:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto/código foi desenvolvido para fins educacionais e profissionais.
A distribuição deste código deve ser usada para fins pessoais e educacionais apenas.

## 👥 Autores

- Gabriel V.G. - [@gveronezg](https://github.com/gveronezg)

## 🙏 Agradecimentos

- OpenAI por fornecer a API GPT-4
- Fontes de dados do mercado financeiro