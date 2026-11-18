"""Keyword rules for the primary bug symptom (codebook v1-2026-11-13, section 1).

Developed on the 100 development issues of validation/samples_game_v3 only.
The title is checked first; if no rule fires on the title, the cleaned body
(issue templates, URLs, code blocks and quoted logs removed) is checked; in the
body, save_load only fires on explicit save/load failures because attached saves
are reproduction material. Within one text, the first category in PRIORITY
that matches wins. With no match, the fallback category is returned.
"""
import re

PRIORITY = ["crash_hang", "save_load", "performance", "network", "audio", "visual", "ui", "tooling_other"]

WORDS = {
    "crash_hang": r"crash\w*|segfault|segmentation fault|freez\w*|\bhangs?\b|\bhung\b|not responding|stops? responding|"
                  r"\bpanic\w*|\babort(?:s|ed)?\b|assert(?:ion)? fail\w*|deadlock|fails? to (?:start|launch|load|run)|"
                  r"won'?t (?:start|launch)|\bctd\b|вылет|краш|падени",
    "save_load": r"\bsave ?(?:file|game|crystal)s?\b|savegame|\b(?:can'?t|cannot|won'?t|unable to|fails? to) (?:save|load)\b|"
                 r"\bload(?:ing)? (?:a |the |old |my )?saves?\b|\bsaves? (?:are |is )?(?:broken|corrupt\w*)|"
                 r"serializ\w*|deserializ\w*",
    "performance": r"\bfps\b|frame ?rate|\blag(?:gy|s)?\b|stutter\w*|performance|slow(?:down|s| down)?\b|memory leak|"
                   r"high cpu|takes? (?:too )?long",
    "network": r"desync\w*|disconnect\w*|\bnetwork\w*|netcode|connection|multiplayer|\bping\b|latency",
    "audio": r"\bsounds?\b|\baudio\b|\bmusic\b|\bsfx\b|\bvolume\b|\bmute\w*",
    "visual": r"render\w*|graphic\w*|textur\w*|sprite\w*|shader\w*|animat\w*|flicker\w*|\bcamera\b|shadow\w*|"
              r"\bglow\w*|lighting|polygon\w*|\bdrawn\b|\bdraws?\b|\bvisual\w*|transparen\w*|\bmodel\b|glitch\w*|"
              r"see (?:in|through|thru)|z-?index|particle\w*|effect (?:is )?display\w*|эффект",
    "ui": r"\bmenus?\b|\bbuttons?\b|\bdialog\w*|\bwindow\b|\bhud\b|tooltip\w*|\btext\b|translat\w*|locali[sz]\w*|"
          r"\blocale\b|\btypo\b|\blabels?\b|\bfonts?\b|popup|pop-up|\bicons?\b|minimap|\bpanel\b|"
          r"\btracker\b|overlay\w*|\bscreen\b|\bdisplay\w*|\bshow(?:s|n|ing)?\b|\bclick\w*|\bscroll\w*|"
          r"\barrows?\b|\bgraph\b|\bchart\b|\bui\b|\bgui\b|keyboard|crosshair|blacklist|notes?\b",
    "tooling_other": r"\beditor\b|\bbuild(?:s|ing)?\b|compil\w*|\binstall\w*|ccache|\bci\b|template|"
                     r"(?:link|url) (?:is )?(?:broken|outdated)|broken link|outdated link|\btools?\b|extract\w*|"
                     r"launcher|sanitizer|runtime error:|case sensitive|\brscript\b",
}
RE = {k: re.compile(v, re.I) for k, v in WORDS.items()}
# In bodies, mentions of a save file are usually reproduction material, not the symptom.
BODY_RE = dict(RE, save_load=re.compile(
    r"\b(?:can'?t|cannot|won'?t|unable to|fails? to) (?:save|load)\b|\bsaves? (?:are |is )?(?:broken|corrupt\w*)", re.I))
TEMPLATE = re.compile(
    r"<!--.*?-->|```.*?```|^\s*#{1,6} .*$|^\s*[-*] \[[ xX]\].*$|^\s*>.*$|https?://\S+|!\[[^\]]*\]\([^)]*\)|"
    r"<img[^>]*>|_No response_|^\s*(?:Not needed|None|Not required|No save file needed)\.?\s*$",
    re.S | re.M)


def clean(body):
    return TEMPLATE.sub(" ", body or "")


def first_match(text, rules=RE):
    for cat in PRIORITY:
        if rules[cat].search(text):
            return cat
    return None


def classify(title, body, fallback="gameplay"):
    """Return (category, source) where source is 'title', 'body' or 'fallback'."""
    hit = first_match(title or "")
    if hit:
        return hit, "title"
    text = clean(body)[:2000]
    hit = first_match(text, BODY_RE)
    if hit:
        return hit, "body"
    return fallback, "fallback"
