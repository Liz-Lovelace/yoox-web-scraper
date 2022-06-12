import axios from 'axios';
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
    let html = (await axios.get(link)).data;
    if (!html)
      reject(`fetch error: skipping ${link}`);
    await fs.promises.writeFile(path, html);
    resolve();
  });
}

async function batchDownload(catalogLimit){
  let batch_size = 50;
  let dir_path = new URL('./data/catalogs/womens-shoes/', import.meta.url);
  let catalog_base_link = 'https://www.yoox.com/ru/%D0%B4%D0%BB%D1%8F%20%D0%B6%D0%B5%D0%BD%D1%89%D0%B8%D0%BD/%D0%BE%D0%B1%D1%83%D0%B2%D1%8C/shoponline?page=';
  for (let batchi = 1; batchi < catalogLimit; batchi += batch_size){
    let a = batchi;
    let b = Math.min(batchi + batch_size, catalogLimit + 1);
    let batch_promises = [];
    for (let i = a; i < b; i++){
      let path = new URL('./'+i+'.html', dir_path);
      batch_promises.push(fetchWrite(path, catalog_base_link + i));
    }
    await Promise.all(batch_promises);
    console.log(`downloaded catalogs ${a}-${b-1}`)
  }
}

async function main() {
  // How many catalogs to download.
  let total_catalogs = 60;
  await batchDownload(total_catalogs);
  let all_items = [];
  for (let i = 1; i <= total_catalogs; i++){
    let catalogHtml = await fs.promises.readFile(new URL(`./data/catalogs/womens-shoes/${i}.html`, import.meta.url), 'utf8');
    let raw_items = getItems(catalogHtml);
    all_items = all_items.concat(raw_items);
    console.log(`parsed catalog ${i}. Complete: ${(i/total_catalogs*100).toFixed(1)}%`)
  }
  let all_items_str = JSON.stringify(all_items);
  await fs.promises.writeFile(new URL('./unchecked_items.json', import.meta.url), all_items_str);
}

main();