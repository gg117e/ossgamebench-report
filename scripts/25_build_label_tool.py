"""Build a self-contained HTML tool for the author's blind labels.

Usage:
    python -I scripts/25_build_label_tool.py validation/samples_game_v3/human_blind.jsonl \
        validation/human_project_review.md validation/label_tool.html

The page contains only the issue titles/bodies and the project table.
It contains no LLM label of the audit sample. Issue text is inserted with
textContent only (it is untrusted data).
"""
import json
import sys
from pathlib import Path

CATEGORIES = [
    ("gameplay", "ゲームのルール・状態・AI・移動・衝突・報酬などの異常"),
    ("ui", "メニュー・HUD・文字・入力欄・ツールチップの表示や操作の異常"),
    ("crash_hang", "異常終了、例外で続行できない、完全に固まる"),
    ("visual", "ワールドの描画・テクスチャ・アニメーション・カメラの異常（メニューや HUD は ui）"),
    ("audio", "音が出ない、違う音、同期や長さの異常"),
    ("network", "接続できない、切断、プレイヤー間の状態のずれ"),
    ("save_load", "保存できない、読み込めない、セーブの破損"),
    ("performance", "FPS 低下、遅い、メモリ増大（完全停止は crash_hang）"),
    ("tooling_other", "ビルド・エディタ・API などの異常や、上記以外の明確な不具合"),
    ("unknown", "情報不足、または独立した複数のバグで主な症状を決められない"),
]
DOMAINS = [
    ("player_runtime", "プレイヤーが遊んでいる最中のゲーム"),
    ("editor_tooling", "マップ・MOD エディタ、開発用ツール、デバッグ機能"),
    ("build_distribution", "ビルド、インストール、起動前の環境"),
    ("project_meta", "文書、CI、リポジトリ設定"),
    ("unknown", "判断できない"),
]


def read_projects(path):
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 8 and cells[0].isdigit():
            rows.append({
                "rank": int(cells[0]), "project": cells[1], "fixes": cells[2],
                "with_test": cells[3], "scope": cells[4], "type": cells[5],
                "web": cells[6], "reason": cells[7],
            })
    return rows


def main():
    blind, projects_md, out = map(Path, sys.argv[1:4])
    issues = []
    for line in blind.read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            issues.append({"sample_id": r["sample_id"], "title": r.get("title") or "",
                           "body": r.get("body") or ""})
    data = {"issues": issues, "projects": read_projects(projects_md),
            "categories": CATEGORIES, "domains": DOMAINS}
    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    out.write_text(TEMPLATE.replace("__DATA__", blob), encoding="utf-8", newline="\n")
    print(f"issues={len(issues)} projects={len(data['projects'])} -> {out}")


