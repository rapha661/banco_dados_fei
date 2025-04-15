from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

ids = {}

def insert_full_data():
    # ---------- PROFESSORES ----------
    professores = [
        {"nome": "Dr. John", "ra": "I001"},
        {"nome": "Alice Mendes", "ra": "I002"},
        {"nome": "Bruno Lima", "ra": "I003"},
        {"nome": "Carla Dias", "ra": "I004"}
    ]
    res = supabase.table("professor").insert(professores).execute()
    ids["professores"] = {p["ra"]: p["id_professor"] for p in res.data}

    # ---------- DEPARTAMENTOS ----------
    departamentos = [
        {"nome": "Departamento de Engenharia", "chefe_id": ids["professores"]["I002"], "orcamento": 100000.00},
        {"nome": "Departamento de Ciências", "chefe_id": ids["professores"]["I003"], "orcamento": 75000.00}
    ]
    res = supabase.table("departamento").insert(departamentos).execute()
    ids["departamentos"] = {d["nome"]: d["id_departamento"] for d in res.data}

    # ---------- CURSOS ----------
    cursos = [
        {"nome": "Engenharia de Software", "coordenador_id": ids["professores"]["I002"], "departamento_id": ids["departamentos"]["Departamento de Engenharia"]},
        {"nome": "Biologia Molecular", "coordenador_id": ids["professores"]["I003"], "departamento_id": ids["departamentos"]["Departamento de Ciências"]}
    ]
    res = supabase.table("curso").insert(cursos).execute()
    ids["cursos"] = {c["nome"]: c["id_curso"] for c in res.data}

    # ---------- CURSO_PROFESSOR ----------
    curso_prof = [
        {"curso_id": ids["cursos"]["Engenharia de Software"], "professor_id": ids["professores"]["I001"]},
        {"curso_id": ids["cursos"]["Engenharia de Software"], "professor_id": ids["professores"]["I002"]}
    ]
    supabase.table("curso_professor").insert(curso_prof).execute()

    # ---------- ALUNOS ----------
    alunos = [
        {"nome": "Eduardo Silva", "data_nascimento": "2000-01-15", "curso_id": ids["cursos"]["Engenharia de Software"]},
        {"nome": "Fernanda Costa", "data_nascimento": "1999-07-22", "curso_id": ids["cursos"]["Engenharia de Software"]},
        {"nome": "Gabriel Oliveira", "data_nascimento": "2001-03-10", "curso_id": ids["cursos"]["Biologia Molecular"]}
    ]
    res = supabase.table("aluno").insert(alunos).execute()
    ids["alunos"] = {a["nome"]: a["id_aluno"] for a in res.data}

    # ---------- DISCIPLINAS ----------
    disciplinas = [
        {"nome": "Programação Orientada a Objetos", "creditos": 4},
        {"nome": "Cálculo Diferencial", "creditos": 3},
        {"nome": "Química Orgânica", "creditos": 4}
    ]
    res = supabase.table("disciplina").insert(disciplinas).execute()
    ids["disciplinas"] = {d["nome"]: d["id_disciplina"] for d in res.data}

    # ---------- MATRIZ CURRICULAR ----------
    matriz = [
        {"curso_id": ids["cursos"]["Engenharia de Software"], "disciplina_id": ids["disciplinas"]["Programação Orientada a Objetos"], "semestre_oferta": 1},
        {"curso_id": ids["cursos"]["Engenharia de Software"], "disciplina_id": ids["disciplinas"]["Cálculo Diferencial"], "semestre_oferta": 2},
        {"curso_id": ids["cursos"]["Biologia Molecular"], "disciplina_id": ids["disciplinas"]["Química Orgânica"], "semestre_oferta": 1}
    ]
    supabase.table("matriz_curricular").insert(matriz).execute()

    # ---------- SALA DE AULA ----------
    sala_res = supabase.table("sala_de_aula").insert([
        {"predio": "Prédio A", "numero_sala": "101", "capacidade": 100}
    ]).execute()
    sala_id = sala_res.data[0]["id_sala"]

    # ---------- DISCIPLINA_SALA ----------
    supabase.table("disciplina_sala").insert([
        {"disciplina_id": ids["disciplinas"]["Química Orgânica"], "sala_id": sala_id}
    ]).execute()

    # ---------- HISTÓRICO PROFESSOR ----------
    supabase.table("historico_professor").insert([
        {"professor_id": ids["professores"]["I001"], "disciplina_id": ids["disciplinas"]["Química Orgânica"], "semestre": "2023.2", "ano": 2023},
        {"professor_id": ids["professores"]["I002"], "disciplina_id": ids["disciplinas"]["Programação Orientada a Objetos"], "semestre": "2023.1", "ano": 2023},
        {"professor_id": ids["professores"]["I003"], "disciplina_id": ids["disciplinas"]["Cálculo Diferencial"], "semestre": "2023.1", "ano": 2023}
    ]).execute()

    # ---------- HISTÓRICO ESCOLAR ----------
    supabase.table("historico_escolar").insert([
        {"aluno_id": ids["alunos"]["Fernanda Costa"], "disciplina_id": ids["disciplinas"]["Cálculo Diferencial"], "semestre": "2023.1", "ano": 2023, "nota": 5.0, "situacao": "reprovado"},
        {"aluno_id": ids["alunos"]["Fernanda Costa"], "disciplina_id": ids["disciplinas"]["Cálculo Diferencial"], "semestre": "2023.2", "ano": 2023, "nota": 7.0, "situacao": "aprovado"},
        {"aluno_id": ids["alunos"]["Eduardo Silva"], "disciplina_id": ids["disciplinas"]["Programação Orientada a Objetos"], "semestre": "2023.1", "ano": 2023, "nota": 8.5, "situacao": "aprovado"},
        {"aluno_id": ids["alunos"]["Gabriel Oliveira"], "disciplina_id": ids["disciplinas"]["Química Orgânica"], "semestre": "2023.1", "ano": 2023, "nota": 9.0, "situacao": "aprovado"}
    ]).execute()

    # ---------- TCC ----------
    res = supabase.table("tcc").insert([
        {"titulo": "Aplicativo de Monitoramento", "orientador_id": ids["professores"]["I002"]},
        {"titulo": "Estudo sobre Genômica", "orientador_id": ids["professores"]["I003"]},
        {"titulo": "Visão Computacional Aplicada", "orientador_id": ids["professores"]["I001"]}  # Dr. John
    ]).execute()
    tcc_ids = {t["titulo"]: t["id_tcc"] for t in res.data}

    # ---------- TCC_ALUNO ----------
    supabase.table("tcc_aluno").insert([
        {"tcc_id": tcc_ids["Aplicativo de Monitoramento"], "aluno_id": ids["alunos"]["Eduardo Silva"]},
        {"tcc_id": tcc_ids["Aplicativo de Monitoramento"], "aluno_id": ids["alunos"]["Fernanda Costa"]},
        {"tcc_id": tcc_ids["Estudo sobre Genômica"], "aluno_id": ids["alunos"]["Gabriel Oliveira"]},
        {"tcc_id": tcc_ids["Visão Computacional Aplicada"], "aluno_id": ids["alunos"]["Gabriel Oliveira"]}
    ]).execute()

    print("✅ Todos os dados foram inseridos com sucesso.")

if __name__ == "__main__":
    insert_full_data()
