import { readFileSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import { lint } from 'markdownlint/promise';
import mlc from 'markdown-link-check';
const root = import.meta.dirname;
const source = resolve(root, 'scratch/installatie.md');
const target = resolve(root, 'workspace/docs/guides/installatie.md');
const content = readFileSync(source, 'utf8');
console.log('target exists BEFORE:', existsSync(target));
console.log('markdownlint MD051:', JSON.stringify(await lint({strings:{'installatie.md':content},config:{default:false,MD051:true}})));
for (const [name, base] of [['scratch',resolve(root,'scratch')],['intended',resolve(root,'workspace/docs/guides')]]) {
  const result = await new Promise((ok, reject) => mlc(content,{baseUrl:pathToFileURL(base).href+'/'},(err,res)=>err?reject(err):ok(res)));
  console.log('markdown-link-check',name,JSON.stringify(result));
}
console.log('target exists AFTER:', existsSync(target));
