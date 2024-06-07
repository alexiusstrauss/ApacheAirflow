from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import random
import string
import sqlite3
from typing import List
import time
import sys
import os
import uuid

# Adicionar o caminho da pasta src ao caminho do airflow
src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(src_dir)

# Definição da DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 6, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'CARGA-USUARIOS',
    default_args=default_args,
    description='DAG para carga de dados de usuários',
    schedule_interval=timedelta(hours=1),
    catchup=False,
    tags=['USUARIOS']
)

# Classe Usuario
class Usuario:
    def __init__(self, id: str, nome: str, telefone: str, email: str, status: str):
        self.id = id
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.status = status

# Repository para salvar os usuários no banco
class UsuarioRepository:
    def __init__(self, db_name: str = f'{src_dir}/carga-diaria.sqlite'):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS usuarios (
            id TEXT PRIMARY KEY,
            nome TEXT,
            telefone TEXT,
            email TEXT,
            status TEXT
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def save(self, usuario: Usuario):
        query = """
        INSERT INTO usuarios (id, nome, telefone, email, status) VALUES (?, ?, ?, ?, ?)
        """
        self.conn.execute(query, (usuario.id, usuario.nome, usuario.telefone, usuario.email, usuario.status))
        self.conn.commit()
        time.sleep(0.1)

    def count_users(self):
        query = "SELECT COUNT(*) FROM usuarios"
        cursor = self.conn.execute(query)
        return cursor.fetchone()[0]

def fetch_users(**kwargs):
    num_users = random.randint(10, 2000)
    users = []
    for _ in range(num_users):
        user_id = str(uuid.uuid4())
        nome = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=10))
        telefone = ''.join(random.choices(string.digits, k=10))
        email = f"{nome.lower()}@example.com"
        status = random.choice(['active', 'inactive'])
        users.append({'id': user_id, 'nome': nome, 'telefone': telefone, 'email': email, 'status': status})
    kwargs['ti'].xcom_push(key='users', value=users)
    kwargs['ti'].xcom_push(key='num_users', value=num_users)

def save_users(**kwargs):
    users = kwargs['ti'].xcom_pull(key='users', task_ids='fetch_users')
    repository = UsuarioRepository()
    for user_data in users:
        usuario = Usuario(**user_data)
        repository.save(usuario)

def print_summary(**kwargs):
    num_users = kwargs['ti'].xcom_pull(key='num_users', task_ids='fetch_users')
    print(f"Total de registros retornados no fetch_users: {num_users}")

def monitor_count(**kwargs):
    repository = UsuarioRepository()
    for _ in range(100):  # Aproximadamente 600 segundos de monitoramento
        total_users = repository.count_users()
        print(f"Total de usuários no banco: {total_users}")
        time.sleep(6)

# Definição das tasks
t1 = PythonOperator(
    task_id='fetch_users',
    python_callable=fetch_users,
    provide_context=True,
    dag=dag
)

t2 = PythonOperator(
    task_id='save_users',
    python_callable=save_users,
    provide_context=True,
    dag=dag
)

t3 = PythonOperator(
    task_id='monitor_count',
    python_callable=monitor_count,
    provide_context=True,
    dag=dag
)

t4 = PythonOperator(
    task_id='print_summary',
    python_callable=print_summary,
    provide_context=True,
    dag=dag
)


# Definição da ordem das tasks
t1 >> t2 >> [t3 >> t4]
