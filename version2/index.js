import cheerio from 'cheerio';
import fetch from 'node-fetch';
import fs from 'fs';
import { URL } from 'url';

function getItems(html) {
  let $ = cheerio.load(html);
  let items = $('.itemContainer');
  let itemProperties = [];
  for (let i = 0; i < items.length; i++){
    let item = items[i];
    let item$ = cheerio.load(item);
    let properties = {}
    properties.parentCategoryId = item.attribs['data-macrocategory_id'];
    properties.parentCategoryName = item.attribs['data-macrocategory'];
    properties.categoryId = item.attribs['data-category_id'];
    properties.categoryName = item.attribs['data-category'];
    properties.id = item.attribs['data-current-cod10'];    
    properties.productUrl = 'https://yoox.com' + item$('.itemImg > a')['0'].attribs['href'];
    if (item$('.itemImg > a > img')['0'].attribs['data-original']){
      properties.imageUrl = item$('.itemImg > a > img')['0'].attribs['data-original'];
    } else if (item$('.itemImg > a > img')['0'].attribs['src']){
      properties.imageUrl = item$('.itemImg > a > img')['0'].attribs['src'];
    } else {
      throw 'can\'t find image!!!';
    }
    //TODO: remove extra tags from image url.
    itemProperties.push(properties);
  }
  return itemProperties;
}

async function saveCatalog(url){
  let html = await fetch(url);
  await fs.promises.writeFile(new URL('catalog.html', import.meta.url), await html.text());
}

function findBrokenItems(items){
  let brokenItems = []
  items.forEach(item => {
    if(!( item.parentCategoryId
       && item.parentCategoryName
       && item.categoryId
       && item.categoryName
       && item.id
       && item.productUrl
       && item.imageUrl)) 
    {
      brokenItems.push(item);
    }
  });
  return brokenItems;
}

async function main() {
  let html = await fs.promises.readFile(new URL('data/womenShoesP1.html', import.meta.url), 'utf8');
  let items = getItems(html);
  console.log(findBrokenItems(items));
}

main();