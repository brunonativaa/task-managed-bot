import logging
import sqlite3
import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram import Update
from database import buscar_tarefas, deletar_tarefa, concluir_tarefa


load_dotenv()  # Carrega as variáveis do arquivo .env
TOKEN = os.getenv('TELEGRAM_TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    tarefas = buscar_tarefas(user_id)


    if not tarefas:
        await update.message.reply_text('📝 Sua lista esá vazia!')
        return
    
    mensagem = "📝 **Suas tarefas:**\n\n"
    
    for item in tarefas:
        t_id, desc, status = item # Desempacotando os valores da tupla
        icone = "✅" if status == "concluída" else "⏳"
        
        if status == 'concluída':
            mensagem += f"#{t_id} {icone}  _{desc}_\n" # Tarefa concluída com texto riscado
        else:
            mensagem += f"#{t_id} {icone}  *{desc}*\n"  # Tarefa pendente com texto em negrito
    
    mensagem += "\nUse /check [número] para marcar como concluída. Ex: /check 2"

    await update.message.reply_text(mensagem, parse_mode='Markdown')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text= f"Olá {user_name}! 🚀\nSeu gerenciador de tarefas de ADS está online.\nUse /ajuda para ver o que posso fazer."
    )

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 1. Pega o que você digitou depois do /add
    # context.args transforma o texto em uma lista, o join junta tudo de novo
    tarefa = " ".join(context.args)
    user_id = update.effective_user.id

    # 2. Verifica se você digitou algo
    if not tarefa:
        await update.message.reply_text("❌ Erro: Digite algo após o comando. Ex: /add Estudar SQL")
        return

    # 3. Salva no banco de dados
    try:
        with sqlite3.connect('task.db') as conn: # Conecta ao banco de dados
            cursor = conn.cursor()
            cursor.execute('INSERT INTO task (user_id, description) VALUES (?, ?)', (user_id, tarefa))
            conn.commit()

        # 4. Responde para você no Telegram
        await update.message.reply_text(f"✅ Salvei na sua lista: {tarefa}")
    
    except Exception as e:
        await update.message.reply_text(f"⚠️ Erro ao acessar o banco: {e}")

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not context.args:
        await update.message.reply_text("❌ Erro: Digite o número da tarefa a concluir. Ex: /check 2")
        return
    
    try:
        tarefa_id = int(context.args[0]) # Pega o número da tarefa que você quer concluir

        if concluir_tarefa(tarefa_id, user_id):
            await update.message.reply_text(f"✅ Tarefa {tarefa_id} marcada como concluída!")
        
        else:
            await update.message.reply_text(f"⚠️ Tarefa {tarefa_id} não encontrada ou já concluída.")

    except ValueError:
        await update.message.reply_text("❌ Erro: O número da tarefa deve ser um inteiro. Ex: /check 2")        

async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not context.args:
        await update.message.reply_text("❌ Erro: /del <id da tarefa>", parse_mode='Markdown')
        return
    
    
    try:
        tarefa_id = int(context.args[0]) # Pega o número da tarefa que você quer deletar
        
        sucesso = deletar_tarefa(tarefa_id, user_id)

        if sucesso:
            await update.message.reply_text(f"✅ Tarefa {tarefa_id} removida com sucesso!")

        else:
            await update.message.reply_text(f"⚠️ Tarefa {tarefa_id} não encontrada.")

    except ValueError:
        await update.message.reply_text("❌ O ID deve ser um número inteiro.")

    except Exception as e:
        await update.message.reply_text(f"⚠️ Erro ao acessar o banco: {e}")


if __name__ == '__main__':

    if not TOKEN:
        print("❌ Erro: TELEGRAM_TOKEN não encontrado.")
        
    else:   
        application = ApplicationBuilder().token(TOKEN).build()
   
   
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('add', add))
    application.add_handler(CommandHandler('list', list_tasks))
    application.add_handler(CommandHandler('check', check))
    application.add_handler(CommandHandler('del', delete))

    

    print("Bot iniciado... Pressione Ctrl+C para desligar.")
    application.run_polling()