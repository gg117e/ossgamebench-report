"""Pilot statistics used to decide which research questions are feasible (HANDOFF.md section 4.2).

Usage:
    python -I scripts/03_pilot_stats.py <raw_dir> <interim_dir> > results/pilot_stats.txt

Scope: the 950 projects of the paper (970 in the archive minus data/duplicated_repos_v1.txt).
Joins use the lower-cased project name because the tables differ in letter case.
"""
import collections, os, re, sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (duplicated_projects, is_bug_label, is_nofix_label, is_bot, TITLE_BUG_RE,
                    CORE_EXT, AMBIG_EXT, EXT_CLASS, ext_of)

pd.set_option("display.width", 200)


def q(s, ps=(0, 25, 50, 75, 90, 100)):
    s = pd.Series(s).dropna()
    return "n=%d " % len(s) + " ".join(f"p{p}={np.percentile(s, p):.1f}" for p in ps) + f" mean={s.mean():.2f}"


def hdr(t):
    print("\n" + "=" * 90 + "\n" + t + "\n" + "=" * 90)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    raw_dir, interim_dir = sys.argv[1], sys.argv[2]
    T = os.path.join(raw_dir, "tables")
    dups = duplicated_projects()

    def load(name, cols):
        df = pd.read_parquet(os.path.join(T, name + ".parquet"), columns=cols)
        df["pk"] = df["project"].str.lower()
        return df[~df["pk"].isin(dups)].copy()

    iss = load("issue", ["project", "number", "contributor", "title", "labels", "state", "created_at", "closed_at"])
    ic = load("issue_comment", ["project", "issue_number", "contributor"])
    pr = load("pr", ["project", "number", "contributor", "state", "created_at", "closed_at", "merged_at"])
    pc = load("pr_comment", ["project", "pr_number", "contributor"])
    ipr = load("issue_pr", ["project", "issue_number", "pr_number"])
    prc = load("pr_commit", ["project", "pr_number", "commit_sha"])
    proj = load("project", ["project", "is_fork", "topics", "languages"])
    cm = pd.read_parquet(os.path.join(interim_dir, "commits_slim.parquet"),
                         columns=["project_key", "sha", "contributor", "contributor_email", "created_at", "files"])
    cm = cm[~cm.project_key.isin(dups)]

    hdr("0. Scope")
    print(f"projects {len(proj)}; with issues {iss.pk.nunique()}; issues {len(iss):,}; PRs {len(pr):,}; "
          f"commits {len(cm):,} (projects {cm.project_key.nunique()})")
    print("commit time range (UTC):", cm.created_at.min(), "->", cm.created_at.max())
    per_proj_commits = cm.groupby("project_key").size()
    print("commits per project:", q(per_proj_commits))
    print("projects with <10 commits (selection required >10):", per_proj_commits[per_proj_commits < 10].to_dict())

    # ------------------------------------------------------------------ #2 bug identification
    hdr("#2 Bug identification by labels")
    all_labels = collections.Counter(l for ls in iss.labels for l in ls)
    bug_labels = {l for l in all_labels if is_bug_label(l)}
    nofix_labels = {l for l in all_labels if is_nofix_label(l)}
    iss["is_bug"] = iss.labels.map(lambda ls: any(l in bug_labels for l in ls))
    iss["exact_bug"] = iss.labels.map(lambda ls: any(l.lower() == "bug" for l in ls))
    iss["nofix"] = iss.labels.map(lambda ls: any(l in nofix_labels for l in ls))
    iss["has_label"] = iss.labels.map(len) > 0
    iss["title_bug"] = iss.title.fillna("").str.contains(TITLE_BUG_RE)
    print(f"distinct labels {len(all_labels)}; matched as bug {len(bug_labels)}; as no-fix {len(nofix_labels)}")
    print("top bug labels:", sorted(((all_labels[l], l) for l in bug_labels), reverse=True)[:25])
    print("top no-fix labels:", sorted(((all_labels[l], l) for l in nofix_labels), reverse=True)[:15])
    print(f"issues with exact label 'bug' (case-insensitive): {iss.exact_bug.sum():,}")
    print(f"issues with any bug label (normalised): {iss.is_bug.sum():,} ({100*iss.is_bug.mean():.1f}%)")
    print(f"  of which also carry a no-fix label: {(iss.is_bug & iss.nofix).sum():,}")
    lab_proj = iss.groupby("pk").agg(labelled=("has_label", "mean"), bugs=("is_bug", "sum"), n=("number", "size"))
    uses_bug = lab_proj.bugs > 0
    print(f"projects using a bug label at least once: {uses_bug.sum()} / {len(lab_proj)}")
    print(f"projects labelling <5% of issues: {(lab_proj.labelled < 0.05).sum()}")
    print(f"issues in projects that never use a bug label: {lab_proj.loc[~uses_bug, 'n'].sum():,}")
    print(f"title keyword match: all issues {100*iss.title_bug.mean():.1f}%, "
          f"bug-labelled {100*iss[iss.is_bug].title_bug.mean():.1f}%, "
          f"labelled non-bug {100*iss[iss.has_label & ~iss.is_bug].title_bug.mean():.1f}%, "
          f"unlabelled {100*iss[~iss.has_label].title_bug.mean():.1f}%")

    bugs = iss[iss.is_bug & ~iss.nofix].copy()
    print(f"ANALYSIS SET (bug label, no no-fix label): {len(bugs):,} issues in {bugs.pk.nunique()} projects")

    # ------------------------------------------------------------------ #5 time to close
    hdr("#5 Time to close (bug issues)")
    bugs["created"] = pd.to_datetime(bugs.created_at, utc=True)
    bugs["closed"] = pd.to_datetime(bugs.closed_at, utc=True)
    bugs["days"] = (bugs.closed - bugs.created).dt.total_seconds() / 86400
    print("state:", bugs.state.value_counts().to_dict(), f"open share {100*(bugs.state=='OPEN').mean():.1f}%")
    print("days to close (closed only):", q(bugs.days, (0, 10, 25, 50, 75, 90, 99, 100)))
    print(f"closed within 1 hour: {100*(bugs.days < 1/24).mean():.1f}% of all bug issues; "
          f"negative durations: {(bugs.days < 0).sum()}")
    cutoff = pd.to_datetime(iss.created_at, utc=True).max()  # latest issue creation = proxy for collection time
    print(f"age of open bug issues at {cutoff} (days):", q((cutoff - bugs[bugs.state == "OPEN"].created).dt.days))

    # ------------------------------------------------------------------ #6 participants
    hdr("#6 Comment participants (bug issues)")
    icb = ic.merge(bugs[["pk", "number", "contributor"]].rename(columns={"number": "issue_number", "contributor": "reporter"}),
                   on=["pk", "issue_number"])
    icb["bot"] = icb.contributor.map(is_bot)
    print(f"comments on bug issues {len(icb):,}; by bots {icb.bot.sum():,} ({100*icb.bot.mean():.1f}%); "
          f"missing author {icb.contributor.isna().sum():,}")
    print("top bot authors:", icb[icb.bot].contributor.value_counts().head(15).to_dict())
    top_authors = icb.contributor.value_counts().head(30)
    print("top comment authors (check for unflagged bots):", top_authors.to_dict())
    human = icb[~icb.bot & icb.contributor.notna() & (icb.contributor != icb.reporter)]
    part = human.groupby(["pk", "issue_number"]).contributor.nunique()
    bugs = bugs.merge(part.rename("participants"), left_on=["pk", "number"], right_index=True, how="left")
    bugs["participants"] = bugs.participants.fillna(0).astype(int)
    print("participants (excl. reporter & bots):", q(bugs.participants))
    print("distribution:", bugs.participants.clip(upper=6).value_counts().sort_index().to_dict(), "(6 = 6+)")
    cl = bugs[bugs.state == "CLOSED"]
    print("Spearman participants vs days (closed, pooled, descriptive only): %.3f" %
          cl.participants.corr(cl.days, method="spearman"))

    # ------------------------------------------------------------------ #3 links
    hdr("#3 Issue -> PR -> commit links (bug issues)")
    print(f"issue_pr rows {len(ipr):,}; issues linked {ipr.groupby(['pk','issue_number']).ngroups:,}")
    lk = bugs[["pk", "number", "state"]].merge(ipr.rename(columns={"issue_number": "number"}), on=["pk", "number"])
    lk = lk.merge(pr.rename(columns={"number": "pr_number", "state": "pr_state", "contributor": "pr_author"})
                  [["pk", "pr_number", "pr_state", "pr_author", "merged_at"]], on=["pk", "pr_number"], how="left")
    n_bug = len(bugs)
    linked = lk.groupby(["pk", "number"])
    print(f"bug issues with >=1 linked PR: {linked.ngroups:,} ({100*linked.ngroups/n_bug:.1f}%)")
    print(f"linked PR missing from pr table: {lk.pr_state.isna().sum():,} of {len(lk):,} links")
    merged = lk[lk.pr_state == "MERGED"]
    print(f"bug issues with >=1 merged linked PR: {merged.groupby(['pk','number']).ngroups:,}")
    print("linked PRs per bug issue:", q(linked.size()))
    print("state of bug issues that have a merged PR:", bugs.merge(merged[['pk','number']].drop_duplicates(),
          on=['pk','number']).state.value_counts().to_dict())
    print("pr_commit sha format ok:", prc.commit_sha.str.fullmatch(r"[0-9a-f]{40}").mean())
    mc = merged[["pk", "number", "pr_number"]].merge(prc.rename(columns={"commit_sha": "sha"}), on=["pk", "pr_number"])
    print(f"merged linked PRs with commits in pr_commit: {mc.groupby(['pk','pr_number']).ngroups:,} "
          f"of {merged.groupby(['pk','pr_number']).ngroups:,}")
    mcf = mc.merge(cm.rename(columns={"project_key": "pk"}), on=["pk", "sha"], how="left")
    found = mcf.files.notna()
    print(f"PR commits found in commit table: {found.sum():,} of {len(mcf):,} ({100*found.mean():.1f}%)")
    fix_issue = mcf[found].groupby(["pk", "number"])
    print(f"bug issues whose fix commits (files) are available: {fix_issue.ngroups:,} "
          f"in {mcf[found].pk.nunique()} projects")

    # ------------------------------------------------------------------ #4 assets in fixes
    hdr("#4 Asset files in fixes")
    ex = mcf[found][["pk", "number", "sha", "contributor", "contributor_email", "files"]].explode("files").dropna(subset=["files"])
    ex["ext"] = ex.files.map(ext_of)
    ex["core"] = ex.ext.isin(CORE_EXT)
    ex["ambig"] = ex.ext.isin(AMBIG_EXT)
    per_issue = ex.groupby(["pk", "number"]).agg(core=("core", "any"), ambig=("ambig", "any"), nfiles=("files", "nunique"))
    print(f"fixed bug issues: {len(per_issue):,}; with core asset file: {per_issue.core.sum():,} "
          f"({100*per_issue.core.mean():.1f}%); with core-or-ambiguous: {(per_issue.core|per_issue.ambig).sum():,}")
    print(f"projects contributing core-asset fixes: {per_issue[per_issue.core].reset_index().pk.nunique()}")
    print("fix size (distinct files):", q(per_issue.nfiles))
    print("asset classes among files in fixes:", ex.ext.map(EXT_CLASS).value_counts().to_dict())
    print("top extensions in fixes:", ex.ext.value_counts().head(30).to_dict())
    top_share = per_issue[per_issue.core].reset_index().pk.value_counts(normalize=True).head(5)
    print("projects with most core-asset fixes (share):", top_share.round(3).to_dict())
    # review volume for the linked merged PRs
    pcn = pc[~pc.contributor.map(is_bot)].groupby(["pk", "pr_number"]).size().rename("pr_comments")
    mp = merged[["pk", "number", "pr_number"]].merge(pcn, left_on=["pk", "pr_number"], right_index=True, how="left").fillna({"pr_comments": 0})
    print("non-bot comments per merged linked PR:", q(mp.pr_comments))
    # fix authors
    fa = mcf[found].groupby(["pk", "number"]).contributor_email.nunique()
    print("distinct commit authors (by e-mail) per fix:", q(fa), fa.clip(upper=4).value_counts().sort_index().to_dict())

    # ------------------------------------------------------------------ #3b alternative link paths
    hdr("#3b Alternative ways to find fix commits")
    # Path A (above): commits listed in pr_commit that exist in the cloned history. PRs merged by
    # squash/rebase leave no such commits, so path B looks for the squash/merge commit itself:
    # GitHub's default messages are 'Title (#N)' (squash) and 'Merge pull request #N from ...' (merge).
    # Path C: commits whose message says 'fixes/closes/resolves #N' for a bug issue (no PR needed).
    pat = r"\(#(\d+)\)|Merge pull request #(\d+)"
    refs = cm[["project_key", "sha"]].copy()
    msgs = pd.read_parquet(os.path.join(interim_dir, "commits_slim.parquet"), columns=["project_key", "message"])
    msgs = msgs[~msgs.project_key.isin(dups)]
    refs["message"] = msgs.message.fillna("").values
    ext_ = refs.message.str.extractall(pat)
    ext_["pr_number"] = ext_[0].fillna(ext_[1]).astype(int)
    pb = refs[["project_key", "sha"]].join(ext_["pr_number"].droplevel(1), how="inner").rename(columns={"project_key": "pk"})
    b = merged[["pk", "number", "pr_number"]].merge(pb, on=["pk", "pr_number"])
    a_prs = set(map(tuple, mcf[found][["pk", "pr_number"]].drop_duplicates().values))
    b_prs = set(map(tuple, b[["pk", "pr_number"]].drop_duplicates().values))
    n_m = merged.groupby(["pk", "pr_number"]).ngroups
    print(f"merged linked PRs {n_m:,}: path A {len(a_prs):,}; path B {len(b_prs):,}; "
          f"A or B {len(a_prs | b_prs):,} ({100*len(a_prs | b_prs)/n_m:.1f}%)")
    kw = r"\b(?:fix(?:e[sd])?|close[sd]?|resolve[sd]?)\s*:?\s+#(\d+)"
    ec = refs.message.str.extractall(re.compile(kw, re.I))
    pcm = refs[["project_key", "sha"]].join(ec[0].droplevel(1).astype(int).rename("number"), how="inner") \
        .rename(columns={"project_key": "pk"})
    c = bugs[["pk", "number"]].merge(pcm, on=["pk", "number"])
    ia = set(map(tuple, mcf[found][["pk", "number"]].drop_duplicates().values))
    ib = set(map(tuple, b[["pk", "number"]].drop_duplicates().values))
    ic_ = set(map(tuple, c[["pk", "number"]].drop_duplicates().values))
    print(f"bug issues with fix files: A {len(ia):,}; B {len(ib):,}; A|B {len(ia | ib):,}; C {len(ic_):,}; "
          f"A|B|C {len(ia | ib | ic_):,}")
    fab = pd.concat([mcf[found][["pk", "number", "sha"]], b[["pk", "number", "sha"]]]).drop_duplicates()
    fab = fab.merge(cm.rename(columns={"project_key": "pk"})[["pk", "sha", "files"]], on=["pk", "sha"])
    fx = fab[["pk", "number", "files"]].explode("files").dropna(subset=["files"])
    fx["core"] = fx.files.map(ext_of).isin(CORE_EXT)
    fx["ambig"] = fx.files.map(ext_of).isin(AMBIG_EXT)
    pi = fx.groupby(["pk", "number"]).agg(core=("core", "any"), ambig=("ambig", "any"))
    print(f"A|B fixed bug issues {len(pi):,}; with core asset {pi.core.sum():,} ({100*pi.core.mean():.1f}%) in "
          f"{pi[pi.core].reset_index().pk.nunique()} projects; core-or-ambiguous {(pi.core | pi.ambig).sum():,}")
    print("A|B core-asset fixes, top projects (share):",
          pi[pi.core].reset_index().pk.value_counts(normalize=True).head(5).round(3).to_dict())

    # ------------------------------------------------------------------ #7 concentration
    hdr("#7 Concentration across projects")
    bp = bugs.pk.value_counts()
    print("bug issues per project:", q(bp))
    print("share of bug issues in top 1/5/10/20 projects:",
          [round(bp.head(k).sum() / bp.sum(), 3) for k in (1, 5, 10, 20)])
    print("top 10:", bp.head(10).to_dict())
    fp = per_issue.reset_index().pk.value_counts()
    print("fixed-with-files issues: top 1/5/10 share",
          [round(fp.head(k).sum() / fp.sum(), 3) for k in (1, 5, 10)], fp.head(5).to_dict())

    # ------------------------------------------------------------------ #8 asset-centric contributors
    hdr("#8 Asset-centric committers (whole history)")
    ce = cm[["project_key", "contributor_email", "files"]].explode("files").dropna(subset=["files"])
    ce["core"] = ce.files.map(ext_of).isin(CORE_EXT)
    per_person = ce.groupby(["project_key", "contributor_email"]).core.agg(["mean", "size"])
    per_person = per_person[per_person["size"] >= 10]
    for th in (0.6, 0.75, 0.9):
        sel = per_person[per_person["mean"] >= th]
        print(f"committers (>=10 file changes) with >={int(th*100)}% core-asset file changes: {len(sel):,} "
              f"in {sel.reset_index().project_key.nunique()} projects")
    credit = cm[cm.files.map(lambda fs: any(f.rsplit('/', 1)[-1].upper().startswith(("CREDITS", "AUTHORS", "CONTRIBUTORS")) for f in fs))]
    print("projects whose history touches CREDITS/AUTHORS/CONTRIBUTORS files:", credit.project_key.nunique())

    # ------------------------------------------------------------------ #9 game vs tool
    hdr("#9 Games vs tools (from GitHub topics)")
    tp = proj.topics.fillna("").str.lower().str.split(";")
    tool_topics = {"game-engine", "engine", "framework", "game-framework", "library", "tool", "tools", "sdk",
                   "editor", "level-editor", "game-development-tools", "gamedev-tools", "emulator", "mod",
                   "modding", "launcher", "mod-manager", "bot", "discord-bot", "api", "server"}
    proj["toolish"] = tp.map(lambda ts: bool(tool_topics.intersection(ts)))
    print(f"projects with a tool-like topic: {proj.toolish.sum()} / {len(proj)}")
    print("most common topics:", collections.Counter(t for ts in tp for t in ts if t).most_common(30))


if __name__ == "__main__":
    main()
