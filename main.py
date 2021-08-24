import requests
#these are for individual products
testLinks = [
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
# It's important to copy these links by right-clicking the shoes section and
# pressing "copy link to clipboard" instead of going to the link and copying the url!
catalogLinks = [
'https://www.yoox.com/ru/%D0%B4%D0%BB%D1%8F%20%D0%B4%D0%B5%D0%B2%D0%BE%D1%87%D0%B5%D0%BA/%D0%BA%D0%BE%D0%BB%D0%BB%D0%B5%D0%BA%D1%86%D0%B8%D0%B8/%D0%BC%D0%B0%D0%BB%D1%8B%D1%88%D0%B8/shoponline/%D0%BE%D0%B1%D1%83%D0%B2%D1%8C_mc#/dept=collgirl_baby&gender=D&page=1&season=X',
'https://www.yoox.com/ru/%D0%B4%D0%BB%D1%8F%20%D0%B4%D0%B5%D0%B2%D0%BE%D1%87%D0%B5%D0%BA/%D0%BA%D0%BE%D0%BB%D0%BB%D0%B5%D0%BA%D1%86%D0%B8%D0%B8/%D0%B4%D0%B5%D1%82%D0%B8/shoponline/%D0%BE%D0%B1%D1%83%D0%B2%D1%8C_mc#/dept=collgirl_kid&gender=D&page=1&attributes=%7b%27ctgr%27%3a%5b%27clztr%27%5d%7d&season=X',
'https://www.yoox.com/ru/%D0%B4%D0%BB%D1%8F%20%D0%B4%D0%B5%D0%B2%D0%BE%D1%87%D0%B5%D0%BA/%D0%BA%D0%BE%D0%BB%D0%BB%D0%B5%D0%BA%D1%86%D0%B8%D0%B8/%D0%BF%D0%BE%D0%B4%D1%80%D0%BE%D1%81%D1%82%D0%BA%D0%B8/shoponline/%D0%BE%D0%B1%D1%83%D0%B2%D1%8C_mc#/dept=collgirl_junior&gender=D&page=1&season=X',
'https://www.yoox.com/ru/%D0%B4%D0%BB%D1%8F%20%D0%BC%D0%B0%D0%BB%D1%8C%D1%87%D0%B8%D0%BA%D0%BE%D0%B2/%D0%BA%D0%BE%D0%BB%D0%BB%D0%B5%D0%BA%D1%86%D0%B8%D0%B8/%D0%BC%D0%B0%D0%BB%D1%8B%D1%88%D0%B8/shoponline/%D0%BE%D0%B1%D1%83%D0%B2%D1%8C_mc#/dept=collboy_baby&gender=U&page=1&attributes=%7b%27ctgr%27%3a%5b%27clztr%27%5d%7d&season=X',
'https://www.yoox.com/ru/%D0%B4%D0%BB%D1%8F%20%D0%BC%D0%B0%D0%BB%D1%8C%D1%87%D0%B8%D0%BA%D0%BE%D0%B2/%D0%BA%D0%BE%D0%BB%D0%BB%D0%B5%D0%BA%D1%86%D0%B8%D0%B8/%D0%B4%D0%B5%D1%82%D0%B8/shoponline/%D0%BE%D0%B1%D1%83%D0%B2%D1%8C_mc#/dept=collboy_kid&gender=U&page=1&attributes=%7b%27ctgr%27%3a%5b%27clztr%27%5d%7d&season=X',
'https://www.yoox.com/ru/%D0%B4%D0%BB%D1%8F%20%D0%BC%D0%B0%D0%BB%D1%8C%D1%87%D0%B8%D0%BA%D0%BE%D0%B2/%D0%BA%D0%BE%D0%BB%D0%BB%D0%B5%D0%BA%D1%86%D0%B8%D0%B8/%D0%BF%D0%BE%D0%B4%D1%80%D0%BE%D1%81%D1%82%D0%BA%D0%B8/shoponline/%D0%BE%D0%B1%D1%83%D0%B2%D1%8C_mc#/dept=collboy_junior&gender=U&page=1&attributes=%7b%27ctgr%27%3a%5b%27clztr%27%5d%7d&season=X'
]

pages = []
def fetchCatalogsAndWriteToFiles():
  for i in range(len(catalogLinks)):
    page = requests.get(catalogLinks[i])
    fileName = ''
    if (i == 0):
      fileName = 'baby-girl.html'
    elif(i == 1):
      fileName = 'child-girl.html'
    elif(i == 2):
      fileName = 'teen-girl.html'
    elif(i == 3):
      fileName = 'baby-boy.html'
    elif(i == 4):
      fileName = 'child-boy.html'
    elif(i == 5):
      fileName = 'teen-boy.html'
    
    f = open('./'+fileName, 'w')
    f.write(page.content.decode())
    f.close()

fetchCatalogsAndWriteToFiles()