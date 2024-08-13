FROM python:3.12.0

RUN pip install terraform-local

RUN mkdir /home/terraform
COPY terraform /home/terraform

RUN mkdir /home/functions
COPY functions /home/functions

RUN mkdir /home/IoTSensors
COPY IoTSensors /home/IoTSensors

WORKDIR /home/terraform
RUN apt-get update && apt-get install -y lsb-release && apt-get clean all
RUN wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
RUN echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/hashicorp.list
RUN apt update && apt install terraform

COPY deploy_infra.sh /home/deploy_infra.sh
WORKDIR /home

RUN apt-get install dos2unix
RUN dos2unix deploy_infra.sh

ENTRYPOINT [ "bash", "deploy_infra.sh" ]


