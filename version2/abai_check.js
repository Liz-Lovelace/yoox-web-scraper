import fs from 'fs';

function fields_filled(j, optional_fields){
  let required_fields = ['id', 'category_id', 'parent_category_id', 'image_url'];
  //optional fields could be: group_id, product_url, available. Or anything else, really
  required_fields = required_fields.concat(optional_fields);
  let problems = [];
  for (let i = 0; i < j.length; i++){
    for (let field_name of required_fields){
      if (!j[i][field_name])
        problems.push( `#${i} doesn't have field '${field_name}'!`);
      else if (j[i][field_name].length < 2)
        problems.push( `#${i}'s '${field_name}' is less than 2 chars in length - ${j[i][field_name]}!\n`);
    }
  }
  return problems;
}

function duplicates(j){
  let data_dump = new Set();
  let duplicates = [];
  let duplicate_ids = [];
  for (let i = 0; i < j.length; i++){
    for (let key of ['id', 'image_url', 'product_url']){
      if (data_dump.has(j[i][key])){
        duplicates.push(`#${i} has a duplicate field '${key}' - ${j[i][key]}`);
        duplicate_ids.push(i);
      }
      data_dump.add(j[i][key]);
    }
  }
  return [duplicates, duplicate_ids];
}

function full_check(j){
  let problems = [];
  problems = problems.concat(fields_filled(j, ['product_url']));
  let dups = duplicates(j, ['product_url']);
  problems = problems.concat(dups[0]);
  for (let i = 0; i < problems.length; i++){
    console.log(problems[i]);
  }
  console.log('full_check done');
}

let stdin = ''
process.stdin.on('data', data => stdin += data);
process.stdin.on('end', async () => {
  let j = JSON.parse(stdin);
  full_check(j);
});
