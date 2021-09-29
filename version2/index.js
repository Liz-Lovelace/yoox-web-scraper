import cheerio from 'cheerio';
import fetch from 'node-fetch';
import fs from 'fs';
import { URL } from 'url';

function getItems(html) {
  let $ = cheerio.load(html);
  let items = $('.itemContainer');
  let itemProperties = [];
  //console.log(items);
  for (let i = 0; i < items.length; i++){
    let item = items[i];
    let properties = {}
    properties.parentCategoryId = item.attribs['data-macrocategory_id'];
    properties.parentCategoryName = item.attribs['data-macrocategory'];
    properties.categoryId = item.attribs['data-category_id'];
    properties.categoryName = item.attribs['data-category'];
    properties.id = item.attribs['data-current-cod10'];
    //properties.productUrl = item.children('.itemImg > a').attribs['href'];
    //imageUrl
    itemProperties.push(properties);
    if (i == 0) console.log(item.children);
  }
  return itemProperties;
}

async function main() {
  let ankleBootsUrl = 'https://www.yoox.com/nl/women/shoponline/ankle%20boots_c#/dept=shoeswomen&gender=D&page=1&season=X';
  let html = await fs.promises.readFile(new URL('./data/ankleBoots.html', import.meta.url), 'utf8');
  console.log(getItems(html)[0]);
}

main();