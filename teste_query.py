import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_ids():
    ids = {}

    aluno = supabase.table("aluno").select("id_aluno").eq("nome", "Fernanda Costa").execute()
    ids["aluno_id"] = aluno.data[0]["id_aluno"] if aluno.data else None

    professor = supabase.table("professor").select("id_professor").eq("ra", "I001").execute()
    ids["professor_id"] = professor.data[0]["id_professor"] if professor.data else None

    curso1 = supabase.table("curso").select("id_curso").eq("nome", "Engenharia de Software").execute()
    curso2 = supabase.table("curso").select("id_curso").eq("nome", "Biologia Molecular").execute()
    ids["curso_id_1"] = curso1.data[0]["id_curso"] if curso1.data else None
    ids["curso_id_2"] = curso2.data[0]["id_curso"] if curso2.data else None

    return ids

# --- QUERIES DO ENUNCIADO ---
def query_1_historico_reprovacao_aprovacao(student_id: int):
    query = f"""
    SELECT h1.aluno_id,
           h1.disciplina_id,
           h1.semestre AS semestre_reprovado,
           h1.nota AS nota_reprovado,
           h2.semestre AS semestre_aprovado,
           h2.nota AS nota_aprovado
    FROM historico_escolar h1
    JOIN historico_escolar h2
      ON h1.aluno_id = h2.aluno_id
     AND h1.disciplina_id = h2.disciplina_id
    WHERE h1.situacao = 'reprovado'
      AND h2.situacao = 'aprovado'
      AND h1.aluno_id = {student_id}
    """
    return supabase.rpc("run_sql", {"query": query}).execute().data

def query_2_tccs_professor(professor_id: int):
    query = f"""
    SELECT 
        t.titulo AS tcc,
        a.nome AS aluno,
        p.nome AS orientador,
        c.nome AS curso
    FROM tcc t
    JOIN professor p ON t.orientador_id = p.id_professor
    JOIN tcc_aluno ta ON ta.tcc_id = t.id_tcc
    JOIN aluno a ON ta.aluno_id = a.id_aluno
    JOIN curso c ON a.curso_id = c.id_curso
    WHERE p.id_professor = {professor_id}
    """
    return supabase.rpc("run_sql", {"query": query}).execute().data

def query_3_matriz_curricular(course_id: int):
    query = f"""
    SELECT c.nome AS curso,
           d.nome AS disciplina,
           m.semestre_oferta
    FROM matriz_curricular m
    JOIN curso c ON m.curso_id = c.id_curso
    JOIN disciplina d ON m.disciplina_id = d.id_disciplina
    WHERE c.id_curso = {course_id}
    """
    return supabase.rpc("run_sql", {"query": query}).execute().data

def query_4_disciplinas_professores(student_id: int):
    query = f"""
    SELECT DISTINCT d.id_disciplina,
           d.nome AS disciplina,
           p.nome AS professor
    FROM historico_escolar h
    JOIN disciplina d ON h.disciplina_id = d.id_disciplina
    JOIN historico_professor hp ON d.id_disciplina = hp.disciplina_id
    JOIN professor p ON hp.professor_id = p.id_professor
    WHERE h.aluno_id = {student_id}
    """
    return supabase.rpc("run_sql", {"query": query}).execute().data

def query_5_chefes_coordenadores():
    query = """
    SELECT p.nome AS professor,
           COALESCE(dep.nome, 'nenhum') AS departamento,
           COALESCE(c.nome, 'nenhum') AS curso
    FROM professor p
    LEFT JOIN departamento dep ON p.id_professor = dep.chefe_id
    LEFT JOIN curso c ON p.id_professor = c.coordenador_id
    """
    return supabase.rpc("run_sql", {"query": query}).execute().data

# --- QUERIES ADICIONAIS ---
def query_01_nomes_estudantes():
    return supabase.rpc("run_sql", {
        "query": "SELECT nome FROM aluno"
    }).execute().data

def query_02_ids_professores():
    return supabase.rpc("run_sql", {
        "query": "SELECT id_professor, nome FROM professor"
    }).execute().data

def query_03_cursos_credito_maior_3():
    return supabase.rpc("run_sql", {
        "query": """
        SELECT DISTINCT c.nome
        FROM curso c
        JOIN matriz_curricular m ON c.id_curso = m.curso_id
        JOIN disciplina d ON m.disciplina_id = d.id_disciplina
        WHERE d.creditos > 3
        """
    }).execute().data

