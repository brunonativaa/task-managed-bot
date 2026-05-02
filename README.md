# 🤖 Task Manager Bot (Telegram)

Projeto desenvolvido para gerenciar listas de tarefas diretamente pelo Telegram, facilitando a organização diária de forma rápida e acessível.

## Imagens/Gif

![Interface do Banco de Dados no DBeaver](./img/Screenshot%202026-05-02%20102549.png)
![Interface do Banco de Dados no DBeaver](./img/Bot-telegram-atualizado5-gif.gif)


## 🚀 O que eu aprendi neste projeto

Neste desenvolvimento, foquei em integrar lógica de backend com uma interface de usuário via API de mensagens. Os principais aprendizados foram:

*   **Integração com API do Telegram:** Configuração e manipulação de mensagens em tempo real.
*   **Manipulação de Banco de Dados (SQLite):** Criação de tabelas, inserção, consulta e exclusão de tarefas de forma persistente.
*   **Lógica de Programação em Python:** Uso de bibliotecas para automação e gerenciamento de estados do bot.
*   **Versionamento e Segurança:** Uso de variáveis de ambiente (arquivos `.env`) para proteger tokens sensíveis e configuração de `.gitignore`.

## 🛠️ Tecnologias Utilizadas

*   **Linguagem:** Python 3.x
*   **Banco de Dados:** SQLite3
*   **Bibliotecas Principais:** `python-telegram-bot`, `python-dotenv`
*   **Ferramentas:** VS Code, Git e GitHub

## 📋 Funcionalidades

- [x] Adicionar novas tarefas via comando.
- [x] Listar tarefas pendentes.
- [x] Marcar tarefas como concluídas ou removê-las.
- [ ] *Próximo passo: Sistema de prioridades ou categorias.*



## Desafios Enfrentados

* ** Versionamento e Segurança: Encontrei dificuldades em instalar o python-dotenv com o Poetry pelo fato de eu ter movido este projeto do meu repositório de estudos para um repositório próprio.

* ** Sintaxe SQL e Organização: Conseguir encontrar e resolver problemas de sintaxe no SQL com mais facilidade já é um bom sinal. Também resolvi enfrentar o desafio de organizar as pastas do projeto com hierarquia; começar com bons costumes é sempre bom.

## 🔧 Como executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/brunonativaa/bot-gerenciado-tarefas.git