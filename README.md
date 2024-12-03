# Sistema de Gerenciamento de Reservas
### Projeto Final de C216

Este projeto é um sistema de gerenciamento de locação de casas. Ele permite que os usuários gerenciem acomodações e reservas, oferecendo funcionalidades CRUD (Create, Read, Update, Delete) tanto para as acomodações quanto para as reservas.

### Funcionalidades Principais

- Cadastro e gerenciamento de acomodações: Adicionar, editar, visualizar e excluir acomodações com detalhes como cidade, preço, categoria, endereço e proprietário.
- Gerenciamento de reservas: Realizar, visualizar, editar e cancelar reservas, incluindo validação de datas.

## Tecnologias utilizadas
- Backend:
	- Python: Linguagem utilizada para o desenvolvimento da aplicação.
	- FastAPI: Framework para criação de APIs assíncronas e rápidas.
	- Uvicorn: Servidor ASGI para rodar a aplicação FastAPI.
	- asyncpg: Driver assíncrono para interagir com o banco de dados PostgreSQL.

- Frontend:
    - HTML/CSS/JavaScript: Linguagens principais para construção das interfaces.
	- Bootstrap: Framework para construção de interfaces responsivas.
	- Bootstrap-datepicker: Componente para seleção de datas.
	- jQuery: Biblioteca JavaScript para facilitar a manipulação de elementos DOM.

- Docker:
	- Dockerfile e Docker-compose: Utilizados para containerização e fácil configuração do ambiente de desenvolvimento.

## Como rodar o projeto

1. Clone o repositório:
```
git clone https://github.com/FerNagata/Projeto-C216.git
```

2. Execução:
    - Com o docker (Recomendado):

        Na raiz do projeto, execute:
            
        ```
        docker-compose up --build
        ```
    - Caso queira executar apenas a API:

        Vá para o diretorio do backend e execute:
        ```
        python main.py
        ```

    - Caso queira executar apenas o frontend:

        Vá para o diretoria do frontend e execute:
        ```
        python app.py
        ```
        Porém vale notar, que o frontend não estará totalmente funcional, pois ele depende do backend.
    

---

### Padrões de Commits

Esta organização segue uma convenção de commits para manter um histórico claro e consistente. Abaixo está uma tabela com os tipos de commits e suas descrições.

| Tipo de Commit | Descrição |
| -------------- | --------- |
| `feat`         | Adição de uma nova funcionalidade |
| `fix`          | Correção de um bug |
| `docs`         | Mudanças na documentação |
| `style`        | Alterações que não afetam o significado do código (espaços em branco, formatação, ponto e vírgula ausente, etc.) |
| `refactor`     | Refatoração de código, que não altera a funcionalidade nem corrige bugs |
| `perf`         | Alterações de código que melhoram o desempenho |
| `test`         | Adição ou correção de testes |
| `build`        | Mudanças que afetam o sistema de build ou dependências externas (ferramentas de compilação, bibliotecas, etc.) |
| `ci`           | Mudanças em arquivos e scripts de configuração de CI (Integração Contínua) |
| `chore`        | Outras mudanças que não modificam o código fonte ou os testes |
| `revert`       | Reversão de um commit anterior |
| `merge`        | Mesclagem de branches |
| `hotfix`       | Correção urgente de um bug crítico |

Siga esses padrões ao fazer commits para garantir um histórico de commits limpo e fácil de entender.