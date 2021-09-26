import requests
import re
from pyquery import PyQuery

# It's important to copy these links by right-clicking the "shoes" section and
# pressing "copy link to clipboard" instead of going to the link and copying the url!
#baby-girl, child-girl, teen-girl, baby-boy, child-boy, teen-boy
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
  for (i, item) in enumerate(imageContainers.items()):
    cardUrl = 'https://yoox.com' + item.attr('href')
    imgUrl = item('img').attr('src')
    if (not imgUrl):
      imgUrl = item('img').attr('data-original')
    imgUrl = re.sub('\?.*', '', str(imgUrl))
    
    itemId = cardUrl[20:30]
    
    items.append((itemId, cardUrl, imgUrl))

  return items

def parseCatalogsAndWriteIntoFiles():
  for catalogI in range(6):
    catalogFile = open('./data/catalogs/'+getCatalogNameFromNum(catalogI)+'.html', 'r')
    catalogContents = catalogFile.read()
    catalogFile.close()
    output = open(getCatalogNameFromNum(catalogI) + '.txt', 'w')
    for (i, t) in enumerate(findInfo(catalogContents)):
      #maximum 1 for one page is around 120
      if (i == 100):
        break
      output.write(t[0] + '\n' +t[1] + '\n' + t[2] + '\n\n')

    output.close()
    print('done with', getCatalogNameFromNum(catalogI))

def visualCheckFiles():
  for fileI in range(6):
    fileName = getCatalogNameFromNum(fileI) + '.txt'
    file = open(fileName, 'r')
    contents = file.read()
    file.close()
    for (i, line) in enumerate(contents.split('\n')):
      print(('\n' if i % 4 == 0 else ' | ' )+ line, end='')
      
visualCheckFiles()