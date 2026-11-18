"""Definitions shared by the analysis scripts (bug labels, bots, asset extensions, project filter).

Every rule here is a measurement decision that the report must state explicitly.
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
DUP_FILE = os.path.join(HERE, "..", "data", "duplicated_repos_v1.txt")


def duplicated_projects():
    """The 20 repositories the authors removed to go from 970 to 950 (lower-cased owner/repo)."""
    with open(DUP_FILE, encoding="utf-8") as f:
        return {l.strip().lower() for l in f if l.strip() and not l.startswith("#")}


# ---------------------------------------------------------------- bug labels
def _tokens(label):
    """lower-case, drop emoji/punctuation, split into word tokens: 'Type: Bug 🐛' -> ['type', 'bug']"""
    return re.findall(r"[a-z0-9]+", label.lower())


BUG_TOKENS = {"bug", "bugs", "bugfix", "defect", "crash", "crashes", "regression"}
BUG_PHRASES = {"error report"}
# labels that contain a bug word but describe a verdict/outcome or something else
NOT_BUG_PATTERNS = [r"\bnot\s*a?\s*bug\b", r"\bno\s*bug\b", r"\bbugzilla\b", r"\bfeature\b"]


def is_bug_label(label):
    l = label.lower()
    if any(re.search(p, l) for p in NOT_BUG_PATTERNS):
        return False
    toks = _tokens(l)
    return bool(BUG_TOKENS.intersection(toks)) or " ".join(toks) in BUG_PHRASES


# labels that mark an issue closed without a fix (used to exclude, since state_reason is missing)
NOFIX_PATTERNS = [r"duplicate", r"won'?t\s*-?\s*fix", r"wont\s*-?\s*fix", r"\binvalid\b",
                  r"not\s*a?\s*bug", r"can'?t\s*reproduce", r"cannot\s*reproduce", r"\bwork(s)?\s*as\s*intended\b",
                  r"by\s*design", r"not\s*planned", r"\bstale\b", r"\bobsolete\b", r"\bspam\b"]


def is_nofix_label(label):
    l = label.lower()
    return any(re.search(p, l) for p in NOFIX_PATTERNS)


TITLE_BUG_RE = re.compile(r"\b(?:bug|bugs|crash\w*|error|exception|broken|glitch\w*|freez\w*|"
                          r"not working|doesn'?t work|does not work|fail\w*)\b", re.I)

# ---------------------------------------------------------------- bots
BOT_NAMES = {"dependabot", "dependabot-preview", "github-actions", "renovate", "renovate-bot", "codecov",
             "codecov-io", "coveralls", "stale", "allcontributors", "imgbot", "weblate", "crowdin-bot",
             "transifex-integration", "netlify", "vercel", "sonarcloud", "deepsource-autofix", "pull",
             "pre-commit-ci", "greenkeeper", "snyk-bot", "mergify", "copilot", "lgtm-com", "gitter-badger",
             "welcome", "issue-label-bot", "github-advanced-security", "codefactor-io", "sourcery-ai",
             "coderabbitai", "ghost"}


def is_bot(login):
    if not isinstance(login, str):
        return False
    l = login.lower().strip()
    return l.endswith("[bot]") or l in BOT_NAMES or bool(re.search(r"(^|[-_])bot$", l))


# ---------------------------------------------------------------- asset files
ASSET_CORE = {  # unambiguous non-code media
    "image": {"png", "jpg", "jpeg", "gif", "bmp", "tga", "psd", "svg", "webp", "dds", "ktx", "ktx2", "exr",
              "hdr", "ico", "tif", "tiff", "xcf", "kra", "ase", "aseprite", "pcx", "icns"},
    "audio": {"ogg", "wav", "mp3", "flac", "opus", "aiff", "aif", "mid", "midi", "xm", "mod", "it", "s3m",
              "wma", "m4a", "bank", "fsb"},
    "model": {"fbx", "obj", "blend", "gltf", "glb", "dae", "3ds", "max", "ma", "mb", "stl", "ply", "md2",
              "md3", "md5mesh", "md5anim", "iqm", "b3d", "x3d", "vox"},
    "font": {"ttf", "otf", "fnt", "woff", "woff2", "bdf", "pcf"},
    "video": {"mp4", "webm", "avi", "mov", "ogv", "mkv", "bik", "flv"},
}
ASSET_AMBIGUOUS = {  # engine data / content files that may be authored by either designers or programmers
    "scene": {"tscn", "tres", "scn", "res", "unity", "prefab", "asset", "mat", "anim", "controller",
              "overridecontroller", "physicmaterial", "uasset", "umap", "spriteatlas", "shadergraph"},
    "level": {"tmx", "tsx", "ldtk", "map", "bsp", "vmf", "lvl", "level"},
    "meta": {"meta", "import"},
    "translation": {"po", "pot", "mo", "ts", "resx", "xliff", "xlf"},
}
CORE_EXT = set().union(*ASSET_CORE.values())
AMBIG_EXT = set().union(*ASSET_AMBIGUOUS.values()) - {"ts"}  # .ts is mostly TypeScript; listed for the record
EXT_CLASS = {e: c for c, s in {**ASSET_CORE, **ASSET_AMBIGUOUS}.items() for e in s}


def ext_of(path):
    base = path.rsplit("/", 1)[-1]
    return base.rsplit(".", 1)[-1].lower() if "." in base else ""
