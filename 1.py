import random, json
W=[("НҰРАЛЫ","Сырым «бұзау еті ауызында кеткен» деп сынаған, Кіші жүздің ханы?"),
("АҚБҰЛАҚ","1838 жылғы 12 шілдедегі Исатай мен Махамбет көтерілісінің шешуші шайқасы өткен өзен?"),
("АҚМОЛА","Кенесары хандығының соңғы астанасы болған бекініс?"),
("НАУРЫЗБАЙ","Кенесарының інісі, батыр?"),
("ЖАНТАЙ","Кенесарының өліміне қатысқан қырғыз манабы?"),
("ОРСК","Есет Көтібарұлы шабуыл жасаған, Жайық бойындағы бекініс?"),
("ЖАҢАҚАЛА","Жанқожа 1856 жылы салған бекіністің аты?"),
("СПЕРАНСКИЙ","1822 және 1824 жылғы жарлықтардың авторы?"),
("ЖӘҢГІР","Махамбет «Хан емессің, қасқырсың» деген Ішкі Орда ханы?"),
("ЖАҢАЕЛЕК","Кенесарыға қарсы салынған шекара шебі?"),
("ШОҚАН","Шыңғыс сұлтанның баласы, қазақтың тұңғыш ғалымы?"),
("ОРЫНБОР","«Елек қорғанысы» деп аталған шеп?"),
("ҚОҚАН","Сырдарияның арғы бетіндегі хандық?"),
("ОТАРШЫЛДЫҚ","Қазақ жерін «бос жатқан жер» деп жариялаған жүйе?"),
("ДОСАН","1870 жылғы Маңғыстау көтерілісінің басшысы?")]

def place(order):
    g={};pl=[]
    def ok(w,r,c,d):
        dr,dc=(0,1) if d=='A' else (1,0)
        if (r-dr,c-dc) in g or (r+dr*len(w),c+dc*len(w)) in g: return False
        n=0
        for i,ch in enumerate(w):
            p=(r+dr*i,c+dc*i)
            if p in g:
                if g[p]!=ch: return False
                n+=1
            else:
                for q in ((p[0]+dc,p[1]+dr),(p[0]-dc,p[1]-dr)):
                    if q in g: return False
        return n>0
    for k,(w,_) in enumerate(order):
        if k==0:
            for i,ch in enumerate(w): g[(0,i)]=ch
            pl.append((w,0,0,'A',_));continue
        best=[]
        for d in 'AD':
            for r in range(-20,20):
                for c in range(-20,20):
                    if ok(w,r,c,d): best.append((r,c,d))
        if not best: continue
        r,c,d=random.choice(best);dr,dc=(0,1) if d=='A' else (1,0)
        for i,ch in enumerate(w): g[(r+dr*i,c+dc*i)]=ch
        pl.append((w,r,c,d,_))
    return g,pl
bp=None
random.seed(1)
for _ in range(300):
    o=sorted(W,key=lambda x:-len(x[0])+random.random()*3)
    g,pl=place(o)
    rs=[p[0] for p in g];cs=[p[1] for p in g]
    area=(max(rs)-min(rs)+1)*(max(cs)-min(cs)+1)
    sc=(len(pl),-area)
    if not bp or sc>bp[0]: bp=(sc,g,pl)
_,g,pl=bp

r0=min(p[0] for p in g);c0=min(p[1] for p in g)
pl=[(w,r-r0,c-c0,d,cl) for w,r,c,d,cl in pl]
pl.sort(key=lambda p:(p[1],p[2],p[3]))
nums={};n=0
for w,r,c,d,cl in pl:
    if (r,c) not in nums: n+=1;nums[(r,c)]=n
cells={}
for w,r,c,d,cl in pl:
    for i,ch in enumerate(w):
        cells[(r+(i if d=='D' else 0),c+(i if d=='A' else 0))]=ch
R=max(p[0] for p in cells)+1;C=max(p[1] for p in cells)+1
data=dict(R=R,C=C,cells={f"{r},{c}":ch for (r,c),ch in cells.items()},nums={f"{r},{c}":v for (r,c),v in nums.items()},
 A=[(nums[(r,c)],cl) for w,r,c,d,cl in pl if d=='A'],D=[(nums[(r,c)],cl) for w,r,c,d,cl in pl if d=='D'],placed=[p[0] for p in pl],miss=[w for w,_ in W if w not in [p[0] for p in pl]])

