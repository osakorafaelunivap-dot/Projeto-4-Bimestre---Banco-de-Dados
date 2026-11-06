"""Projeto 08: prova objetiva A-E, gabarito e correcao automatica."""
from conexao import banco

provas = banco['provas_p08']
resultados = banco['resultados_p08']
provas.create_index('codigo', unique=True)
resultados.create_index([('prova', 1), ('aluno', 1)], unique=True)

while True:
    print('\n[1] Criar prova [2] Corrigir aluno [3] Resultados [0] Sair')
    op = input('Opção: ').strip()
    if op == '1':
        codigo = input('Código da prova: ').strip()
        gabarito = input('Gabarito (ex.: ABCDE): ').strip().upper()
        if not codigo or not gabarito or any(c not in 'ABCDE' for c in gabarito):
            print('Código ou gabarito inválido.'); continue
        if provas.find_one({'codigo': codigo}):
            print('Código já utilizado.'); continue
        provas.insert_one({'codigo': codigo, 'gabarito': gabarito})
        print('Prova criada.')
    elif op == '2':
        codigo = input('Código da prova: ').strip()
        prova = provas.find_one({'codigo': codigo})
        if not prova:
            print('Prova não encontrada.'); continue
        aluno = input('Matrícula do aluno: ').strip()
        respostas = input('Respostas (A-E; X para em branco): ').strip().upper()
        if not aluno or len(respostas) != len(prova['gabarito']) or any(
                c not in 'ABCDEX' for c in respostas):
            print('Respostas inválidas ou quantidade incorreta.'); continue
        acertos = sum(a == b for a, b in zip(respostas, prova['gabarito']))
        nota = round(10 * acertos / len(prova['gabarito']), 2)
        resultados.update_one({'prova': codigo, 'aluno': aluno},
                              {'$set': {'respostas': respostas, 'acertos': acertos,
                                        'nota': nota}}, upsert=True)
        print(f'Resultado: {acertos}/{len(respostas)} | Nota: {nota:.2f}')
    elif op == '3':
        codigo = input('Código da prova: ').strip()
        for r in resultados.find({'prova': codigo}).sort('nota', -1):
            print(f"{r['aluno']} | {r['acertos']} acertos | Nota {r['nota']:.2f}")
    elif op == '0':
        break
    else:
        print('Opção inválida.')