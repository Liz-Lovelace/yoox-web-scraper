import requests
import re
from pyquery import PyQuery

#these are test cases for individual products
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


def getCatalogNameFromNum(i):
    if (i == 0):
      return 'baby-girl'
    elif(i == 1):
      return 'child-girl'
    elif(i == 2):
      return 'teen-girl'
    elif(i == 3):
      return 'baby-boy'
    elif(i == 4):
      return 'child-boy'
    elif(i == 5):
      return 'teen-boy'

def fetchCatalogsAndWriteToFiles():
  for i in range(len(catalogLinks)):
    page = requests.get(catalogLinks[i])
    
    f = open('./'+getCatalogNameFromNum(i) + '.html', 'w')
    f.write(page.content.decode())
    f.close()
    
def findInfo(catalogHtml):
  d = PyQuery(catalogHtml)
  imageContainers = d('.itemContainer .itemImg a')
  items = []
  #idRe = re.compile('items/../.........._')
  for (i, item) in enumerate(imageContainers.items()):
    cardUrl = 'https://yoox.com' + item.attr('href')
    imgUrl = item('img').attr('src')
    if (not imgUrl):
      imgUrl = item('img').attr('data-original')
    imgUrl = re.sub('\?.*', '', str(imgUrl))
    
    itemId = cardUrl[20:30]
    
    items.append((itemId, cardUrl, imgUrl))

  return items

catalogFile = open('./data/catalogs/baby-girl.html', 'r')
catalogContents = catalogFile.read()
catalogFile.close()

output = open(getCatalogNameFromNum(0) + '.txt', 'w')
for (i, t) in enumerate(findInfo(catalogContents)):
  if (i == 100):
    break
  output.write(t[0] + '\n' +t[1] + '\n' + t[2] + '\n\n')

output.close()
