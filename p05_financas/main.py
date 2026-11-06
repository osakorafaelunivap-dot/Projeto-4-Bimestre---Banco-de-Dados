"""Projeto 05: receitas, despesas e agregacoes com valores em centavos."""
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from datetime import datetime, timezone
from conexao import banco

lancamentos = banco['lancamentos_p05']

def centavos(texto):
    try:
        valor = Decimal(texto.replace(',', '.'))
        if not valor.is_finite() or valor <= 0:
            raise ValueError
        return int((valor * 100).quantize(Decimal('1'), rounding=ROUND_HALF_UP))
    except (InvalidOperation, ValueError):
        return None

while True:
    print('\n[1] Registrar [2] Extrato [3] Resumo por categoria [0] Sair')
    op = input('Opção: ').strip()
    if op == '1':
        tipo = input('Tipo (receita/despesa): ').strip().lower()
        categoria = input('Categoria: ').strip()
        valor = centavos(input('Valor (R$): ').strip())
        if tipo not in ('receita', 'despesa') or not categoria or valor is None:
            print('Dados inválidos.'); continue
        lancamentos.insert_one({'tipo': tipo, 'categoria': categoria,
                                'valor_centavos': valor,
                                'criado_em': datetime.now(timezone.utc)})
        print('Lançamento registrado.')
    elif op == '2':
        for item in lancamentos.find().sort('criado_em', -1).limit(30):
            print(f"{item['tipo']} | {item['categoria']} | R$ {item['valor_centavos']/100:.2f}")
    elif op == '3':
        pipeline = [
            {'$group': {'_id': {'tipo': '$tipo', 'categoria': '$categoria'},
                        'total': {'$sum': '$valor_centavos'}}},
            {'$sort': {'_id.tipo': 1, '_id.categoria': 1}}
        ]
        receitas = despesas = 0
        for item in lancamentos.aggregate(pipeline):
            tipo, categoria = item['_id']['tipo'], item['_id']['categoria']
            total = item['total']
            print(f'{tipo} / {categoria}: R$ {total/100:.2f}')
            if tipo == 'receita': receitas += total
            else: despesas += total
        print(f'SALDO: R$ {(receitas - despesas)/100:.2f}')
    elif op == '0':
        break
    else:
        print('Opção inválida.')