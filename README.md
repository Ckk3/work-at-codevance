 Desafio Técnico Codevance

Esse repo contém o meu teste [técnico para a Codevance](https://github.com/Ckk3/work-at-codevance/blob/ceb7245439c7c41a15d3f35ec483ef168657cfca/challenge_info.md).

## Inicie e configure o projeto

1. Tenha docker compose na sua máquina
2. Acesse o arquivo ***********example.env***********  e coloque o valores de acordo com o seu ambiente, você pode utilizar esse com base:
    
    ```jsx
    POSTGRES_NAME="postgres"
    POSTGRES_USER="postgres"
    POSTGRES_PASSWORD="postgres"
    CELERY_BROKER_URL="amqp://guest:guest@broker:5672//"
    EMAIL_HOST_USER = ""
    EMAIL_HOST_PASSWORD = ""
    DEFAULT_FROM_EMAIL= ""
    ```
    
3. Renomeie o arquivo ***********example.env*********** para *.env*
4. Execute o docker compose utilizando o seguinte comando
    
    ```bash
    docker-compose up
    ```
    
5. Agora, você já pode acessar o projeto em [http:/localhost:8000](http://localhost:8000), porém vamos terminar a configuração
6. Todas as informações do banco de dados são excluídas no repositório, então você precisa criar manualmente os grupos e usuários do projeto.
7. Descubra qual é o container que está rodando o django utlizando o comando:
    
    ```jsx
    docker ps
    ```
    
8. Procure na lista o container que está com o final ***web*** e use o seguinte comando para abrir um temrinal interativo nele
    
    ```jsx
    docker exec -it id_do_container bash
    ```
    
9. Dentro do container *web* criado no compose, crie um super usuário utilizando esse comando e seguindo as instruções:
    
    ```bash
    python3 manage.py createsuperuser
    ```
    
10. Acesse a página de administrador do sistema, vá em [http://localhost:8000/admin](http://localhost:8000/admin) e entre com a conta de super usuario que voce acabou de criar
11. Vá em *Groups* → ***Add***, e crie um grupo com o nome “operadores” e outro com o nome “fornecedores”. Não precisa adicionar nenhuma permissão
12. Agora crie um usuário qualquer, adicione no grupo fornecedores e adicione um email
13. Depois, crie um usuário e o adicione ao grupo operadores
14. Depois, volte para a raiz do projeto em  [http://localhost:8000](http://localhost:8000/admin) , você receberá uma mensagem que diz que você não tem permissão, isso acontece porque estamos logados no usuário admin, Clique na opção SAIR
15. Efetue o login com o usuário do grupo fornecedor que você criou
    
    ![Untitled](https://github.com/Ckk3/work-at-codevance/blob/c2c597037f4eda843d52089b3cdb03216670b15e/readme_Images/login.png)
    
16. Agora você verá essa página com todos os pagamentos
    
    ![Untitled](https://github.com/Ckk3/work-at-codevance/blob/c2c597037f4eda843d52089b3cdb03216670b15e/readme_Images/payments.png)
    
17. Quando você adiantar um pagamento, um email será enviado para o funcionário (por isso você deve colocar um email válido na criação do usuário)

![Untitled](https://github.com/Ckk3/work-at-codevance/blob/c2c597037f4eda843d52089b3cdb03216670b15e/readme_Images/email.png)

1. Para ter a utilização sendo operador, é só clicar em sair e entrar com a conta de um operador
2. Você também têm uma lista com todos os pedidos de antecipação 

![Untitled](https://github.com/Ckk3/work-at-codevance/blob/c2c597037f4eda843d52089b3cdb03216670b15e/readme_Images/anticipates.png)


## Testes

O programa possui alguns testes, siga as instruções para executá-los

1. Descubra qual é o container que está rodando o django utilizando o comando:
    
    ```jsx
    docker ps
    ```
    
2. Procure na lista o container que está com o final ***web*** e use o seguinte comando para abrir um temrinal interativo nele
    
    ```jsx
    docker exec -it <id_do_container> bash
    ```
    
3. Dentro do container *web* criado no compose, execute os testes utilizando o comando:
    
    ```bash
    python3 manage.py test
    ```
    
    Note que para os testes funcionarem, você deve ter feito o a configuração inicial do projeto.


















