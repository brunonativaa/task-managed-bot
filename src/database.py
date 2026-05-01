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
            category TEXT DEFAULT 'Geral',
            status TEXT DEFAULT   'pendente',
            create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP )

   """)
    conn.commit()
    print("✅Banco de dados e tabela preparados com sucesso!")

def buscar_tarefas(user_id):
    with sqlite3.connect('task.db') as conn:
        cursor = conn.cursor()
        cursor.execute(""" SELECT id, description, status 
                       FROM task 
                       WHERE user_id = ? 
                       ORDER BY status DESC, ID DESC
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
    with sqlite3.connect('task.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE task SET status = "concluída" WHERE id = ? AND user_id = ?""", (tarefa_id, user_id))
        
        sucesso = conn.total_changes > 0
        conn.commit()   
    return sucesso

if __name__ == "__main__":
    criar_tabela()  
