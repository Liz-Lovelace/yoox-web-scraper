import fs from 'fs';

function check(str, optional_fields){
  let required_fields = ['id', 'category_id', 'parent_category_id', 'image_url'];
  //optional fields could be: group_id, product_url, available. Or anything else, really
  required_fields = required_fields.concat(optional_fields);
  let j = JSON.parse(str);
  let problems = '';
  for (let i = 0; i < j.length; i++){
    for (let field_name of required_fields){
      if (!j[i][field_name])
        problems += `#${i} doesn't have field '${field_name}'!`;
      if (j[i][field_name].length < 2)
        problems += `#${i}'s '${field_name}' is less than 2 chars in length - ${j[i][field_name]}!\n`;
    }
  }
  return problems;
}

let stdin = ''
process.stdin.on('data', data => stdin += data);
process.stdin.on('end', () => {
  console.log(check(stdin, ['product_url']));
});
