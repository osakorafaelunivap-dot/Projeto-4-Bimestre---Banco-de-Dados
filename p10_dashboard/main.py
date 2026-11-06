"""Projeto 10: agregacao de vendas e exportacao de grafico PNG."""
from datetime import datetime, timezone
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from conexao import banco

vendas = banco['vendas_p10']
vendas.create_index('codigo', unique=True)

def adicionar(codigo, categoria, produto, quantidade, preco_centavos):
    vendas.update_one({'codigo': codigo}, {'$setOnInsert': {
        'codigo': codigo, 'categoria': categoria, 'produto': produto,
        'quantidade': quantidade, 'total_centavos': quantidade * preco_centavos,
        'data': datetime.now(timezone.utc)}}, upsert=True)

# Demonstração idempotente: executar duas vezes não duplica estas vendas.
adicionar('V001', 'Informática', 'Teclado', 2, 8990)
adicionar('V002', 'Informática', 'Mouse', 4, 4590)
adicionar('V003', 'Papelaria', 'Caderno', 5, 2490)
adicionar('V004', 'Papelaria', 'Caneta', 20, 350)
adicionar('V005', 'Informática', 'Monitor', 1, 89900)

pipeline = [
    {'$group': {'_id': '$categoria', 'faturamento': {'$sum': '$total_centavos'},
                'unidades': {'$sum': '$quantidade'}}},
    {'$sort': {'faturamento': -1}}
]
dados = list(vendas.aggregate(pipeline))
if not dados:
    print('Sem dados de vendas.'); raise SystemExit(0)

print('RELATÓRIO DE VENDAS POR CATEGORIA')
for item in dados:
    print(f"{item['_id']}: {item['unidades']} unidades | R$ {item['faturamento']/100:.2f}")
print(f"Faturamento geral: R$ {sum(i['faturamento'] for i in dados)/100:.2f}")

plt.figure(figsize=(9, 5))
plt.bar([d['_id'] for d in dados], [d['faturamento']/100 for d in dados])
plt.ylabel('Faturamento (R$)')
plt.title('Vendas por categoria')
plt.tight_layout()
destino = Path(__file__).with_name('grafico_vendas.png')
plt.savefig(destino, dpi=150)
plt.close()
print(f'Gráfico gerado: {destino}')