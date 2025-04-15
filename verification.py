from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception("Variáveis SUPABASE_URL ou SUPABASE_KEY não definidas!")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def run_verification_queries():
    print("✅ Iniciando verificação de consistência dos dados...")

    # 1. Alunos devem estar vinculados a cursos válidos
    query_1 = """
    SELECT a.nome AS aluno
    FROM aluno a
    LEFT JOIN curso c ON a.curso_id = c.id_curso
    WHERE c.id_curso IS NULL
    """
    res1 = supabase.rpc("run_sql", {"query": query_1}).execute()
    if res1.data:
        print("⚠️ Alunos sem curso válido:", res1.data)
    else:
        print("✅ Todos os alunos possuem curso válido.")

    # 2. Histórico escolar deve ter disciplinas e alunos válidos
    query_2 = """
    SELECT h.id_historico
    FROM historico_escolar h
    LEFT JOIN aluno a ON h.aluno_id = a.id_aluno
    LEFT JOIN disciplina d ON h.disciplina_id = d.id_disciplina
    WHERE a.id_aluno IS NULL OR d.id_disciplina IS NULL
    """
    res2 = supabase.rpc("run_sql", {"query": query_2}).execute()
    if res2.data:
        print("⚠️ Registros inválidos no histórico escolar:", res2.data)
    else:
        print("✅ Histórico escolar está consistente.")

    # 3. TCCs devem possuir orientadores válidos
    query_3 = """
    SELECT t.id_tcc, t.titulo
    FROM tcc t
    LEFT JOIN professor p ON t.orientador_id = p.id_professor
    WHERE p.id_professor IS NULL
    """
    res3 = supabase.rpc("run_sql", {"query": query_3}).execute()
    if res3.data:
        print("⚠️ TCCs com orientadores inexistentes:", res3.data)
    else:
        print("✅ Todos os TCCs possuem orientadores válidos.")

    # 4. Vínculos TCC-Aluno devem ser consistentes
    query_4 = """
    SELECT ta.tcc_id, ta.aluno_id
    FROM tcc_aluno ta
    LEFT JOIN tcc t ON ta.tcc_id = t.id_tcc
    LEFT JOIN aluno a ON ta.aluno_id = a.id_aluno
    WHERE t.id_tcc IS NULL OR a.id_aluno IS NULL
    """
    res4 = supabase.rpc("run_sql", {"query": query_4}).execute()
    if res4.data:
        print("⚠️ Relações TCC-Aluno inválidas:", res4.data)
    else:
        print("✅ Todos os vínculos TCC-Aluno estão corretos.")

    print("🔍 Verificação de consistência concluída.")

if __name__ == "__main__":
    run_verification_queries()
