#!/bin/bash -l
docker run --rm -v /home/abp/abp-m3u/pop-epg/wallet:/opt/oracle/instantclient_21_3/network/admin \
-e ATP_USER=$ATP_USER -e ATP_PASSWORD=$ATP_PASSWORD -e ATP_DSN=$ATP_DSN abpdock/populate_epg_db