def query_05_departamentos_maior_50k():
    return supabase.rpc("run_sql", {
        "query": "SELECT * FROM departamento WHERE orcamento > 50000"
    }).execute().data

def query_06_salas_100():
    return supabase.rpc("run_sql", {
        "query": "SELECT * FROM sala_de_aula WHERE capacidade = 100"
    }).execute().data

def query_11_cursos_outono_primavera():
    return supabase.rpc("run_sql", {
        "query": """
        SELECT c.nome AS curso, d.nome AS disciplina, m.semestre_oferta
        FROM matriz_curricular m
        JOIN curso c ON m.curso_id = c.id_curso
        JOIN disciplina d ON m.disciplina_id = d.id_disciplina
        WHERE m.semestre_oferta IN (1, 2)
        ORDER BY c.nome, m.semestre_oferta
        """
    }).execute().data

def query_20_salas_dr_john():
    return supabase.rpc("run_sql", {
        "query": """
        SELECT d.nome AS disciplina, sa.predio, sa.numero_sala
        FROM disciplina_sala ds
        JOIN sala_de_aula sa ON ds.sala_id = sa.id_sala
        JOIN disciplina d ON ds.disciplina_id = d.id_disciplina
        JOIN historico_professor hp ON d.id_disciplina = hp.disciplina_id
        JOIN professor p ON hp.professor_id = p.id_professor
        WHERE p.nome ILIKE '%Dr. John%'
        """
    }).execute().data

def query_21_cursos_por_prof_ra_i001():
    return supabase.rpc("run_sql", {
        "query": """
        SELECT p.nome AS professor, c.nome AS curso
        FROM curso c
        JOIN curso_professor cp ON cp.curso_id = c.id_curso
        JOIN professor p ON cp.professor_id = p.id_professor
        WHERE p.ra = 'I001'
        """
    }).execute().data

def query_27_total_creditos_por_aluno():
    return supabase.rpc("run_sql", {
        "query": """
        SELECT a.id_aluno, a.nome, SUM(d.creditos) AS total_creditos
        FROM historico_escolar h
        JOIN aluno a ON a.id_aluno = h.aluno_id
        JOIN disciplina d ON d.id_disciplina = h.disciplina_id
        WHERE h.situacao = 'aprovado'
        GROUP BY a.id_aluno, a.nome
        """
    }).execute().data

def query_42_num_alunos_por_curso():
    return supabase.rpc("run_sql", {
        "query": """
        SELECT c.nome AS curso, COUNT(a.id_aluno) AS total_alunos
        FROM curso c
        LEFT JOIN aluno a ON a.curso_id = c.id_curso
        GROUP BY c.nome
        """
    }).execute().data

# --- EXECUÇÃO DE TODAS AS QUERIES ---
def main():
    ids = get_ids()

    queries = [
        ("Query 1: Histórico Reprovação e Aprovação", query_1_historico_reprovacao_aprovacao(ids["aluno_id"])),
        ("Query 2: TCCs do Professor", query_2_tccs_professor(ids["professor_id"])),
        ("Query 3.1: Matriz Curso 1", query_3_matriz_curricular(ids["curso_id_1"])),
        ("Query 3.2: Matriz Curso 2", query_3_matriz_curricular(ids["curso_id_2"])),
        ("Query 4: Disciplinas cursadas + Professores", query_4_disciplinas_professores(ids["aluno_id"])),
        ("Query 5: Chefes e Coordenadores", query_5_chefes_coordenadores()),
        ("Query 01: Nomes dos Estudantes", query_01_nomes_estudantes()),
        ("Query 02: IDs e Nomes de Professores", query_02_ids_professores()),
        ("Query 03: Cursos com mais de 3 créditos", query_03_cursos_credito_maior_3()),
        ("Query 05: Departamentos com orçamento > 50K", query_05_departamentos_maior_50k()),
        ("Query 06: Salas com capacidade = 100", query_06_salas_100()),
        ("Query 11: Cursos Outono/Primavera", query_11_cursos_outono_primavera()),
        ("Query 20: Salas do Dr. John", query_20_salas_dr_john()),
        ("Query 21: Cursos ministrados por 'I001'", query_21_cursos_por_prof_ra_i001()),
        ("Query 27: Créditos por Aluno", query_27_total_creditos_por_aluno()),
        ("Query 42: Nº de alunos por curso", query_42_num_alunos_por_curso())
    ]

    for title, data in queries:
        print(f"\n==== {title} ====")
        if data:
            for row in data:
                print(row)
        else:
            print("Nenhum resultado.")

if __name__ == "__main__":
    main()