TEMPLATE = r"""<!doctype html>
<html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>判定ツール</title>
<style>
:root{--bg:#f7f7f5;--fg:#1c1c1c;--mut:#666;--card:#fff;--line:#d8d8d4;--acc:#2a78d6;--ok:#2e8b57}
@media (prefers-color-scheme:dark){:root{--bg:#18191b;--fg:#e8e8e6;--mut:#a0a0a0;--card:#222326;--line:#3a3b3f;--acc:#6aa9ee;--ok:#5fc08a}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.6 system-ui,"Yu Gothic UI","Meiryo",sans-serif}
header{position:sticky;top:0;background:var(--card);border-bottom:1px solid var(--line);padding:8px 16px;display:flex;gap:12px;align-items:center;flex-wrap:wrap;z-index:2}
header b{font-size:16px}
button{font:inherit;padding:6px 12px;border:1px solid var(--line);border-radius:6px;background:var(--card);color:var(--fg);cursor:pointer}
button.on{background:var(--acc);border-color:var(--acc);color:#fff}
button.primary{background:var(--acc);border-color:var(--acc);color:#fff}
main{max-width:1200px;margin:0 auto;padding:16px;display:grid;grid-template-columns:minmax(0,1fr) 380px;gap:16px}
@media (max-width:900px){main{grid-template-columns:1fr}}
.card{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:14px}
h2{font-size:17px;margin:0 0 4px}
.mut{color:var(--mut);font-size:13px}
pre{white-space:pre-wrap;overflow-wrap:anywhere;max-height:62vh;overflow:auto;font:13px/1.5 ui-monospace,Consolas,monospace;margin:8px 0 0;padding:10px;border:1px solid var(--line);border-radius:6px;background:var(--bg)}
fieldset{border:0;padding:0;margin:0 0 14px}
legend{font-weight:600;padding:0;margin-bottom:4px}
label.opt{display:block;padding:4px 8px;border:1px solid var(--line);border-radius:6px;margin:3px 0;cursor:pointer}
label.opt.sel{border-color:var(--acc);outline:1px solid var(--acc)}
label.opt small{display:block;color:var(--mut);line-height:1.35}
.row{display:flex;gap:6px;flex-wrap:wrap}
textarea,input[type=text]{width:100%;font:inherit;padding:6px;border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--fg)}
.dots{display:flex;flex-wrap:wrap;gap:3px}
.dot{width:22px;height:22px;border-radius:4px;border:1px solid var(--line);font-size:11px;display:flex;align-items:center;justify-content:center;cursor:pointer;background:var(--card)}
.dot.done{background:var(--ok);color:#fff;border-color:var(--ok)}
.dot.cur{outline:2px solid var(--acc)}
table{border-collapse:collapse;width:100%;font-size:14px}
th,td{border-bottom:1px solid var(--line);padding:6px;text-align:left;vertical-align:top}
.wide{grid-column:1/-1;overflow-x:auto}
.hide{display:none}
</style></head><body>
<header>
  <b>判定ツール</b>
  <button id="tabI" class="on">バグ報告 50 件</button>
  <button id="tabP">プロジェクト 30 件</button>
  <span id="prog" class="mut"></span>
  <span style="flex:1"></span>
  <button id="dl" class="primary">結果を保存（ダウンロード）</button>
</header>

<main id="viewI">
  <section class="card">
    <div class="row" style="justify-content:space-between;align-items:center">
      <span class="mut" id="pos"></span>
      <span class="row"><button id="prev">← 前</button><button id="next">次 →</button></span>
    </div>
    <h2 id="title"></h2>
    <div class="mut" id="sid"></div>
    <pre id="body"></pre>
    <div class="mut" id="trunc"></div>
  </section>
  <aside class="card">
    <fieldset><legend>1. 本当にバグの報告か（必須）</legend><div class="row" id="fBug"></div>
      <div class="mut">機能の要望や質問なら no。</div></fieldset>
    <fieldset><legend>2. 主な症状（必須）</legend><div id="fCat"></div></fieldset>
    <fieldset><legend>3. 場面（任意）</legend><div id="fDom"></div></fieldset>
    <fieldset><legend>4. 自信（任意）</legend><div class="row" id="fConf"></div></fieldset>
    <fieldset><legend>5. 理由のメモ（任意）</legend><textarea id="fWhy" rows="2"></textarea></fieldset>
    <div class="dots" id="dots"></div>
    <p class="mut">タイトルと本文だけで判断します。GitHub のページや画像の中身は見ません。入力はこのブラウザに自動で保存されます。数字キー 1〜9, 0 で症状、←→ で移動できます。</p>
  </aside>
</main>

<main id="viewP" class="hide">
  <section class="card wide">
    <p>LLM が付けた分類が正しいかを確認します。GitHub のページを見て判断して構いません。正しければ「正しい」、違う場合は「違う」を選んで正しい内容を書いてください。</p>
    <p class="mut">ゲーム本体か：game / engine_tool。種類：discrete（手番や選択で進む）/ continuous（リアルタイムで進む）/ mixed。Web：ブラウザやチャットのボットで遊ぶなら True。</p>
    <table><thead><tr><th>#</th><th>プロジェクト</th><th>修正</th><th>ゲーム本体か</th><th>種類</th><th>Web</th><th>LLM の根拠</th><th>確認</th><th>違う場合の正しい内容</th></tr></thead><tbody id="ptab"></tbody></table>
  </section>
</main>

<script id="data" type="application/json">__DATA__</script>
<script>
const D = JSON.parse(document.getElementById('data').textContent);
const KEY = 'adse-label-tool-v1';
const LIMIT = 8000;
let S = {issues:{}, projects:{}, cur:0};
try { const s = JSON.parse(localStorage.getItem(KEY)); if (s) S = Object.assign(S, s); } catch(e) {}
const save = () => { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch(e) {} };
const $ = id => document.getElementById(id);
const ans = () => { const id = D.issues[S.cur].sample_id; return S.issues[id] || (S.issues[id] = {}); };
const done = a => a && a.is_actual_bug && a.primary_category;

function radio(box, name, opts, field, big) {
  box.textContent = '';
  opts.forEach(([v, desc], i) => {
    const l = document.createElement('label'); l.className = 'opt'; l.dataset.v = v;
    const r = document.createElement('input'); r.type = 'radio'; r.name = name; r.value = v;
    r.addEventListener('change', () => { ans()[field] = v; save(); paint(); });
    l.append(r, ' ', big ? ((i + 1) % 10) + '. ' + v : v);
    if (desc) { const s = document.createElement('small'); s.textContent = desc; l.append(s); }
    box.append(l);
  });
}
radio($('fBug'), 'bug', [['yes'], ['no'], ['unknown']], 'is_actual_bug');
radio($('fCat'), 'cat', D.categories, 'primary_category', true);
radio($('fDom'), 'dom', D.domains, 'issue_domain');
radio($('fConf'), 'conf', [['high'], ['medium'], ['low']], 'confidence');
$('fWhy').addEventListener('input', e => { ans().rationale = e.target.value; save(); });

function setRadios(box, v) {
  box.querySelectorAll('label.opt').forEach(l => {
    const on = l.dataset.v === v; l.classList.toggle('sel', on); l.querySelector('input').checked = on;
  });
}
function paint() {
  const it = D.issues[S.cur], a = ans();
  $('pos').textContent = (S.cur + 1) + ' / ' + D.issues.length;
  $('title').textContent = it.title; $('sid').textContent = it.sample_id;
  const long = it.body.length > LIMIT;
  $('body').textContent = long ? it.body.slice(0, LIMIT) : it.body;
  $('trunc').textContent = long ? '（本文が長いため、先頭 ' + LIMIT + ' 文字だけ表示しています。全体は ' + it.body.length + ' 文字）' : '';
  setRadios($('fBug'), a.is_actual_bug); setRadios($('fCat'), a.primary_category);
  setRadios($('fDom'), a.issue_domain); setRadios($('fConf'), a.confidence);
  $('fWhy').value = a.rationale || '';
  const dots = $('dots'); dots.textContent = '';
  let n = 0;
  D.issues.forEach((x, i) => {
    const d = document.createElement('div'); d.className = 'dot'; d.textContent = i + 1;
    if (done(S.issues[x.sample_id])) { d.classList.add('done'); n++; }
    if (i === S.cur) d.classList.add('cur');
    d.addEventListener('click', () => go(i)); dots.append(d);
  });
  const pn = D.projects.filter(p => (S.projects[p.project] || {}).check).length;
  $('prog').textContent = 'バグ報告 ' + n + ' / ' + D.issues.length + '　プロジェクト ' + pn + ' / ' + D.projects.length;
}
function go(i) { S.cur = Math.max(0, Math.min(D.issues.length - 1, i)); save(); paint(); $('body').scrollTop = 0; }
$('prev').onclick = () => go(S.cur - 1); $('next').onclick = () => go(S.cur + 1);
document.addEventListener('keydown', e => {
  if (['TEXTAREA', 'INPUT'].includes(e.target.tagName) && e.target.type !== 'radio') return;
  if ($('viewI').classList.contains('hide')) return;
  if (e.key === 'ArrowRight') go(S.cur + 1);
  else if (e.key === 'ArrowLeft') go(S.cur - 1);
  else if (/^[0-9]$/.test(e.key)) { const i = e.key === '0' ? 9 : +e.key - 1; ans().primary_category = D.categories[i][0]; save(); paint(); }
});

const ptab = $('ptab');
D.projects.forEach(p => {
  const st = S.projects[p.project] || (S.projects[p.project] = {});
  const tr = document.createElement('tr');
  const cell = t => { const td = document.createElement('td'); td.textContent = t; return td; };
  const link = document.createElement('a'); link.href = 'https://github.com/' + p.project; link.target = '_blank'; link.rel = 'noopener'; link.textContent = p.project;
  const tdl = document.createElement('td'); tdl.append(link);
  const tdc = document.createElement('td'); tdc.className = 'row';
  [['ok', '正しい'], ['wrong', '違う']].forEach(([v, t]) => {
    const b = document.createElement('button'); b.textContent = t; b.classList.toggle('on', st.check === v);
    b.onclick = () => { st.check = v; save(); tdc.querySelectorAll('button').forEach(x => x.classList.remove('on')); b.classList.add('on'); paint(); };
    tdc.append(b);
  });
  const inp = document.createElement('input'); inp.type = 'text'; inp.value = st.correction || '';
  inp.placeholder = '例：種類は continuous';
  inp.addEventListener('input', () => { st.correction = inp.value; save(); });
  const tdi = document.createElement('td'); tdi.append(inp);
  tr.append(cell(p.rank), tdl, cell(p.fixes), cell(p.scope), cell(p.type), cell(p.web), cell(p.reason), tdc, tdi);
  ptab.append(tr);
});

function tab(i) {
  $('viewI').classList.toggle('hide', !i); $('viewP').classList.toggle('hide', i);
  $('tabI').classList.toggle('on', i); $('tabP').classList.toggle('on', !i);
}
$('tabI').onclick = () => tab(true); $('tabP').onclick = () => tab(false);

function download(name, obj) {
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([JSON.stringify(obj, null, 2) + '\n'], {type: 'application/json'}));
  a.download = name; document.body.append(a); a.click(); a.remove();
}
$('dl').onclick = () => {
  const issues = D.issues.map(x => { const a = S.issues[x.sample_id] || {}; return {
    sample_id: x.sample_id, is_actual_bug: a.is_actual_bug || '', primary_category: a.primary_category || '',
    issue_domain: a.issue_domain || '', confidence: a.confidence || '', rationale: a.rationale || '' }; });
  const projects = D.projects.map(p => { const s = S.projects[p.project] || {}; return {
    project: p.project, llm_scope: p.scope, llm_type: p.type, llm_web: p.web, check: s.check || '', correction: s.correction || '' }; });
  const missI = issues.filter(a => !a.is_actual_bug || !a.primary_category).length;
  const missP = projects.filter(p => !p.check).length;
  if ((missI || missP) && !confirm('未入力があります（バグ報告 ' + missI + ' 件、プロジェクト ' + missP + ' 件）。このまま保存しますか？')) return;
  download('human_answers.json', issues);
  setTimeout(() => download('human_project_review.json', projects), 400);
};
paint();
</script>
</body></html>
"""

if __name__ == "__main__":
    main()
