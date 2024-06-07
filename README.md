## Apache Airflow v 2.9.1-python3.10
Contém um ambiente de desenvolvimento local do Apache Airflow e os workflows (DAGs).

### Requisitos mínimos

- Docker
- Docker Compose v1.29.1 ou mais recente

### Rodando o Airflow com o Make do linux:
O Comando abaixo vai fazer o build da imagem docker; subir os serviços e popular o banco
```
make up
```

Para acessar o container que está o Airflow rode o seguinte comando:
```
make bash
```

Para finalizar os serviços do airflow rode o seguinte comando:
```
make down
```
### Rodando localmente apenas com Docker

Primeiro faça o build da imagem com o comando abaixo:
```
docker build -t airflow:latest .
```


Com a imagem docker pronta, é necessário construir e popular o banco de dados com o comando abaixo:
```
docker-compose up airflow-init
```


E por fim, para rodar o Airflow rode o comando abaixo:
```
docker-compose up
```

### Interface Web

Uma vez que o cluster estiver rodando
- acesse a interface web em http://localhost:8080

Credenciais de acesso:
> usuário: airflow, senha: airflow. 

### Cleaning up

Caso queira parar e apagar os containeres, imagens e volumes (banco de dados) que foram criados:
```
docker-compose down --volumes --rmi all
```

