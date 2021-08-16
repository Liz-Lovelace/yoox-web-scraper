import requests
links = [
'https://www.yoox.com/ru/17106928PA/item#dept=collgirl_kid&sts=sr_collgirl_kid80',
'https://www.yoox.com/ru/17107493VC/item#dept=collgirl_kid&sts=sr_collgirl_kid80',
'https://www.yoox.com/ru/17112120MG/item#dept=collgirl_kid&sts=sr_collgirl_kid80',
'https://www.yoox.com/ru/17098128HC/item#dept=collgirl_kid&sts=sr_collgirl_kid80',
'https://www.yoox.com/ru/17099160RG/item#dept=collgirl_kid&sts=sr_collgirl_kid80',
'https://www.yoox.com/ru/17037876WV/item#dept=collgirl_kid&sts=sr_collgirl_kid80',
'https://www.yoox.com/ru/17091579TC/item#dept=collgirl_kid&sts=sr_collgirl_kid80',
'https://www.yoox.com/ru/17106942AS/item#dept=collgirl_kid&sts=sr_collgirl_kid80',
'https://www.yoox.com/ru/17098124TI/item#dept=collgirl_kid&sts=sr_collgirl_kid80',
'https://www.yoox.com/ru/17103763NS/item#dept=collgirl_kid&sts=sr_collgirl_kid80'
]
pages = []
for i in links:
  pages.append(requests.get(i))

print(pages)