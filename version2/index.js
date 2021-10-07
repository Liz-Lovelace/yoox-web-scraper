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
    //soldout items require different parsing, so I'm skipping them
    if (item.attribs['class'].indexOf('soldout') != -1)
      continue;
    let item$ = cheerio.load(item);
    let properties = {}
    properties.parentCategoryId = item.attribs['data-macrocategory_id'];
    properties.parentCategoryName = item.attribs['data-macrocategory'];
    properties.categoryId = item.attribs['data-category_id'];
    properties.categoryName = item.attribs['data-category'];
    properties.id = item.attribs['data-current-cod10'];    
    
    properties.productUrl = 'https://yoox.com' + item$('.itemImg > a')['0'].attribs['href'];
    
    let img = item$('.itemImg > a > img')['0'];
    if (img.attribs['data-original']){
      properties.imageUrl = img.attribs['data-original'];
    } else if (img.attribs['src']){
      properties.imageUrl = img.attribs['src'];
    } else {
      throw 'can\'t find image!!!';
    }
    //TODO: remove extra tags from image url.
    itemProperties.push(properties);
  }
  return itemProperties;
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

async function fetchWrite(path, link){
  return new Promise(async (resolve, reject)=>{
    let html = await (await fetch(link)).text();
    if (!html)
      reject('no html???');
    await fs.promises.writeFile(path, html);
    resolve();
  });
}

async function batchDownload(){
  let catalogLimit = 544;
  let dir_path = new URL('./data/catalogs/womens-shoes/', import.meta.url);
  let catalog_base_link = 'https://www.yoox.com/ru/%D0%B4%D0%BB%D1%8F%20%D0%B6%D0%B5%D0%BD%D1%89%D0%B8%D0%BD/%D0%BE%D0%B1%D1%83%D0%B2%D1%8C/shoponline?page=';
  for (let batchi = 50; batchi < 544; batchi += 100){
    let a = batchi;
    let b = batchi + 1;
    let batch_promises = [];
    console.time('fetching');
    for (let i = a; i < b; i++){
      let path = new URL('./'+i+'.html', dir_path);
      batch_promises.push(fetchWrite(path, catalog_base_link + i));
    }
    await Promise.all(batch_promises);
    console.timeEnd('fetching');
  }
}


async function main() {
  //let html = await fs.promises.readFile(new URL('./data/catalogs/womens-shoes/100.html', import.meta.url), 'utf8');
  //let items = getItems(html);
  //console.log(items.length);
  batchDownload();
}

main();