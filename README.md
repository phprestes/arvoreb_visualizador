# Visualizador de Árvore B
Visualizador de Árvore B para a disciplina de Organização em Arquivos

### Nós por cor:
- Vermelho: Raiz
- Azul: Intermediário
- Verde: Folha

## Instale as dependências (crie uma venv pelo bem do seu SO)
```bash
sudo apt-get install graphviz graphviz-dev
pip install requirements.txt
```

## Rodando
```bash
python3 arvere.py nome_do_arquivo_da_sua_arvore_b.bin
```

## NOTA: OS NÓS NÃO SÂO PLOTADOS NA ORDEM DOS PONTEIROS!!!
Eles são printados na ordem dos arquivo binário de cima para baixo, para de ser preguiçoso e olha manualmente para saber se os ponteiros estão na ordem correta!
