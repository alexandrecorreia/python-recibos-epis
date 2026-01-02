# Geração de Recibos de EPIs

Aplicação desktop desenvolvida em **Python** para **controle e geração de comprovantes de entrega de EPIs**, com opção de **baixa automática de estoque via API Omie**, geração de **PDF** e interface gráfica baseada em **Tkinter**.

O sistema permite selecionar funcionários, escolher EPIs, informar quantidades entregues e gerar um **comprovante formal em PDF**, além de integrar (opcionalmente) com o estoque do Omie.

---

## Funcionalidades
- Interface gráfica multiplataforma (Windows, Linux e macOS), com maximização automática da janela.
- Cadastro de funcionários via arquivo CSV (ordenado alfabeticamente).
- Cadastro de EPIs via arquivo CSV, com seleção múltipla via checkboxes visuais (usando imagens para melhor usabilidade).
- Modal para informar e editar quantidades entregues por EPI.
- Geração automática de **comprovante em PDF** usando template HTML customizável.
- Integração opcional com a **API Omie** para ajuste de estoque (baixa automática por item).
- Validações e mensagens de erro para arquivos ausentes, falhas na API e entradas inválidas.
- Software livre sob licença **GPL-3.0**.

---

## Tecnologias Utilizadas
- Python 3.8+ (testado em 3.12 para compatibilidade com bibliotecas).
- Tkinter e ttk (para a GUI).
- Pandas (para leitura de CSVs).
- Requests (para chamadas à API Omie).
- WeasyPrint (para geração de PDF a partir de HTML).
- Pillow (PIL, para imagens de checkboxes).
- ConfigParser (para leitura de configurações).

---

## Requisitos
- Python 3.8 ou superior.
- Bibliotecas: Instale via `pip install pandas weasyprint requests pillow`.
  - **Nota sobre WeasyPrint**: Pode requerer dependências do sistema como Pango e Cairo (ex: no Ubuntu, `sudo apt install libpango-1.0-0 libpangoft2-1.0-0 libcairo2`).
- Arquivos de dados: `data/estoque.csv` e `data/funcionarios.csv`.
- Template: `TEMPLATE_CONTROLE_EPI.tpl` (HTML com placeholders como `{{NOME_FUNCIONARIO}}`, `{{NOME_DA_EMPRESA}}`, `{{DATA_HOJE}}` e `{{TABELA_DE_ITENS}}`).
- Configuração: `config.ini` com chaves da API Omie.

---

## Instalação
1. Clone ou baixe o repositório.
2. Crie um ambiente virtual (opcional): `python -m venv venv` e ative-o.
3. Instale as dependências: `pip install -r requirements.txt`.
4. Crie o diretório `data/` e adicione os arquivos CSV (veja formatos abaixo).
5. Adicione o template HTML na raiz do projeto.
6. Configure `config.ini` (veja exemplo abaixo).

---

## Estrutura do Projeto
```
.
├── app.py                      # Script principal (renomeie o código fornecido para app.py se necessário)
├── config.ini                  # Configurações da API e opções
├── README.md                   # Este arquivo
├── data/
│   ├── estoque.csv             # Lista de EPIs
│   └── funcionarios.csv        # Lista de funcionários
└── TEMPLATE_CONTROLE_EPI.tpl   # Template HTML para PDF
```

---

## Formato dos Arquivos CSV
### data/funcionarios.csv (separador: ",")
```
funcionario,empresa,cnpj
João da Silva,Empresa Exemplo LTDA,00.000.000/0001-00
Maria Oliveira,Empresa Exemplo LTDA,00.000.000/0001-00
```

### data/estoque.csv (separador: ";")
```
Código;Descrição
1001;Capacete de Segurança
1002;Luvas de Proteção
```

**Nota**: Os CSVs devem estar em UTF-8. O app ignora linhas vazias ou incompletas.

---

## Configuração (config.ini)
```
[Omie]
app_key = SUA_APP_KEY
app_secret = SEU_APP_SECRET
ajustar_estoque = false

[EstoqueAjuste]
url = https://app.omie.com.br/api/v1/estoque/ajuste/
```
- **ajustar_estoque** tornar a baixa opcional (ex: `ajustar_estoque = false`, desabilitado ).

---

## Uso
1. Execute o app: `python app.py`.
2. Na interface:
   - Selecione um funcionário na tabela superior.
   - Marque EPIs na tabela inferior (clique no checkbox ou selecione múltiplos).
   - Clique em "Imprimir Comprovante de Entrega".
   - No modal, edite quantidades (duplo-clique na coluna "Quantidade").
   - Confirme para gerar PDF e (se configurado) ajustar estoque no Omie.
3. O PDF será gerado como `Comprovante_EPI.pdf` e aberto automaticamente (se possível).

---

## Problemas Comuns e Soluções
- **Erro em config.ini**: Verifique se o arquivo existe e contém as seções/chaves corretas.
- **CSVs não encontrados**: Certifique-se de que os caminhos em `data/` estão corretos.
- **Falha na API Omie**: Cheque chaves, URL e conexão de rede. Erros são exibidos via messagebox.
- **PDF não gerado**: Instale WeasyPrint corretamente e verifique o template.
- **Checkboxes não visíveis**: Pillow é necessário; reinstale se houver problemas.

---

## Contribuição
Contribuições são bem-vindas! Abra issues para bugs ou pull requests para melhorias. Mantenha o código limpo e adicione comentários.

## Licença
GPL-3.0 License.

## Autor
- Alexandre Correia ( dinhocorreia@gmail.com )

Gerado em 02/01/2026.