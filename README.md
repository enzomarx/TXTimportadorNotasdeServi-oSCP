CSV to TXT Processor (NFS Layout)

Aplicativo desktop em Python + Tkinter para importar um CSV, validar colunas obrigatórias e gerar um arquivo TXT no formato de registros (ex.: 3000 e 3500) com layout pré-definido. Inclui visualização em tabela, logs, configuração de data de serviço, fullscreen e suporte básico a internacionalização (i18n) via gettext.

O que este projeto faz

Importa um arquivo .csv (delimitado por , ou ;)

Normaliza nomes de colunas (strip)

Valida a existência das colunas obrigatórias:

MATRICULA

BRUTO

CENTAVOS

Exibe os dados em uma tabela (Treeview)

Permite definir a Data de Serviço (DD/MM/AAAA)

Gera um TXT com:

Cabeçalho fixo de layout

Para cada linha do CSV, gera:

Registro 3000 (Tipo do registro NFS)

Registro 3500 (Parcela NFS)

Mantém um painel de logs

Alterna tema (default/clam)

Inicia em tela cheia (sair com Esc)

Formato de saída (TXT)

O arquivo de saída começa com dois cabeçalhos fixos:

Tipo do registro NFS|...

Parcela NFS|...

Depois, para cada linha do CSV:

3000|...|{numero_doc}|...|{service_date}|...|{bruto},{centavos}|...|{matricula}|...

3500|{service_date}|{bruto},{centavos}|...

📌 Observação: numero_doc e doc_final são gerados com random.randint(1000, 9999).

📦 Requisitos

Python 3.9+ (recomendado)

Bibliotecas:

pandas

tkinter, random, os, gettext já vêm com o Python (na maioria dos ambientes).
