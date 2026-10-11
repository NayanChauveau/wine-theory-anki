const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const source=fs.readFileSync(path.join(__dirname,'../../templates/mcq/shuffle.js'),'utf8');
function client({bag={},droid,reps=0,random=Math.random,storage=true}={}) {
 const memory={getItem:k=>bag[k]??null,setItem:(k,v)=>bag[k]=v};
 const blocked={getItem(){throw Error('disabled')},setItem(){throw Error('disabled')}};
 const math=Object.create(Math);math.random=random;
 const context={window:{name:''},sessionStorage:storage?memory:blocked,localStorage:storage?memory:blocked,Math:math,JSON,Array,setTimeout:fn=>fn()};
 if(droid){context.AnkiDroidJS={ankiGetCardId:()=>droid,ankiGetCardReps:()=>reps};context.window.AnkiDroidJS=context.AnkiDroidJS;}
 vm.createContext(context);vm.runInContext(source,context);return context;
}
function order(a){return Array.from(a)}
function valid(a,n){assert.deepEqual(order(a).sort((a,b)=>a-b),Array.from({length:n},(_,i)=>i));}
test('each front draws a new order; back restores it across fresh contexts',()=>{
 for(let n=2;n<=10;n++){
  const bag={};let previous;
  for(let presentation=0;presentation<100;presentation++){
   const front=client({bag});const a=order(front.wset3NewOrder(n,'card'));valid(a,n);
   if(previous)assert.notDeepEqual(a,previous);
   front.wset3SaveOrder('card',a);
   assert.deepEqual(order(client({bag}).wset3LoadOrder('card',n)),a);
   previous=a;
  }
 }
});
test('constant RNG cannot repeat the preceding order or loop forever',()=>{
 const c=client({random:()=>0});let prev;
 for(let i=0;i<20;i++){const a=order(c.wset3NewOrder(4,'card'));valid(a,4);if(prev)assert.notDeepEqual(a,prev);c.wset3SaveOrder('card',a);prev=a;}
});
test('malformed/stale permutations do not omit or duplicate options',()=>{
 for(const bad of [[0,0,0],['0','1','2'],[0,1,3],[0,1],null,{length:3}]){
  const c=client();c.wset3Write('card',bad);valid(c.wset3NewOrder(3,'card'),3);valid(c.wset3LoadOrder('card',3),3);
 }
});
test('synchronous AnkiDroid fallback varies with each review and matches without shared storage',()=>{
 for(let n=2;n<=10;n++){
  let previous;
  for(let reps=0;reps<100;reps++){
   const options={droid:'123456',reps,storage:false};
   const a=order(client(options).wset3NewOrder(n,'card'));valid(a,n);
   if(previous)assert.notDeepEqual(a,previous);
   assert.deepEqual(order(client(options).wset3LoadOrder('card',n)),a);previous=a;
  }
 }
});
function choice(i,correct=false){
 const classes=new Set(correct?['correct']:[]);
 return {i:String(i),letter:{textContent:''},events:{},classList:{add:x=>classes.add(x),remove:x=>classes.delete(x),contains:x=>classes.has(x)},getAttribute:k=>k==='data-i'?String(i):null,setAttribute(){},querySelector(){return this.letter},addEventListener(k,fn){this.events[k]=fn}};
}
function box(nodes){
 const attrs={};const classes=new Set();
 return {nodes,classList:{add:x=>classes.add(x)},getAttribute:k=>k==='data-card'?'same-card':attrs[k],setAttribute:(k,v)=>attrs[k]=v,querySelectorAll(){return this.nodes},appendChild(node){this.nodes=this.nodes.filter(x=>x!==node);this.nodes.push(node)}};
}
test('whole presentation keeps selected answer identity and clears the previous pick',()=>{
 const c=client({random:()=>0.25});let front,back;
 c.document={querySelector:s=>back||front};c.pycmd=()=>{};
 for(let review=0;review<10;review++){
  front=box([choice(0),choice(1),choice(2)]);back=null;c.wset3ShuffleChoices(false);
  assert.equal(c.wset3LoadPick('wset3-mcq:same-card'),null);
  const shown=front.nodes.map(x=>x.i);front.nodes[1].events.click({preventDefault(){},stopPropagation(){}});const picked=front.nodes[1].i;
  back=box([choice(0,true),choice(1),choice(2)]);c.wset3ShuffleChoices(true);
  assert.deepEqual(back.nodes.map(x=>x.i),shown);
  assert.equal(back.nodes.find(x=>x.classList.contains('picked')).i,picked);
  assert.equal(back.nodes.filter(x=>x.classList.contains('correct')).length,1);
  assert.equal(back.nodes.find(x=>x.classList.contains('correct')).i,'0');
  assert.deepEqual(back.nodes.map(x=>x.letter.textContent),['A','B','C']);
 }
});
