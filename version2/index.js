import cheerio from 'cheerio';
import fetch from 'node-fetch';
import fs from 'fs';
import { URL } from 'url';

function getItems(html) {
  //this operation takes by far the most time
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
    } else
      throw 'can\'t find image!!!';
    //this removes url arguments after '?'
    properties.imageUrl = properties.imageUrl.match(/(^.*)\?/)[1];

    itemProperties.push(properties);
  }
  return itemProperties;
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

//not sure what this does lol
async function writeRawJson(){
  let items = []
  for (let i = 1; i <=544; i++){
    //this is wrong i'm pretty sure
    let html = await fs.promises.readFile(new URL('./data/catalogs/womens-shoes/100.html', import.meta.url), 'utf8');
    let catalogItems = getItems(html);
    findBrokenItems(catalogItems);
    items = items.concat(catalogItems);
    console.log(i + ' ' + i / 544 * 100 + '%')
  }
  console.log(items.length);
  console.log('writing...');
  await fs.promises.writeFile(new URL('./raw.json', import.meta.url), JSON.stringify(items));
  console.log('done!');
}

function rawToABAi(raw){
  let formatted = [];
  for (let i = 0; i < raw.length; i++){
    let obj = {};
    obj.id = raw[i].id
    obj.category_id = raw[i].categoryId;
    obj.parent_category_id = raw[i].parentCategoryId;
    obj.product_url = raw[i].productUrl;
    obj.image_url = raw[i].imageUrl;
    formatted.push(obj);
  }
  return formatted;
}

async function main() {
  let all_items = [];
  //don't forget this  vvv
  for (let i = 1; i <= 544; i++){
    let catalogHtml = await fs.promises.readFile(new URL(`./data/catalogs/womens-shoes/${i}.html`, import.meta.url), 'utf8');
    let raw_items = getItems(catalogHtml);
    let ABAi_items = rawToABAi(raw_items);
    all_items = all_items.concat(ABAi_items);
    if (i % 10 == 0)
      console.log(`${i}  ${(i/544*100).toFixed(1)}%`)
  }
  let all_items_str = JSON.stringify(all_items);
  await fs.promises.writeFile(new URL('./unchecked_items.json', import.meta.url), all_items_str);
}

main();