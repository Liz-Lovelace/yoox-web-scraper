import cheerio from 'cheerio';
import fetch from 'node-fetch';
import fs from 'fs';
import { URL } from 'url';

class Catalog {
  constructor(url){
    this.url = url;
    this.html = ''
  }
  
  async getHtml() {
    if (!this.html){
      this.html = await (await fetch(this.url)).text();
    }
    return this.html;
  }
}

async function main(){
  let catalogUrl = 'https://www.yoox.com/ru/%D0%B4%D0%BB%D1%8F%20%D0%B6%D0%B5%D0%BD%D1%89%D0%B8%D0%BD/shoponline/%D0%B4%D0%B6%D0%B8%D0%BD%D1%81%D0%BE%D0%B2%D1%8B%D0%B5%20%D0%B1%D1%80%D1%8E%D0%BA%D0%B8_c#/dept=clothingwomen&gender=D&page=1&attributes=%7b%27ctgr%27%3a%5b%27pntlnjns%27%5d%7d&season=X';
  let cat = new Catalog(catalogUrl);
}

main();