import logging
import sqlite3
import os
import html
from turtle import update
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram import Update
from database import buscar_tarefas,upgrade_db, deletar_tarefa, concluir_tarefa


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
    
    mensagem = "<b>📝 Suas Tasks:</b>\n\n"
    
    for t_id, desc, status, category, priority in tarefas:
        stars = "⭐" * priority # Cria uma string de estrelas baseada na prioridade
        icone = "✅" if status == "concluded" else "⏳"

        descricao_limpa = html.escape(desc) # Escapa caracteres especiais para evitar problemas de formatação
        category_limpa = html.escape(category) # Escapa caracteres especiais para a categoria    
        if status == 'concluded':
            mensagem += f"{t_id} {icone}  <i>{descricao_limpa}</i>\n" # Tarefa concluída com texto riscado
            mensagem += f"📂<i>{category_limpa}</i> | {stars}\n\n"
        else:
            mensagem += f"<b>{t_id} {icone}  *{descricao_limpa}*</b>\n"  # Tarefa pendente com texto em negrito
            mensagem += f"📂<i>{category_limpa}</i> | {stars}\n\n"

    mensagem += "\nUse /check [número] para marcar como concluída. Ex: /check 2"
    await update.message.reply_text(mensagem, parse_mode='HTML')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text= f"Olá {user_name}! 🚀\nSeu gerenciador de tarefas de ADS está online.\nUse /ajuda para ver o que posso fazer."
    )

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    user_input = " ".join(context.args) # Junta os argumentos em uma string única
    user_id = update.effective_user.id

    # 2. Verifica se você digitou algo
    if not user_input:
        await update.message.reply_text("❌ Erro: Digite algo após o comando. Ex: /add Nome da Tarefa | Categoria | Prioridade (1-3) | YYYY-MM-DD") 
        return


    # 3. Logica de Divisão (split) para separar descrição, categoria e prioridade
    partes = user_input.split("|")

    tarefa = partes[0].strip() # A descrição é a primeira parte, removendo espaços extras
    categoria = partes[1].strip() if len(partes) > 1 else "Geral" # Categoria é a segunda parte ou "Geral" se não for fornecida
    prioridade = partes[2].strip() if len(partes) > 2 else "1" # Prioridade é a terceira parte ou "1" se não for fornecida
    deadline = partes[3].strip() if len(partes) > 3 else None # Deadline é a quarta parte ou None se não for fornecida
   
    try:
        prioridade = int(prioridade) # Tenta converter a prioridade para inteiro

    except ValueError:
        prioridade = 1 # Se a conversão falhar, define prioridade como 1
    
    # 4. Salva a tarefa no banco de dados agora com categoria e prioridade

    try:
        with sqlite3.connect('task.db') as conn:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO task (user_id, description, category, priority, deadline) VALUES (?, ?, ?, ?, ?)
            """, (user_id, tarefa, categoria, prioridade, deadline))
            conn.commit()

            prazo_str = deadline if deadline else "No deadline set"

        # 5 Resposta pensonalizada (English practice)

        desc_limpa = html.escape(tarefa)
        cat_limpa = html.escape(categoria)
        prazo_limpo = html.escape(prazo_str)

        stars = "⭐" * prioridade # Cria uma string de estrelas baseada na prioridade
        
        texto_final = (
            f"✅ <b>Task Saved!</b>\n\n"
            f"📝 <b>Description:</b> {desc_limpa}\n"
            f"📂 <b>Category:</b> {cat_limpa}\n"
            f"🔥 <b>Priority:</b> {stars}\n"
            f"⏰ <b>Deadline:</b> {prazo_limpo}"
        )
        await update.message.reply_text(texto_final, parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"⚠️ Database Error: {e}")

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
        await update.message.reply_text("❌ Erro: /del <id da tarefa>", parse_mode='HTML')
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