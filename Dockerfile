FROM apache/airflow:2.9.1-python3.10

ENV TZ=America/Sao_Paulo

USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    ca-certificates \
    libaio1 unzip curl libsnl-dev git

USER airflow

COPY pip.conf /home/airflow/.pip/pip.conf
RUN pip install --upgrade pip
RUN pip install --no-cache-dir \
    psycopg2-binary \
    pyarrow==10.0.1 \
    pyocclient==0.6 \
    pandas \
    xlsxwriter \
    SQLAlchemy \
    django-environ \
    graypy \
    xlwt \
    openpyxl \
    xlrd \
    tqdm 

COPY --chown=airflow:root dags/ /opt/airflow/dags
COPY --chown=airflow:root tests/ /opt/airflow/tests
COPY --chown=airflow:root plugins/ /opt/airflow/plugins
COPY --chown=airflow:root logs/ /opt/airflow/logs
COPY --chown=airflow:root reports/ /opt/airflow/reports
COPY --chown=airflow:root stage/ /opt/airflow/stage

USER root
RUN chmod -R 777 /opt/airflow/reports /opt/airflow/stage

USER airflow