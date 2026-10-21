import random, json

W = [
("НҰРАЛЫ","Сырым «бұзау еті ауызында кеткен» деп сынаған, Кіші жүздің ханы?"),
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
("ДОСАН","1870 жылғы Маңғыстау көтерілісінің басшысы?")
]

# Сортируем слова по длине (от длинных к коротким), чтобы каркас был плотным
words = sorted(W, key=lambda x: len(x[0]), reverse=True)
grid = {}
placed = []

# Ставим первое слово
w1, q1 = words[0]
for i, ch in enumerate(w1):
    grid[(0, i)] = ch
placed.append({"word": w1, "clue": q1, "r": 0, "c": 0, "dir": "A"})

for w, q in words[1:]:
    best = None
    for pw in placed:
        p_w, p_r, p_c, p_dir = pw["word"], pw["r"], pw["c"], pw["dir"]
        for i, ch in enumerate(w):
            for j, p_ch in enumerate(p_w):
                if ch == p_ch:
                    if p_dir == "A":
                        r, c, n_dir = p_r - i, p_c + j, "D"
                    else:
                        r, c, n_dir = p_r + j, p_c - i, "A"
                    
                    valid = True
                    for k, char in enumerate(w):
                        nr = r + (k if n_dir == "D" else 0)
                        nc = c + (k if n_dir == "A" else 0)
                        if (nr, nc) in grid:
                            if grid[(nr, nc)] != char:
                                valid = False; break
                        else:
                            if n_dir == "A":
                                if (nr-1, nc) in grid or (nr+1, nc) in grid: valid = False; break
                            else:
                                if (nr, nc-1) in grid or (nr, nc+1) in grid: valid = False; break
                    
                    if valid:
                        if n_dir == "A":
                            if (r, c-1) in grid or (r, c+len(w)) in grid: valid = False
                        else:
                            if (r-1, c) in grid or (r+len(w), c) in grid: valid = False
                    
                    if valid:
                        best = (r, c, n_dir); break
            if best: break
        if best: break
    
    if best:
        r, c, n_dir = best
        for k, char in enumerate(w):
            nr = r + (k if n_dir == "D" else 0)
            nc = c + (k if n_dir == "A" else 0)
            grid[(nr, nc)] = char
        placed.append({"word": w, "clue": q, "r": r, "c": c, "dir": n_dir})

min_r = min(k[0] for k in grid.keys())
min_c = min(k[1] for k in grid.keys())
max_r = max(k[0] for k in grid.keys())
max_c = max(k[1] for k in grid.keys())

shift_r, shift_c = -min_r, -min_c
cells = {f"{r+shift_r},{c+shift_c}": ch for (r,c), ch in grid.items()}

placed.sort(key=lambda x: (x["r"], x["c"]))
nums = {}; counter = 1
A_clues, D_clues = [], []

for pw in placed:
    r, c = pw["r"] + shift_r, pw["c"] + shift_c
    if (r, c) not in nums:
        nums[(r, c)] = counter; counter += 1
    if pw["dir"] == "A": A_clues.append([nums[(r, c)], pw["clue"]])
    else: D_clues.append([nums[(r, c)], pw["clue"]])

data = {
    "R": max_r - min_r + 1, "C": max_c - min_c + 1,
    "cells": cells, "nums": {f"{r},{c}": v for (r, c), v in nums.items()},
    "A": A_clues, "D": D_clues
}

# Дизайн в точности как на твоем скриншоте (с кнопкой "Басып шығару")
html = """<!doctype html>
<html lang="kk">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Кроссворд</title>
<style>
:root{--bg:#1e1e1e;--fg:#e0e0e0;--line:#3e3e3e;--cell:#2d2d2d;--accent:#4db8ff}
body{background:var(--bg);color:var(--fg);font-family:"Segoe UI",serif;margin:0;padding:20px;display:flex;flex-direction:column;align-items:center}
h2{font-size:24px;margin-bottom:20px;font-weight:normal}
table{border-collapse:collapse;margin-bottom:20px}
td{width:32px;height:32px;padding:0;position:relative}
td.c{border:1px solid var(--line);background:var(--cell)}
td input{width:100%;height:100%;background:transparent;border:none;color:#fff;text-align:center;font-size:16px;text-transform:uppercase;outline:none}
td input:focus{background:rgba(77,184,255,0.2)}
td i{position:absolute;top:1px;left:2px;font-size:9px;font-style:normal;color:#aaa}
.toolbar{display:flex;gap:10px;flex-wrap:wrap;justify-content:center;margin-bottom:30px}
button{background:transparent;border:1px solid var(--accent);color:var(--accent);padding:8px 16px;border-radius:4px;cursor:pointer;font-size:14px}
button:hover{background:rgba(77,184,255,0.1)}
.clues{width:100%;max-width:600px;text-align:left}
.clues h3{color:var(--accent);font-size:18px;margin-bottom:10px}
.clue{font-size:14px;line-height:1.4;margin-bottom:8px;display:flex;gap:8px}
.clue b{min-width:20px}
</style>
</head>
<body>
<h2>Қазақ көтерілістері</h2>
<div id="grid"></div>
<div class="toolbar">
  <button onclick="rev()">Жауаптарды көрсету</button>
  <button onclick="clr()">Тазалау</button>
  <button onclick="window.print()">Басып шығару</button>
</div>
<div class="clues">
  <h3>Көлденең</h3><div id="a"></div>
  <h3>Тік</h3><div id="d"></div>
</div>
<script>
const D=%s;
const g=document.getElementById('grid');
let t=document.createElement('table');
for(let r=0;r<D.R;r++){
  let tr=t.insertRow();
  for(let c=0;c<D.C;c++){
    let td=tr.insertCell(),k=r+','+c;
    if(D.cells[k]){
      td.className='c';
      td.innerHTML=(D.nums[k]?'<i>'+D.nums[k]+'</i>':'')+'<input maxlength="1" data-a="'+D.cells[k]+'">';
    }
  }
}
g.appendChild(t);
const I=[...document.querySelectorAll('input')];
function rev(){I.forEach(i=>i.value=i.dataset.a)}
function clr(){I.forEach(i=>i.value='')}
const f=(l,id)=>document.getElementById(id).innerHTML=l.map(x=>'<div class="clue"><b>'+x[0]+'.</b><span>'+x[1]+'</span></div>').join('');
f(D.A,'a');f(D.D,'d');
</script>
</body>
</html>""" % json.dumps(data, ensure_ascii=False)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Готово! Файл index.html создан.")