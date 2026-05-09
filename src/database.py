import sqlite3

def criar_tabela():

    
    with sqlite3.connect('task.db') as conn:
        cursor = conn.cursor()


        cursor.execute("""
        CREATE TABLE IF NOT EXISTS task (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            description TEXT NOT NULL,
            deadline DATETIME,
            category TEXT DEFAULT 'General',
            priority INTEGER DEFAULT 1,
            status TEXT DEFAULT   'pending',
            create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP )

   """)
        conn.commit()
        print("✅Banco de dados e tabela preparados com sucesso!")


def upgrade_db():
    conn = sqlite3.connect('task.db')
    cursor = conn.cursor()

    try:
        cursor.execute("ALTER TABLE task ADD COLUMN category TEXT DEFAULT 'Geral'")
        cursor.execute("ALTER TABLE task ADD COLUMN priority INTEGER DEFAULT 1")
        conn.commit()

    except sqlite3.OperationalError as e:
        print(f"Erro ao atualizar o banco de dados: {e}")
    
    conn.close()


def buscar_tarefas(user_id):
    with sqlite3.connect('task.db') as conn:
        cursor = conn.cursor()
        cursor.execute(""" SELECT id, description, status, category, priority 
                       FROM task 
                       WHERE user_id = ? 
                       ORDER BY status DESC, priority DESC, id DESC
                       """, (user_id,))
        tarefas = cursor.fetchall()
    return tarefas
    
def deletar_tarefa(tarefa_id, user_id):

    try:
        with sqlite3.connect('task.db') as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM task WHERE id = ? AND user_id = ?', (tarefa_id, user_id))
            conn.commit()

        return conn.total_changes > 0 # Retorna True se uma linha foi deletada, False caso contrário

    except Exception as e:
        print(f"Erro ao acessar o banco: {e}")
        return False
    
        
def concluir_tarefa(tarefa_id, user_id):
   try: 
       with sqlite3.connect('task.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE task SET status = "concluded" WHERE id = ? AND user_id = ?""", (tarefa_id, user_id))
        
        sucesso = conn.total_changes > 0
        conn.commit()   
        return sucesso
   except Exception as e:
        print(f"Erro ao acessar o banco: {e}")
        return False

if __name__ == "__main__":
    criar_tabela()  
