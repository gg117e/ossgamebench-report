"""Exploratory counts used to choose a research direction (tests in bug fixes, bug-report artefacts).

Usage:
    python -I scripts/04_explore_ideas.py <raw_dir> <interim_dir> > results/idea_exploration.txt

All classifications here are crude keyword/path rules for a feasibility check, NOT validated measures.
"""
import os, re, sys, pandas as pd
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import duplicated_projects, is_bug_label, is_nofix_label, CORE_EXT, ext_of
RAW, INTERIM = sys.argv[1], sys.argv[2]; T=RAW+"/tables/"; dups=duplicated_projects()
def load(n,c):
    d=pd.read_parquet(T+n+".parquet",columns=c); d["pk"]=d.project.str.lower(); return d[~d.pk.isin(dups)]
TEST_RE=re.compile(r"(^|/)(tests?|__tests__|spec|specs|testing|unittests?|playmodetests?|editmodetests?)(/|$)|"
                   r"(^|/)test_[^/]*$|_tests?\.[a-z]+$|tests?\.(cs|java|kt|scala|cpp|cc|h|hpp|ts|js|py|rs|go|gd|lua)$|\.(spec|test)\.[jt]sx?$", re.I)
is_test=lambda p: bool(TEST_RE.search(p))
cm=pd.read_parquet(INTERIM+"/commits_slim.parquet",columns=["project_key","sha","message","files"]).rename(columns={"project_key":"pk"})
cm=cm[~cm.pk.isin(dups)]
cm["test"]=cm.files.map(lambda fs:any(is_test(f) for f in fs))
pt=cm.groupby("pk").test.agg(["any","mean"])
print(f"projects with any test-file change in history: {pt['any'].sum()} / {len(pt)}; commits touching tests {100*cm.test.mean():.1f}%")
print("share of commits touching tests per project (among projects with tests):", pt[pt['any']]['mean'].describe().round(3).to_dict())
# bug fixes via paths A|B
iss=load("issue",["project","number","labels","title","body","state","created_at","closed_at"])
iss["bug"]=iss.labels.map(lambda ls:any(is_bug_label(l) for l in ls) and not any(is_nofix_label(l) for l in ls))
bugs=iss[iss.bug].copy()
ipr=load("issue_pr",["project","issue_number","pr_number"]); pr=load("pr",["project","number","state"]); prc=load("pr_commit",["project","pr_number","commit_sha"])
m=bugs.rename(columns={"number":"issue_number"})[["pk","issue_number"]].merge(ipr[["pk","issue_number","pr_number"]],on=["pk","issue_number"])
m=m.merge(pr[pr.state=="MERGED"].rename(columns={"number":"pr_number"})[["pk","pr_number"]],on=["pk","pr_number"])
a=m.merge(prc.rename(columns={"commit_sha":"sha"})[["pk","pr_number","sha"]],on=["pk","pr_number"])
ref=cm.message.fillna("").str.extractall(r"\(#(\d+)\)|Merge pull request #(\d+)")
ref["pr_number"]=ref[0].fillna(ref[1]).astype(int)
pb=cm[["pk","sha"]].join(ref["pr_number"].droplevel(1),how="inner")
b=m.merge(pb,on=["pk","pr_number"])
fx=pd.concat([a[["pk","issue_number","sha"]],b[["pk","issue_number","sha"]]]).drop_duplicates().merge(cm[["pk","sha","files","test"]],on=["pk","sha"])
ex=fx[["pk","issue_number","files"]].explode("files").dropna()
ex["test"]=ex.files.map(is_test); ex["asset"]=ex.files.map(ext_of).isin(CORE_EXT)
ex["code"]=~ex.test & ~ex.asset
pi=ex.groupby(["pk","issue_number"]).agg(test=("test","any"),asset=("asset","any"),code=("code","any"))
proj_has_tests=set(pt[pt['any']].index)
pi=pi.reset_index(); pi["proj_tests"]=pi.pk.isin(proj_has_tests)
print(f"bug fixes with files: {len(pi):,}; fix includes test change: {pi.test.sum():,} ({100*pi.test.mean():.1f}%)")
print(f"  in projects that have tests at all: {pi.proj_tests.sum():,} fixes, of which with test {100*pi[pi.proj_tests].test.mean():.1f}%")
print("  test share: asset-touching fixes %.1f%% vs code-only fixes %.1f%%" % (100*pi[pi.asset].test.mean(),100*pi[~pi.asset].test.mean()))
print("  asset-only fixes (no code, no test):", int((pi.asset & ~pi.code & ~pi.test).sum()))
pp=pi.groupby("pk").test.agg(["size","mean"]); pp=pp[pp["size"]>=30]
print("per project (>=30 fixes) share of fixes with tests:", pp["mean"].describe().round(3).to_dict(), "projects", len(pp))
# crude bug categories from title+body keywords
cats={"crash":r"crash|segfault|exception|freez|hang|stack ?trace|null ?pointer",
      "visual":r"render|graphic|texture|sprite|shader|visual|flicker|glitch|animation|camera|display",
      "audio":r"sound|audio|music|sfx",
      "ui":r"\bui\b|menu|button|hud|tooltip|dialog|font|text overlap",
      "gameplay/rules":r"rule|damage|score|level|quest|spell|unit|card|ai\b|balance|collision|physics|move",
      "network/multiplayer":r"network|multiplayer|server|desync|lag|connect|sync",
      "save/load":r"save|load|savegame|corrupt",
      "performance":r"performance|slow|fps|lag|memory leak|stutter"}
txt=(bugs.title.fillna("")+" "+bugs.body.fillna("").str[:2000]).str.lower()
for k,p in cats.items(): bugs[k]=txt.str.contains(p,regex=True)
lab=bugs.set_index(["pk","number"])[list(cats)]
pj=pi.set_index(["pk","issue_number"]).join(lab.rename_axis(["pk","issue_number"]),how="left")
print("crude category (title/body keywords): share of all bugs | n fixes | % fixes with test")
for k in cats: print(f"  {k:20s} {100*bugs[k].mean():5.1f}% | {int(pj[k].sum()):6,} | {100*pj[pj[k]==True].test.mean():5.1f}%")
# reproduction artefacts in bug reports
body=bugs.body.fillna("")
art={"image/screenshot":r"\.(?:png|jpe?g|gif)\b|user-images\.githubusercontent|github\.com/user-attachments/assets",
     "video":r"\.(?:mp4|webm|mov)\b|youtu\.?be|streamable|imgur\.com/.*\.gifv",
     "save file":r"save ?(?:file|game)|\.sav\b|savegame",
     "log/stacktrace":r"stack ?trace|traceback|\bat [\w\.$]+\(|\.log\b|```",
     "steps to reproduce":r"steps to reproduce|to reproduce|repro(?:duction)? steps|how to reproduce",
     "version/platform":r"\bversion\b|\bos\b|windows|linux|macos|android"}
for k,p in art.items(): bugs[k]=body.str.contains(p,case=False,regex=True)
bugs["days"]=(pd.to_datetime(bugs.closed_at,utc=True)-pd.to_datetime(bugs.created_at,utc=True)).dt.total_seconds()/86400
print("artefacts in bug report bodies: share | median days to close with vs without (closed only)")
cl=bugs[bugs.state=="CLOSED"]
for k in art: print(f"  {k:20s} {100*bugs[k].mean():5.1f}% | {cl[cl[k]].days.median():6.1f} vs {cl[~cl[k]].days.median():6.1f}")
print("empty body:", f"{100*(body.str.strip()=='').mean():.1f}%")
