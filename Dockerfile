FROM puckel/docker-airflow:1.10.9
USER root
RUN touch /var/run/docker.sock &&\
    chgrp airflow /var/run/docker.sock &&\
    chmod 777 /var/run/docker.sock
USER airflow:airflow