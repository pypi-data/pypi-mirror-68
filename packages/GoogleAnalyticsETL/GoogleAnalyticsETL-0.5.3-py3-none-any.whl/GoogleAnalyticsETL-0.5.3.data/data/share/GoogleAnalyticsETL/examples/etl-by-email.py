#!/usr/bin/env python3

import logging
from GACustomReportEmailToDB import GACustomReportParcelasClicadas

# Switch between INFO/DEBUG while running in production/developping:
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())


config={}

config['database']={
    'url': "mysql+pymysql://user:password@host.com/database?charset=utf8mb4",
    'update': True
}

config['imap']={
    'server': "imap.gmail.com",
    'folder': "braseg/GACustomReports",
    'subject': "ga_parcelas_atrasadas_clicadas",
    'user': "a.....i@email.com",
    'password': "w.......g",
}


etl1=GACustomReportParcelasClicadas.GACustomReportParcelasClicadasV1(
    config=config,
    imap_sent_since='2019-09-29',
    imap_sent_before='2019-11-10'   
)

# etl2=GACustomReportParcelasClicadas.GACustomReportParcelasClicadasV2(
#     config=config,
#     imap_sent_since='2019-12-09',
#     imap_sent_before='2020-01-25'
# )

etl3=GACustomReportParcelasClicadas.GACustomReportParcelasClicadasV3(
    config=config,
    imap_sent_since='2020-01-11',
    imap_sent_before='2020-03-20'
)


etl4=GACustomReportParcelasClicadas.GACustomReportParcelasClicadasV4(
    config=config,
    imap_sent_since='2020-03-25',
    imap_sent_before=None
)



processors=[etl4,etl3,etl1]

for p in processors:
    p.sync()
