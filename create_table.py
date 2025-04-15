import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def create_tables():
    queries = [
        # 1 - Criar sequência para RA do aluno (inicia em 100)
        """
        CREATE SEQUENCE IF NOT EXISTS seq_ra_aluno START 100;
        """,

        # 2 - PROFESSOR (id gerado automaticamente)
        """
        CREATE TABLE IF NOT EXISTS PROFESSOR (
            id_professor SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            ra VARCHAR(20) UNIQUE NOT NULL
        );
        """,

        # 3 - DEPARTAMENTO (id gerado automaticamente)
        """
        CREATE TABLE IF NOT EXISTS DEPARTAMENTO (
            id_departamento SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            chefe_id INT,
            FOREIGN KEY (chefe_id) REFERENCES PROFESSOR(id_professor)
        );
        """,

        # 4 - CURSO (id gerado automaticamente)
        """
        CREATE TABLE IF NOT EXISTS CURSO (
            id_curso SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            coordenador_id INT,
            departamento_id INT,
            FOREIGN KEY (coordenador_id) REFERENCES PROFESSOR(id_professor),
            FOREIGN KEY (departamento_id) REFERENCES DEPARTAMENTO(id_departamento)
        );
        """,

        # 5 - ALUNO (id e ra gerados automaticamente)
        """
        CREATE TABLE IF NOT EXISTS ALUNO (
            id_aluno SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            ra VARCHAR(20) UNIQUE NOT NULL DEFAULT nextval('seq_ra_aluno'),
            data_nascimento DATE
        );
        """,

        # 6 - DISCIPLINA (id gerado automaticamente)
        """
        CREATE TABLE IF NOT EXISTS DISCIPLINA (
            id_disciplina SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            creditos INT
        );
        """,

        # 7 - HISTORICO_ESCOLAR (id gerado automaticamente)
        """
        CREATE TABLE IF NOT EXISTS HISTORICO_ESCOLAR (
            id_historico SERIAL PRIMARY KEY,
            aluno_id INT NOT NULL,
            disciplina_id INT NOT NULL,
            semestre VARCHAR(10) NOT NULL,
            ano INT NOT NULL,
            nota DECIMAL(4,2),
            situacao VARCHAR(20),
            FOREIGN KEY (aluno_id) REFERENCES ALUNO(id_aluno),
            FOREIGN KEY (disciplina_id) REFERENCES DISCIPLINA(id_disciplina)
        );
        """,

        # 8 - HISTORICO_PROFESSOR (id gerado automaticamente)
        """
        CREATE TABLE IF NOT EXISTS HISTORICO_PROFESSOR (
            id_hist_prof SERIAL PRIMARY KEY,
            professor_id INT NOT NULL,
            disciplina_id INT NOT NULL,
            semestre VARCHAR(10) NOT NULL,
            ano INT NOT NULL,
            FOREIGN KEY (professor_id) REFERENCES PROFESSOR(id_professor),
            FOREIGN KEY (disciplina_id) REFERENCES DISCIPLINA(id_disciplina)
        );
        """,

        # 9 - MATRIZ_CURRICULAR (id gerado automaticamente)
        """
        CREATE TABLE IF NOT EXISTS MATRIZ_CURRICULAR (
            id_matriz SERIAL PRIMARY KEY,
            curso_id INT NOT NULL,
            disciplina_id INT NOT NULL,
            semestre_oferta INT NOT NULL,
            FOREIGN KEY (curso_id) REFERENCES CURSO(id_curso),
            FOREIGN KEY (disciplina_id) REFERENCES DISCIPLINA(id_disciplina)
        );
        """,

        # 10 - TCC (id gerado automaticamente)
        """
        CREATE TABLE IF NOT EXISTS TCC (
            id_tcc SERIAL PRIMARY KEY,
            titulo VARCHAR(200) NOT NULL,
            orientador_id INT NOT NULL,
            FOREIGN KEY (orientador_id) REFERENCES PROFESSOR(id_professor)
        );
        """,

        # 11 - TCC_ALUNO (chave composta, sem SERIAL)
        """
        CREATE TABLE IF NOT EXISTS TCC_ALUNO (
            tcc_id INT NOT NULL,
            aluno_id INT NOT NULL,
            PRIMARY KEY (tcc_id, aluno_id),
            FOREIGN KEY (tcc_id) REFERENCES TCC(id_tcc),
            FOREIGN KEY (aluno_id) REFERENCES ALUNO(id_aluno)
        );
        """
    ]

    for i, query in enumerate(queries):
        print(f"Executando criação da tabela ({i+1}/{len(queries)})...")
        res = supabase.rpc("run_sql", {"query": query}).execute()
        print("Resultado:", res.data)

if __name__ == "__main__":
    create_tables()
