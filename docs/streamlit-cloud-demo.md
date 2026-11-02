# Demonstração no Streamlit Community Cloud

O modo de demonstração oferece alunos, exercícios, fichas, evolução física e
mensalidades fictícios. Todas as operações acontecem na sessão do visitante,
sem API FastAPI, banco SQLite ou compartilhamento entre visitantes.
O login é dispensado exclusivamente quando o modo está ativo.

## Execução local (PowerShell, na raiz)

```powershell
$env:DEMO_MODE = "true"
.\.venv\Scripts\python.exe -m streamlit run frontend/app.py
```

Para voltar ao modo normal, encerre o processo e remova a variável:

```powershell
Remove-Item Env:DEMO_MODE
```

## Configuração no Cloud

1. Selecione o repositório e o arquivo principal `frontend/app.py`.
2. Use Python 3.11. As dependências ficam em `frontend/requirements.txt`.
3. Em **Advanced settings → Secrets**, configure apenas:

```toml
DEMO_MODE = true
```

4. Publique o app. O modo normal continua sendo o padrão quando a opção não está ativa.

Não é necessário copiar os secrets locais de banco ou API para a demonstração.
O aviso na barra lateral identifica o modo e permite restaurar os exemplos.
Alterações sobrevivem à navegação e aos reruns, mas são perdidas quando a sessão
é encerrada. Atualizar a página pode abrir uma nova sessão.

Para apresentar: abra Alunos, visualize a ficha de Ana em Treinos, acompanhe os
gráficos em Avaliações e registre a baixa de uma mensalidade em Financeiro.
Você também pode cadastrar dados fictícios e restaurar a demonstração ao final.

Documentação oficial:
- [Deploy e configuração](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy)
- [Dependências](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies)
