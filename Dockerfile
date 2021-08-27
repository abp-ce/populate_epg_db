FROM ubuntu:latest
RUN apt update && apt install -y python3.8 python3-pip wget unzip libaio1
COPY requirements.txt populate_epg_db.py /root/
RUN pip install -r /root/requirements.txt
RUN wget -P /root https://download.oracle.com/otn_software/linux/instantclient/213000/instantclient-basiclite-linux.x64-21.3.0.0.0.zip
WORKDIR /opt/oracle
RUN unzip /root/instantclient-basiclite-linux.x64-21.3.0.0.0.zip
#COPY wallet/* /opt/oracle/instantclient_21_3/network/admin/
ENV LD_LIBRARY_PATH=/opt/oracle/instantclient_21_3:$LD_LIBRARY_PATH
WORKDIR /root
RUN rm instantclient-basiclite-linux.x64-21.3.0.0.0.zip
ENTRYPOINT [ "python3" ]
CMD [ "populate_epg_db.py" ]