# --- ВСТАВЬТЕ СЮДА УЛУЧШЕННЫЙ HTML ---
html = """<!doctype html><html lang="kk"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Қазақ көтерілістері — Кроссворд</title>
<style>
:root{
  --bg:#f6f7f9; --card:#ffffff; --fg:#16181d; --muted:#6b7280;
  --line:#c9ced6; --cell:#ffffff; --accent:#2563eb; --ok:#dcfce7; --okb:#16a34a;
  --bad:#fee2e2; --badb:#dc2626; --shadow:0 1px 2px rgba(0,0,0,.06),0 8px 24px rgba(0,0,0,.06);
  --radius:14px;
}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){
  --bg:#0f1115; --card:#171a21; --fg:#e8eaed; --muted:#9aa3af;
  --line:#3a4150; --cell:#1f242e; --accent:#60a5fa; --ok:#12351f; --okb:#22c55e;
  --bad:#3a1414; --badb:#ef4444; --shadow:0 1px 2px rgba(0,0,0,.4),0 12px 32px rgba(0,0,0,.5);
}}
*{box-sizing:border-box}
html,body{margin:0}
body{
  background:var(--bg); color:var(--fg);
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
  padding:calc(16px + env(safe-area-inset-top,0px)) 16px calc(24px + env(safe-area-inset-bottom,0px));
  -webkit-text-size-adjust:100%;
}
header{max-width:1040px;margin:0 auto 16px}
h1{font-size:clamp(20px,4vw,28px);margin:0 0 4px;letter-spacing:-.02em}
.sub{color:var(--muted);font-size:14px;margin:0}
.layout{max-width:1040px;margin:0 auto;display:grid;gap:20px;grid-template-columns:minmax(0,1fr)}
@media(min-width:860px){.layout{grid-template-columns:auto minmax(280px,1fr);align-items:start}}
.card{background:var(--card);border-radius:var(--radius);box-shadow:var(--shadow);padding:16px}
.gridwrap{overflow-x:auto;-webkit-overflow-scrolling:touch;border-radius:10px}
table{border-collapse:separate;border-spacing:0;margin:0 auto}
td{width:34px;height:34px;padding:0;position:relative}
td.c{border:1px solid var(--line)}
td input{
  width:100%;height:100%;border:0;background:var(--cell);color:var(--fg);
  text-align:center;font-size:17px;font-weight:600;text-transform:uppercase;
  padding:0;outline:none;caret-color:var(--accent);border-radius:2px;
  transition:background .15s,box-shadow .15s;
}
td input:focus{box-shadow:inset 0 0 0 2px var(--accent);background:var(--card)}
td i{position:absolute;top:1px;left:3px;font-size:10px;font-style:normal;font-weight:600;color:var(--muted);pointer-events:none}
td.ok input{background:var(--ok);box-shadow:inset 0 0 0 1px var(--okb)}
td.bad input{background:var(--bad);box-shadow:inset 0 0 0 1px var(--badb)}
.toolbar{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px}
button{
  appearance:none;border:1px solid var(--line);background:var(--card);color:var(--fg);
  padding:9px 16px;border-radius:10px;font-size:15px;font-weight:600;cursor:pointer;
  transition:transform .06s,background .15s,border-color .15s;
}
button:hover{border-color:var(--accent)}
button:active{transform:scale(.97)}
button.primary{background:var(--accent);border-color:var(--accent);color:#fff}
.clues h3{font-size:14px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin:0 0 8px}
.clues h3:not(:first-child){margin-top:18px}
.clue{display:flex;gap:10px;padding:7px 8px;border-radius:8px;font-size:14.5px;line-height:1.4}
.clue:hover{background:rgba(127,127,127,.08)}
.clue b{color:var(--accent);min-width:1.6em;text-align:right;font-variant-numeric:tabular-nums}
@media print{
  body{background:#fff;color:#000;padding:0}
  .card{box-shadow:none;border:1px solid #ccc}
  .toolbar{display:none}
  td input{background:#fff}
}
</style></head><body>
<header>
  <h1>Қазақ көтерілістері</h1>
  <p class="sub">Тарихи кроссворд · жауаптарды ұяшықтарға толтырыңыз</p>
</header>
<div class="layout">
  <div class="card">
    <div class="gridwrap"><table id="t"></table></div>
    <div class="toolbar">
      <button class="primary" onclick="chk()">Тексеру</button>
      <button onclick="rev()">Жауаптар</button>
      <button onclick="clr()">Тазалау</button>
    </div>
  </div>
  <div class="card clues">
    <h3>Көлденең</h3><div id="a"></div>
    <h3>Тік</h3><div id="d"></div>
  </div>
</div>
<script>
const D=%s;
const t=document.getElementById('t');
for(let r=0;r<D.R;r++){
  const tr=t.insertRow();
  for(let c=0;c<D.C;c++){
    const td=tr.insertCell(), k=r+','+c;
    if(D.cells[k]){
      td.className='c';
      td.innerHTML=(D.nums[k]?'<i>'+D.nums[k]+'</i>':'')+'<input maxlength="1" inputmode="text" autocomplete="off" autocorrect="off" autocapitalize="characters" spellcheck="false" data-a="'+D.cells[k]+'">';
    }
  }
}
const I=[...document.querySelectorAll('input')];
I.forEach((inp,idx)=>{
  inp.addEventListener('input',()=>{
    inp.value=inp.value.toUpperCase().slice(-1);
    inp.parentNode.classList.remove('ok','bad');
    if(inp.value && I[idx+1]) I[idx+1].focus();
  });
  inp.addEventListener('keydown',e=>{
    if(e.key==='Backspace' && !inp.value && I[idx-1]){I[idx-1].focus();}
  });
});
function chk(){
  I.forEach(i=>{
    const p=i.parentNode;
    p.classList.remove('ok','bad');
    if(!i.value) return;
    p.classList.add(i.value.toUpperCase()===i.dataset.a?'ok':'bad');
  });
}
function rev(){I.forEach(i=>{i.value=i.dataset.a;i.parentNode.classList.remove('bad');i.parentNode.classList.add('ok')})}
function clr(){I.forEach(i=>{i.value='';i.parentNode.classList.remove('ok','bad')})}
const f=(l,id)=>document.getElementById(id).innerHTML=l.map(x=>'<div class="clue"><b>'+x[0]+'.</b><span>'+x[1]+'</span></div>').join('');
f(D.A,'a');f(D.D,'d');
</script></body></html>""" % json.dumps(data, ensure_ascii=False)

# Сохраняем результат в текущую папку
with open('krossvord_gotovyi.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Готово! Файл krossvord_gotovyi.html создан.")