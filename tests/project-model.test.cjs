const {test}=require('node:test');
const assert=require('node:assert/strict');
const model=require('../studio/v2/project-model.js');
test('legacy projects default to empty project-owned content',()=>{
 assert.deepEqual(model.content(),{lyrics:'',styleIntent:'',stylePrompt:'',annotations:[],sampler:{}});
 assert.equal(model.events({hits:[]},{}).length,0);
});
test('project event and text changes do not leak to another project',()=>{
 const a={hits:[{i:1,s:0,e:1,label:'alpha',ipa:'a',cat:'TONAL'}]},b={hits:[{i:1,s:0,e:.5,label:'beta',cat:'PERC'}]};
 assert.equal(model.events(a,{})[0].ipa,'a');
 assert.equal(model.events(b,{})[0].ipa,'');
 const one=model.content({lyrics:'one'}),two=model.content({lyrics:'two'});one.lyrics='changed';assert.equal(two.lyrics,'two');
 assert.equal(model.events(b,{})[0].label,'beta');
});
test('annotations must identify and fit the selected media',()=>{
 const good={fileName:'b.wav',duration:2,events:[{start:.5,end:1,text:'hi',ipa:'haɪ'}]};
 assert.equal(model.importAnnotations(good,'b.wav',2)[0].ipa,'haɪ');
 assert.throws(()=>model.importAnnotations(good,'a.wav',2));
 assert.throws(()=>model.importAnnotations(good,'b.wav',3));
 assert.throws(()=>model.importAnnotations({...good,events:[{start:1,end:3}]},'b.wav',2));
});
test('prompt drafts use the active project and never insert demo lyrics',()=>{
 const p=model.prompt({bpm:93,hits:[{cat:'KICK'}]},{styleIntent:'Ambient dub'});
 assert.match(p,/93 BPM/);assert.match(p,/Ambient dub/);assert.match(p,/kick/);assert.doesNotMatch(p,/BOW|skibidi|IMG_3268/);
});
