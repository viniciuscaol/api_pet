### Criando o Banco de Dados em Container
Para criar um banco de dados PostgreSQL em um container Docker e inicializá-lo com uma tabela, use o seguinte comando:

```bash
docker run --name postgres-container \
    -e POSTGRES_USER=user \
    -e POSTGRES_PASSWORD=senha123 \
    -e POSTGRES_DB=pet_db \
    -v $(pwd)/init.sql:/docker-entrypoint-initdb.d/init.sql \
    -p 5432:5432 \
    -d postgres
```
##### Parâmetros do comando:

**--name postgres-container:** Nome do container.</br>
**-e POSTGRES_USER=user:** Nome do usuário do banco de dados.</br>
**-e POSTGRES_PASSWORD=senha123:** Senha do usuário.</br>
**-e POSTGRES_DB=pet_db:** Nome do banco de dados.</br>
**-v $(pwd)/init.sql:/docker-entrypoint-initdb.d/init.sql:** Monta o arquivo init.sql no diretório de inicialização do PostgreSQL.</br>
**-p 5432:5432:** Mapeia a porta 5432 do container para a porta 5432 do host.</br>
**-d postgres:** Usa a imagem oficial do PostgreSQL e executa em modo destacado (background).

### Bibliotecas Necessárias
Instale a biblioteca **psycopg2-binary** para interagir com o PostgreSQL:

```bash
pip install psycopg2-binary
```

### Executando o Script
Depois de configurar o banco de dados e instalar as bibliotecas necessárias, execute o script Python **grafic.py**:

```bash
python grafic.py
```
