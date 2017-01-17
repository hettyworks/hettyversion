FROM google/cloud-sdk:latest


RUN apt-get install -y mysql-client-5.5

ADD entrypoint.sh /opt/hettyversion/entrypoint.sh

CMD /opt/hettyversion/entrypoint.sh