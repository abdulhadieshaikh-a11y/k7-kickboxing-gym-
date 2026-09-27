#!/usr/bin/env python3
"""
K7 KICKBOXING GYM — static site generator.

Edit content / images here, then run:   python3 _source/build.py
It rewrites the nine .html pages in the site root.
No dependencies beyond Python 3.8+.
"""
import html, json, os
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# SITE SETTINGS
# ---------------------------------------------------------------------------
SITE_URL = ""   # e.g. "https://www.yourdomain.pk" — set before launch (enables canonical, og:url, sitemap)
NAME = "K7 Kickboxing Gym"
PHONE = "0348 2136361"
TEL = "+923482136361"
ADDR_LINES = ["11-C Ittehad Lane 2,", "D.H.A Phase 6,", "Ittehad Commercial Area,", "Phase 6, Defence Housing Authority,", "Karachi, 75500,", "Pakistan"]
ADDR_ONE = "11-C Ittehad Lane 2, D.H.A Phase 6, Ittehad Commercial Area, Phase 6, Defence Housing Authority, Karachi, 75500, Pakistan"
MAP_Q = quote("K7 Kickboxing Gym, 11-C Ittehad Lane 2, Ittehad Commercial Area, DHA Phase 6, Karachi 75500")
DIRECTIONS = "https://www.google.com/maps/dir/?api=1&destination=" + MAP_Q
MAP_EMBED = "https://www.google.com/maps?q=" + MAP_Q + "&output=embed"

# ---------------------------------------------------------------------------
# IMAGES
# Each slot: remote placeholder photo (Unsplash, free licence) + alt text.
# If a remote photo ever fails to load, the browser swaps in the matching
# local file from assets/images/fallback/<slot>.jpg automatically.
# TO USE YOUR OWN PHOTOS: put e.g. assets/images/hero.jpg in the folder and
# change the slot value to "assets/images/hero.jpg", then rebuild.
# ---------------------------------------------------------------------------
U = "https://images.unsplash.com/photo-{}?auto=format&fit=crop&q=75&w={}"
IMAGES = {
    "hero":       ("1549719386-74dfcbf7dbed", "Boxer in gloves under dramatic low light"),
    "intro":      ("1517438322307-e67111335449", "Athlete training with focus in a dark gym"),
    "kickboxing": ("assets/images/kickboxing-card.jpg", "Two people training kickboxing"),
    "kickboxing_card": ("assets/images/kickboxing-card.jpg", "Two people training kickboxing"),
    "mma":        ("1555597673-b21d5c935865", "Mixed martial arts athletes training"),
    "gym":        ("1534438327276-14e5300c3a48", "Strength training floor with free weights"),
    "personal":   ("1571019614242-c5c5dee9f50b", "Coach guiding an athlete through an exercise"),
    "hiit":       ("1601422407692-ec4eeec1d9b3", "High intensity conditioning workout"),
    "aerobics":   ("1518611012118-696072aa579a", "Cardio and aerobics class in motion"),
    "nutrition":  ("1490645935967-10de6ba17061", "Prepared healthy meals for nutrition planning"),
    "private":    ("1605296867304-46d5465a13f1", "One-to-one combat training session"),
    "combat":     ("1517438476312-10d79c077509", "Fighter working the heavy bag"),
    "combat_hero": ("assets/images/combat-hero.jpg", "Combat sports training"),
    "weight":     ("1583454110551-21f2fa2afe61", "Athlete lifting in a strength session"),
    "women":      ("1594381898411-846e7d193883", "Woman training with boxing gloves"),
    "women2":     ("1571019613454-1cb2f99b2d8b", "Woman performing a strength exercise"),
    "youth":      ("assets/images/youth-classes.jpg", "Young athletes in a training class"),
    "kidskick":   ("1555597408-26bc8e548a46", "Young martial arts students in class"),
    "gymnastics": ("assets/images/kids-gymnastics.jpg", "Children doing gymnastics in a group class"),
    "gym2":       ("1540497077202-7c8a3999166f", "Rows of dumbbells on a rack"),
    "gym3":       ("1517836357463-d25dfeac3438", "Athlete mid-lift in a dark gym"),
    "functional": ("1541534741688-6078c6bfb5c5", "Functional training equipment in a gym"),
    "loss":       ("1576678927484-cc907957088c", "Athlete during a demanding cardio session"),
    "gain":       ("1532029837206-abbe2b7620e3", "Barbell loaded for heavy strength training"),
    "manage":     ("1574680096145-d05b474e2155", "Athlete stretching between training sets"),
    "gloves":     ("1614632537190-23e4146777db", "Pair of boxing gloves hanging in the gym"),
    "readytrain": ("assets/images/ready-to-train.jpg", "Training session"),
}

SIZES_W = [640, 1024, 1600, 2200]


def img(key, cls="", sizes="100vw", eager=False, parallax=None, extra=""):
    src, alt = IMAGES[key]
    fb = f"assets/images/fallback/{key}.jpg"
    if src.startswith("assets/") or src.startswith("http"):
        s_main, srcset = src, ""
    else:
        s_main = U.format(src, 1600)
        srcset = ", ".join(f"{U.format(src, w)} {w}w" for w in SIZES_W)
    a = [f'src="{s_main}"']
    if srcset:
        a.append(f'srcset="{srcset}" sizes="{sizes}"')
    a.append(f'alt="{html.escape(alt)}"')
    a.append('width="1600" height="1067"')
    a.append('loading="eager" fetchpriority="high"' if eager else 'loading="lazy"')
    a.append('decoding="async"')
    if cls:
        a.append(f'class="{cls}"')
    if parallax:
        a.append(f'data-parallax="{parallax}"')
    a.append(f'onerror="this.onerror=null;this.removeAttribute(\'srcset\');this.src=\'{fb}\'"')
    if extra:
        a.append(extra)
    return "<img " + " ".join(a) + ">"


def ph(key, cls="", cap="", sizes="(max-width: 900px) 100vw, 50vw", reveal=True, corners=True, eager=False):
    c = "ph" + (" ph--corners" if corners else "") + (" rv-img" if reveal else "") + (" " + cls if cls else "")
    cap_html = f'<figcaption class="ph__cap">{cap}</figcaption>' if cap else ""
    return f'<figure class="{c}">{img(key, sizes=sizes, eager=eager)}{cap_html}</figure>'


def btn(text, href, v="", attrs=""):
    cls = "btn" + (" " + v if v else "")
    return f'<a class="{cls}" href="{href}"{(" " + attrs) if attrs else ""}><span>{text}</span><span class="arr" aria-hidden="true">→</span></a>'


def lines(*parts, tag="h2", cls="h2", extra=""):
    inner = "".join(f"<span><span>{p}</span></span>" for p in parts)
    return f'<{tag} class="{cls} lines"{(" " + extra) if extra else ""}>{inner}</{tag}>'


def tag(text, n=None, cls=""):
    num = f'<span class="tag__n">{n}</span>' if n else ""
    return f'<p class="tag {cls}">{num}<span>{text}</span></p>'


def enquire_href(program=None):
    return "enquire.html" + (f"?program={quote(program)}" if program else "")


# ---------------------------------------------------------------------------
# SERVICES — the fifteen services supplied by the gym. Nothing added.
# ---------------------------------------------------------------------------
CATS = [
    ("combat", "Combat", "Stand-up striking and complete mixed martial arts, taught with a focus on technique and conditioning."),
    ("personal", "Personal Training", "Dedicated attention for people who want coaching built around them."),
    ("fitness", "Fitness", "Strength, cardio and conditioning to build a body that performs."),
    ("kids", "Kids & Youth", "Structured classes that give young people a strong start in movement and sport."),
    ("wellness", "Wellness & Nutrition", "Support for your body-composition goals, in and out of the gym."),
]
SERVICES = [
    # key, name, subline, cat, image, description, detail page
    ("kickboxing", "Kickboxing", "Stand-up striking", "combat", "kickboxing",
     "Punches, kicks, knees and footwork, built on solid fundamentals. A demanding workout and a real skill to learn.", "combat.html"),
    ("mma", "MMA", "Mixed Martial Arts", "combat", "mma",
     "A complete combat sport that joins striking, clinch work and ground fighting into one system of training.", "combat.html"),
    ("private", "Private Lessons", "Dedicated sessions", "personal", "private",
     "Focused sessions for sharpening technique or working on something specific, without the pace of a group class.", "combat.html"),
    ("personal", "Personal Training", "One-to-one coaching", "personal", "personal",
     "Coaching shaped around your goal, your starting point and your schedule, with someone keeping you accountable.", "fitness.html"),
    ("female", "Female-Only Sessions", "Dedicated sessions for women", "personal", "women",
     "Sessions reserved for women who prefer to train in a female-only setting. Same standards, same intensity.", "female-only.html"),
    ("gym", "Gym", "Strength & conditioning", "fitness", "gym",
     "Train strength and conditioning on the gym floor, whether you're building muscle, fitness or both.", "fitness.html"),
    ("hiit", "HIIT", "High Intensity Interval Training", "fitness", "hiit",
     "Short, hard intervals with brief recovery. Efficient conditioning that pushes your heart rate and your limits.", "fitness.html"),
    ("aerobics", "Aerobics", "Cardio classes", "fitness", "aerobics",
     "Rhythm-led cardio to build stamina, coordination and energy.", "fitness.html"),
    ("youth", "Youth Classes", "For young athletes", "kids", "youth",
     "Classes for young people that build fitness, coordination and discipline.", "kids.html"),
    ("kidskick", "Kids Kickboxing", "Striking for kids", "kids", "kidskick",
     "Kickboxing fundamentals for kids, with an emphasis on control, focus and confidence.", "kids.html"),
    ("gymnastics", "Kids Gymnastics", "Movement & balance", "kids", "gymnastics",
     "Balance, flexibility and body control, the building blocks of every sport.", "kids.html"),
    ("nutrition", "Nutrition Consulting", "Eat for your goal", "wellness", "nutrition",
     "Guidance on what and how to eat so your nutrition supports your training rather than working against it.", "fitness.html"),
    ("manage", "Weight Management", "Long-term balance", "wellness", "manage",
     "Reach a healthy weight and stay there, with training and habits you can keep.", "fitness.html"),
    ("loss", "Weight Loss", "Lose fat, keep strength", "wellness", "loss",
     "A structured approach to losing weight that combines training and nutrition.", "fitness.html"),
    ("gain", "Weight Gain", "Build size & strength", "wellness", "gain",
     "Put on healthy weight through strength training and eating to support it.", "fitness.html"),
]
SVC = {s[0]: s for s in SERVICES}
PROGRAM_NAMES = {
    "kickboxing": "Kickboxing", "mma": "MMA — Mixed Martial Arts", "private": "Private Lessons",
    "personal": "Personal Training", "female": "Female-Only Sessions", "gym": "Gym", "hiit": "HIIT — High Intensity Interval Training",
    "aerobics": "Aerobics", "youth": "Youth Classes", "kidskick": "Kids Kickboxing", "gymnastics": "Kids Gymnastics",
    "nutrition": "Nutrition Consulting", "manage": "Weight Management", "loss": "Weight Loss", "gain": "Weight Gain",
}
assert len(SERVICES) == 15

# ---------------------------------------------------------------------------
# PAGE CHROME
# ---------------------------------------------------------------------------
NAV = [("index.html", "Home", "home"), ("about.html", "About", "about"), ("programs.html", "Programs", "programs"),
       ("combat.html", "Combat", "combat"), ("fitness.html", "Fitness", "fitness"), ("kids.html", "Kids", "kids"),
       ("contact.html", "Contact", "contact")]
MENU = NAV[:6] + [("female-only.html", "Female-Only", "female"), ("enquire.html", "Enquire", "enquire"), ("contact.html", "Contact", "contact")]

JSONLD = {
    "@context": "https://schema.org",
    "@type": "ExerciseGym",
    "name": NAME,
    "telephone": TEL,
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "11-C Ittehad Lane 2, Ittehad Commercial Area, D.H.A Phase 6, Defence Housing Authority",
        "addressLocality": "Karachi",
        "postalCode": "75500",
        "addressCountry": "PK",
    },
    "openingHoursSpecification": [{
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
        "opens": "09:00", "closes": "22:00",
    }],
    "hasMap": "https://www.google.com/maps/search/?api=1&query=" + MAP_Q,
    "image": U.format(IMAGES["hero"][0], 1200),
}


def head(page, title, desc, og_img="hero"):
    canonical = ""
    if SITE_URL:
        path = "" if page == "index.html" else page
        canonical = f'<link rel="canonical" href="{SITE_URL}/{path}">\n  <meta property="og:url" content="{SITE_URL}/{path}">'
    ld = dict(JSONLD)
    if SITE_URL:
        ld["url"] = SITE_URL + "/"
    og_src = IMAGES[og_img][0]
    og = og_src if og_src.startswith("http") else (SITE_URL + "/" + og_src if og_src.startswith("assets/") else U.format(og_src, 1200))
    return f"""<!doctype html>
<html lang="en-PK" class="no-js">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{title}</title>
  <meta name="description" content="{html.escape(desc)}">
  <meta name="theme-color" content="#000000">
  <meta name="format-detection" content="telephone=no">
  {canonical}
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{NAME}">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(desc)}">
  <meta property="og:image" content="{og}">
  <meta property="og:locale" content="en_PK">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(title)}">
  <meta name="twitter:description" content="{html.escape(desc)}">
  <meta name="twitter:image" content="{og}">
  <meta name="geo.region" content="PK-SD">
  <meta name="geo.placename" content="Karachi">
  <link rel="icon" href="assets/images/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preconnect" href="https://images.unsplash.com">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@400;500;600;700&display=swap">
  <link rel="stylesheet" href="assets/css/styles.css">
  <script>document.documentElement.className=document.documentElement.className.replace('no-js','js');</script>
  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
"""


def header(active):
    cur = ' aria-current="page"'
    links = "".join(
        f'<li><a href="{h}"{cur if k == active else ""}>{t}</a></li>' for h, t, k in NAV)
    mlinks = "".join(
        f'<li><a href="{h}"{cur if k == active else ""}>{t}<span>{i:02d}</span></a></li>'
        for i, (h, t, k) in enumerate(MENU, 1))
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="hdr" data-hdr>
  <div class="wrap hdr__in">
    <a class="logo" href="index.html" aria-label="{NAME}, home">
      <img class="logo__image" src="assets/images/k7-logo.svg" alt="{NAME}" width="132" height="72">
    </a>
    <nav class="nav" aria-label="Primary"><ul>{links}</ul></nav>
    {btn("Enquire now", "enquire.html", "btn--sm hdr__cta")}
    <button class="burger" type="button" aria-expanded="false" aria-controls="menu" aria-label="Open menu"><span></span><span></span></button>
  </div>
</header>
<div class="menu" id="menu" aria-hidden="true">
  <nav aria-label="Mobile"><ul class="menu__list">{mlinks}</ul></nav>
  <div class="menu__foot">
    <a href="tel:{TEL}">Call {PHONE}</a>
    <span>Mon — Sat, 9:00 AM — 10:00 PM. Sunday closed.</span>
    <span>DHA Phase 6, Karachi</span>
  </div>
</div>
"""


def status(cls=""):
    return f'<p class="status {cls}" data-status role="status" aria-live="polite"><span class="status__dot" aria-hidden="true"></span><span data-status-text>Mon — Sat, 9:00 AM — 10:00 PM</span></p>'


def footer():
    prog = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in [
        ("combat.html", "Kickboxing & MMA"), ("fitness.html", "Fitness"), ("kids.html", "Kids & Youth"),
        ("female-only.html", "Female-Only Sessions"), ("programs.html", "All programs")])
    nav = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in [
        ("index.html", "Home"), ("about.html", "About"), ("programs.html", "Programs"), ("combat.html", "Combat"),
        ("fitness.html", "Fitness"), ("kids.html", "Kids"), ("enquire.html", "Enquire"), ("contact.html", "Contact")])
    return f"""<footer class="ftr">
  <div class="wrap">
    <div class="ftr__top">
      <div class="ftr__lead">
        <figure class="ftr__image" aria-hidden="true"><img src="assets/images/footer-training.jpg" alt="" width="800" height="600" loading="lazy"></figure>
        <a class="ftr__logo" href="index.html" aria-label="{NAME}, home"><img src="assets/images/k7-logo.svg" alt="" width="160" height="88"></a>
        <p>Train with purpose. Train with K7.</p>
        <div class="btn-row">{btn("Enquire now", "enquire.html", "btn--solid")}</div>
      </div>
      <div class="ftr__info">
        <div><h2>Visit</h2><address><strong>{NAME}</strong>11-C Ittehad Lane 2,<br>D.H.A Phase 6,<br>Ittehad Commercial Area,<br>Karachi, Pakistan</address></div>
        <div><h2>Call</h2><a href="tel:{TEL}"><strong>{PHONE}</strong></a></div>
      </div>
      <div class="ftr__info">
        <div><h2>Hours</h2>
          <div class="ftr__hrs"><span>Mon — Sat</span><span>9:00 AM — 10:00 PM</span><span>Sunday</span><span>Closed</span></div>
        </div>
        <div><h2>Programs</h2><ul>{prog}</ul></div>
      </div>
      <div><h2>Navigation</h2><ul>{nav}</ul></div>
    </div>
  </div>
  <div class="wrap" aria-hidden="true"><div class="ftr__big"><span class="ftr__k7">K7</span><span class="ftr__words"><span>Train</span><span>Fight</span><span>Move</span><span>Perform</span></span></div></div>
  <div class="wrap"><div class="ftr__bot"><span>© <span data-year>2026</span> {NAME}</span><span>DHA Phase 6, Karachi, Pakistan</span></div></div>
</footer>
"""


def tail():
    return """<script src="assets/js/main.js" defer></script>
</body>
</html>
"""


def page_hero(crumb, title_parts, lede, img_key, idx=None, actions="", short=False):
    idx_html = f'<span class="phero__idx" aria-hidden="true">{idx}</span>' if idx else ""
    media = "" if short else f'<div class="phero__media">{img(img_key, eager=True, parallax="0.08")}</div>'
    h = "".join(f"<span><span>{p}</span></span>" for p in title_parts)
    return f"""<section class="phero{' phero--short' if short else ''}" aria-labelledby="page-title">
  {media}{idx_html}
  <div class="wrap phero__body">
    <nav class="phero__crumb rv" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><span aria-current="page">{crumb}</span></nav>
    <h1 id="page-title" class="h1 lines">{h}</h1>
    <div class="phero__foot rv rv-d2">
      <p class="lede">{lede}</p>
      <div class="btn-row">{actions}</div>
    </div>
  </div>
</section>"""


def marquee(words=("Train", "Fight", "Move", "Perform", "K7"), light=False):
    items = "".join(
        f'<span class="marquee__item"><span class="{"o" if i % 2 else ""}">{w}</span><span class="marquee__sq"></span></span>'
        for i, w in enumerate(words))
    group = f'<div class="marquee__group">{items}{items}</div>'
    return f'<div class="marquee{" marquee--light" if light else ""}" aria-hidden="true"><div class="marquee__track">{group}{group}</div></div>'


def cta(title=("Ready", "to train?"), body="Tell us what you want to work on and we'll help you find the right program.", img_key="gloves"):
    t = "".join(f"<span><span>{p}</span></span>" for p in title)
    return f"""<section class="cta" aria-labelledby="cta-title">
  <div class="cta__bg">{img(img_key, parallax="0.12")}</div>
  <div class="wrap cta__grid">
    <h2 id="cta-title" class="d cta__t lines">{t}</h2>
    <div class="cta__side rv">
      <p class="muted">{body}</p>
      <div class="btn-row">{btn("Enquire now", "enquire.html", "btn--solid")}{btn("Call " + PHONE, "tel:" + TEL)}</div>
    </div>
  </div>
</section>"""


def hours_block(dark=False, num="07"):
    sec = "sec--coal" if dark else "sec--light"
    btnv = "" if dark else "btn--dark"
    return f"""<section class="sec {sec}" aria-labelledby="hours-title">
  <div class="wrap">
    <div class="shead shead--split">
      {f'<span class="shead__num" aria-hidden="true">{num}</span>' if num else "<span></span>"}
      <div class="shead__body">{tag("Opening hours", cls="tag--plain")}<h2 id="hours-title" class="h2 lines"><span><span>When we train</span></span></h2></div>
      {status()}
    </div>
    <div class="hours">
      <div class="hours__row rv"><p class="hours__day">Monday — Saturday</p><p class="hours__time">09:00 AM — 10:00 PM</p></div>
      <div class="hours__row hours__row--closed rv"><p class="hours__day">Sunday</p><p class="hours__time">Closed</p></div>
    </div>
    <div class="hours__meta rv">
      <p class="muted">11-C Ittehad Lane 2, Ittehad Commercial Area, D.H.A Phase 6, Karachi</p>
      <div class="btn-row">{btn("Get directions", DIRECTIONS, btnv, 'target="_blank" rel="noopener"')}{btn("Call " + PHONE, "tel:" + TEL, btnv)}</div>
    </div>
  </div>
</section>"""


def program_select():
    groups = []
    for ck, cname, _ in CATS:
        opts = "".join(f'<option value="{PROGRAM_NAMES[s[0]]}">{PROGRAM_NAMES[s[0]]}</option>' for s in SERVICES if s[3] == ck)
        groups.append(f'<optgroup label="{cname}">{opts}</optgroup>')
    return '<option value="" disabled selected>Select a program</option>' + "".join(groups) + '<option value="Not sure yet">Not sure yet — help me choose</option>'


def form(kind="enquire"):
    is_contact = kind == "contact"
    prog_field = f"""<div class="field field--full">
          <label for="{kind}-program">Interested program</label>
          <select id="{kind}-program" name="program" {'' if is_contact else 'required'} aria-describedby="{kind}-program-err">{program_select()}</select>
          <p class="field__err" id="{kind}-program-err"></p>
        </div>"""
    return f"""<div data-form-wrap>
  <form class="form" data-enquiry="{kind}" novalidate>
    <div class="form-alert" role="alert"></div>
    <div class="form__grid">
      <div class="field">
        <label for="{kind}-name">Name</label>
        <input id="{kind}-name" name="name" type="text" autocomplete="name" required aria-describedby="{kind}-name-err" placeholder="Your full name">
        <p class="field__err" id="{kind}-name-err"></p>
      </div>
      <div class="field">
        <label for="{kind}-phone">Phone</label>
        <input id="{kind}-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" required aria-describedby="{kind}-phone-err" placeholder="03XX XXXXXXX">
        <p class="field__err" id="{kind}-phone-err"></p>
      </div>
      <div class="field field--full">
        <label for="{kind}-email">Email <em>(optional)</em></label>
        <input id="{kind}-email" name="email" type="email" autocomplete="email" aria-describedby="{kind}-email-err" placeholder="name@example.com">
        <p class="field__err" id="{kind}-email-err"></p>
      </div>
      {prog_field}
      <div class="field field--full">
        <label for="{kind}-message">Message {'' if is_contact else '<em>(optional)</em>'}</label>
        <textarea id="{kind}-message" name="message" rows="4" {'required' if is_contact else ''} aria-describedby="{kind}-message-err" placeholder="Your goals, experience or any questions"></textarea>
        <p class="field__err" id="{kind}-message-err"></p>
      </div>
      <div class="sr-only" aria-hidden="true"><label for="{kind}-company">Company</label><input id="{kind}-company" name="company" type="text" tabindex="-1" autocomplete="off"></div>
    </div>
    <div class="form__foot">
      <p class="form__note">We use your details only to reply to this enquiry.</p>
      <button class="btn btn--solid" type="submit"><span class="lbl">{'Send message' if is_contact else 'Send enquiry'}</span><span class="spin" aria-hidden="true"></span><span class="arr" aria-hidden="true">→</span></button>
    </div>
  </form>
  <div class="fstate fstate--ok" role="status" aria-live="polite">
    <p class="fstate__t" data-ready>Your enquiry is ready.</p>
    <p class="fstate__t" data-sent>Enquiry sent.</p>
    <p class="muted" data-ready>Send it to us on WhatsApp with one tap, or call us directly during opening hours.</p>
    <p class="muted" data-sent>Thanks for reaching out. We'll get back to you on the number you gave us. For anything urgent, call {PHONE}.</p>
    <div class="btn-row"><a class="btn btn--solid" data-ready data-wa href="https://wa.me/923482136361" target="_blank" rel="noopener"><span>Send on WhatsApp</span><span class="arr" aria-hidden="true">→</span></a>{btn("Call " + PHONE, "tel:" + TEL)}</div>
    <button class="link" type="button" data-form-back>Edit enquiry</button>
  </div>
  <div class="fstate fstate--err" role="alert">
    <p class="fstate__t">Your enquiry didn't go through.</p>
    <p class="muted">The connection failed before we received it. Try again, or send the same message on WhatsApp or call {PHONE}.</p>
    <div class="btn-row"><button class="btn btn--solid" type="button" data-form-back><span>Try again</span><span class="arr" aria-hidden="true">→</span></button><a class="btn" data-wa href="https://wa.me/923482136361" target="_blank" rel="noopener"><span>Send on WhatsApp</span><span class="arr" aria-hidden="true">→</span></a></div>
  </div>
</div>"""


# ---------------------------------------------------------------------------
# PAGES
# ---------------------------------------------------------------------------
def home():
    tiles = [
        ("kickboxing", "stile--a", "combat.html"), ("mma", "stile--b", "combat.html"),
        ("gym", "stile--c", "fitness.html"), ("personal", "stile--c", "fitness.html"), ("hiit", "stile--c", "fitness.html"),
        ("aerobics", "stile--d", "fitness.html"), ("nutrition", "stile--c", "fitness.html"), ("private", "stile--e", "combat.html"),
    ]
    short = {
        "kickboxing": "Punches, kicks, knees and footwork. Stand-up striking built from the fundamentals up.",
        "mma": "Striking, clinch and ground work combined into one complete martial art.",
        "gym": "Strength and conditioning for every level.",
        "personal": "One-to-one coaching built around your goal and your pace.",
        "hiit": "Short, hard intervals for serious conditioning.",
        "aerobics": "Rhythm-led cardio to build stamina and energy.",
        "nutrition": "Eating guidance that supports your training.",
        "private": "Dedicated sessions for focused technical work.",
    }
    sgrid = ""
    for k, cls, href in tiles:
        s = SVC[k]
        name = "MMA" if k == "mma" else s[1]
        image_key = "kickboxing_card" if k == "kickboxing" else s[4]
        sgrid += f"""<a class="stile {cls} rv" href="{href}">
        {img(image_key, sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 45vw")}
        <span class="stile__arr" aria-hidden="true">→</span>
        <span class="stile__body">
          <span class="stile__k">{s[2]}</span>
          <span class="stile__t">{name}</span>
          <span class="stile__d"><span>{short[k]}</span></span>
        </span>
      </a>"""

    fit_keys = [("gym", "Strength & conditioning"), ("personal", "One-to-one"), ("hiit", "Intervals"), ("aerobics", "Cardio"),
                ("manage", "Long-term balance"), ("loss", "Lose fat"), ("gain", "Build size"), ("nutrition", "Eat for your goal")]
    rows = "".join(f"""<a class="ilist__row" href="fitness.html#{k}" data-prev="{k}">
          <span class="ilist__t">{SVC[k][1]}</span><span class="ilist__k">{kk}</span><span class="ilist__a" aria-hidden="true">→</span></a>""" for k, kk in fit_keys)
    prev_imgs = "".join(img(SVC[k][4], sizes="300px", extra=f'data-k="{k}"') for k, _ in fit_keys)

    kids = ""
    for k in ["youth", "kidskick", "gymnastics"]:
        s = SVC[k]
        kids += f"""<article class="trio__item rv">
        {ph(s[4], sizes="(max-width: 860px) 100vw, 33vw")}
        <div class="trio__meta"><h3 class="h4">{s[1]}</h3><span class="tag tag--plain muted">{s[2]}</span></div>
        <p class="body">{s[5]}</p>
      </article>"""

    return head("index.html", "K7 Kickboxing Gym | Kickboxing, MMA & Fitness in DHA Phase 6, Karachi",
                "K7 Kickboxing Gym in Ittehad Commercial Area, DHA Phase 6, Karachi. Kickboxing, MMA, gym, personal training, HIIT, kids classes and female-only sessions. Open Mon–Sat, 9 AM–10 PM.") + header("home") + f"""
<main id="main">
<section class="hero" aria-labelledby="hero-title">
  <div class="hero__media">{img("hero", eager=True, sizes="100vw")}</div>
  <span class="hero__k7" aria-hidden="true">K7</span>
  <div class="ropes" aria-hidden="true"><i></i><i></i><i></i></div>
  <div class="wrap hero__top">
    <p class="tag tag--plain ld">Karachi, DHA Phase 6</p>
    <div class="ld">{status()}</div>
  </div>
  <div class="wrap hero__main">
    <div class="hero__brand ld"><b>K7 Kickboxing Gym</b><i aria-hidden="true"></i></div>
    <h1 id="hero-title" class="d lines"><span class="sr-only">K7 Kickboxing Gym: </span><span><span>Built for</span></span><span><span>the fight.</span></span></h1>
    <div class="hero__row">
      <p class="lede ld ld-2">Kickboxing, MMA and complete fitness training in Ittehad Commercial Area. One gym for the fighter, the athlete, and anyone ready to start.</p>
      <div class="btn-row ld ld-3">{btn("Explore programs", "programs.html", "btn--solid")}{btn("Enquire now", "enquire.html")}</div>
    </div>
  </div>
  <div class="hero__bar ld ld-4">
    <div class="wrap">
      <span>Mon — Sat / 09:00 — 22:00</span>
      <a href="tel:{TEL}">{PHONE}</a>
      <span class="hide-sm">Sunday closed</span>
      <a class="scroll-cue" href="#intro"><span>Scroll</span><span class="scroll-cue__line" aria-hidden="true"></span></a>
    </div>
  </div>
</section>

{marquee()}

<section class="sec sec--light" id="intro" aria-labelledby="intro-title">
  <div class="wrap intro">
    <div class="intro__text">
      {tag("Introduction", "01")}
      {lines("Discipline", "starts here.", cls="h2", extra='id="intro-title"')}
      <p class="lede rv">K7 Kickboxing Gym brings combat sports and fitness under one roof in DHA Phase 6, Karachi.</p>
      <p class="body rv">Whether you want to learn to strike, get stronger, lose weight or simply move better, the approach is the same: show up, put in the work, and keep improving. Every program here is built for people who take their training seriously, at any level.</p>
      <ul class="pillars rv" aria-label="What K7 is about"><li>Fitness</li><li>Combat sports</li><li>Training</li><li>Performance</li><li>Personal development</li></ul>
      <div class="btn-row rv">{btn("About K7", "about.html", "btn--dark")}</div>
    </div>
    {ph("intro", "intro__media")}
  </div>
</section>

<section class="sec sec--dark" aria-labelledby="svc-title">
  <div class="wrap">
    <div class="shead shead--split">
      <span class="shead__num" aria-hidden="true">02</span>
      <div class="shead__body">{tag("Programs", cls="tag--plain")}{lines("Everything you", "need to train.", extra='id="svc-title"')}</div>
      <div class="rv">{btn("View all programs", "programs.html")}</div>
    </div>
  </div>
  <div class="wrap"><div class="sgrid">{sgrid}</div></div>
</section>

<section class="combat sec" aria-labelledby="combat-title">
  <div class="combat__bg">{img("combat", parallax="0.1")}</div>
  <div class="wrap">
    {tag("Combat sports", "03")}
    <h2 id="combat-title" class="d combat__title lines" style="margin-top:28px"><span><span>Train.</span></span><span><span class="outline">Fight.</span></span><span><span>Evolve.</span></span></h2>
    <div class="combat__grid">
      <div class="stack rv">
        <p class="lede">Combat training is more than hitting hard. It's technique repeated until it becomes instinct, conditioning that holds up in the last round, and the composure to think under pressure.</p>
        <p class="body">Start with the fundamentals of kickboxing, take on the full picture of mixed martial arts, or book private lessons to sharpen one thing at a time.</p>
        <div class="btn-row">{btn("Explore combat training", "combat.html", "btn--solid")}</div>
      </div>
      <div class="fcard rv rv-d1">
        <div class="fcard__head"><span>K7 Combat card</span><span>3 disciplines</span></div>
        <a class="bout" href="combat.html#kickboxing"><span class="bout__n">Bout<b>01</b></span><span class="bout__t">Kickboxing<span class="bout__s">Stand-up striking: hands, feet, knees and footwork.</span></span><span class="bout__a" aria-hidden="true">→</span></a>
        <a class="bout" href="combat.html#mma"><span class="bout__n">Bout<b>02</b></span><span class="bout__t">MMA — Mixed Martial Arts<span class="bout__s">Striking, clinch and ground work in one system.</span></span><span class="bout__a" aria-hidden="true">→</span></a>
        <a class="bout" href="combat.html#private"><span class="bout__n">Bout<b>03</b></span><span class="bout__t">Private Lessons<span class="bout__s">Dedicated sessions, focused on you.</span></span><span class="bout__a" aria-hidden="true">→</span></a>
      </div>
    </div>
  </div>
</section>

<section class="sec sec--paper on-light" aria-labelledby="fit-title">
  <div class="wrap fsplit">
    <div class="fsplit__aside">
      {tag("Fitness", "04")}
      {lines("Stronger in", "every", "direction.", extra='id="fit-title"')}
      <p class="body rv">Build strength, burn fat, gain size or simply get fitter. Pick the training that matches your goal, with coaching and nutrition guidance to back it up.</p>
      <div class="btn-row rv">{btn("Explore fitness", "fitness.html", "btn--dark-solid")}</div>
    </div>
    <div class="ilist" data-hoverlist>{rows}</div>
  </div>
  <div class="hoverprev" aria-hidden="true">{prev_imgs}</div>
</section>

<section class="sec sec--char" aria-labelledby="kids-title">
  <div class="wrap">
    <div class="kids-head">
      <div class="stack">{tag("Kids & youth", "05")}{lines("Start them", "strong.", cls="d d-xl", extra='id="kids-title"')}</div>
      <div class="stack rv">
        <p class="body">Structured classes that build coordination, confidence and discipline. Skills that carry well beyond the gym.</p>
        <div class="btn-row">{btn("Explore kids programs", "kids.html", "btn--solid")}</div>
      </div>
    </div>
    <div class="trio">{kids}</div>
  </div>
</section>

<section class="sec--dark" aria-labelledby="fem-title">
  <div class="feature">
    <div class="feature__media">{ph("women", sizes="(max-width: 900px) 100vw, 50vw")}</div>
    <div class="feature__body">
      {tag("Female-only sessions", "06")}
      {lines("Train on", "your terms.", extra='id="fem-title"')}
      <p class="lede rv">Dedicated sessions for women who want to train in a female-only setting.</p>
      <p class="body rv">Same standards, same intensity, same K7. Get in touch to find out session timings and what's on offer.</p>
      <ul class="feature__vals rv" aria-label="Session values"><li>Focus</li><li>Strength</li><li>Respect</li></ul>
      <div class="btn-row rv">{btn("Enquire about sessions", enquire_href("Female-Only Sessions"), "btn--solid")}{btn("Learn more", "female-only.html")}</div>
    </div>
  </div>
</section>

{hours_block()}

{cta(img_key="readytrain")}
</main>
""" + footer() + tail()


def about():
    fit = ["Gym", "Personal Training", "HIIT", "Aerobics", "Weight Management", "Nutrition Consulting"]
    com = ["Kickboxing", "MMA", "Private Lessons", "Kids Kickboxing", "Youth Classes", "Female-Only Sessions"]
    return head("about.html", "About K7 Kickboxing Gym | Combat Sports & Fitness in DHA Phase 6, Karachi",
                "K7 Kickboxing Gym is a combat sports and fitness gym in Ittehad Commercial Area, DHA Phase 6, Karachi, built on discipline, technique and consistency.", "intro") + header("about") + f"""
<main id="main">
{page_hero("About", ["More than", "a gym."], "K7 Kickboxing Gym is where combat sports and fitness meet: one address in DHA Phase 6 for anyone who wants to train with purpose.", "intro", "K7", btn("Explore programs", "programs.html", "btn--solid"))}

<section class="sec sec--light" aria-label="Brand statement">
  <div class="wrap manifesto">
    {tag("What we stand for", "01")}
    <h2 class="statement lines"><span><span>K7 is not</span></span><span><span class="o">just a gym.</span></span><span><span>K7 is a combat</span></span><span><span>& fitness brand.</span></span></h2>
    <div class="grid-2">
      <p class="lede rv">We believe the discipline of a fighter can change how anyone trains, whether they ever step into a ring or not.</p>
      <p class="body rv">That's why kickboxing and MMA sit alongside the gym, HIIT, aerobics, personal training and nutrition at K7. Different goals, one standard: turn up, work hard, get better.</p>
    </div>
  </div>
</section>

<section class="sec sec--dark" aria-labelledby="worlds-title">
  <div class="wrap">
    <div class="shead"><span class="shead__num" aria-hidden="true">02</span><div class="shead__body">{tag("Identity", cls="tag--plain")}{lines("Two disciplines.", "One standard.", extra='id="worlds-title"')}</div></div>
    <div class="worlds">
      <div class="world rv"><h3 class="h3">Combat</h3><p class="body">Striking, grappling and the mental edge that comes with them.</p><ul>{"".join(f"<li>{x}</li>" for x in com)}</ul>{btn("Combat training", "combat.html")}</div>
      <div class="world rv rv-d1"><h3 class="h3">Fitness</h3><p class="body">Strength, conditioning and body composition, done properly.</p><ul>{"".join(f"<li>{x}</li>" for x in fit)}</ul>{btn("Fitness training", "fitness.html")}</div>
    </div>
  </div>
</section>

<div class="band" aria-hidden="true"><div class="band__img">{img("gym3", parallax="0.14")}</div>
  <div class="band__txt"><div class="wrap"><p class="statement" style="color:#fff"><span>Technique.</span><span class="o">Conditioning.</span><span>Composure.</span></p></div></div>
</div>

<section class="sec sec--light" aria-labelledby="phil-title">
  <div class="wrap">
    <div class="shead"><span class="shead__num" aria-hidden="true">03</span><div class="shead__body">{tag("Training philosophy", cls="tag--plain")}{lines("How we train", extra='id="phil-title"')}</div></div>
    <div class="princ">
      <div class="princ__row rv"><h3 class="h2">Discipline</h3><p class="body">Progress comes from showing up when it's hard. Every session is a chance to build the habit before the result.</p></div>
      <div class="princ__row rv"><h3 class="h2">Technique</h3><p class="body">Whether it's a jab, a squat or a sprint interval, doing it right matters more than doing it fast. Good form is what makes hard work count.</p></div>
      <div class="princ__row rv"><h3 class="h2">Consistency</h3><p class="body">No single workout changes you. Months of steady, honest training do. We build programs you can keep coming back to.</p></div>
    </div>
  </div>
</section>

<section class="sec sec--coal" aria-labelledby="story-title">
  <div class="wrap grid-2" style="align-items:start">
    <div class="stack">{tag("Our story", "04")}{lines("The K7 story", extra='id="story-title"')}</div>
    <div class="stack">
      <!-- EDIT: replace this slot with the gym's real story. Delete the .slot wrapper when done. -->
      <div class="slot rv" data-slot="Content slot: Our story">
        <p class="h4">Founding story</p>
        <p class="body">Add how and when K7 Kickboxing Gym started, who founded it and what drives the team. Keep it factual and in your own words.</p>
      </div>
      <!-- EDIT: add coach profiles (name, discipline, photo) here when ready. -->
      <div class="slot rv" data-slot="Content slot: Coaches">
        <p class="h4">Coaching team</p>
        <p class="body">Add each coach's name, discipline and photo. Include only verified qualifications.</p>
      </div>
    </div>
  </div>
</section>

{cta(("Come train", "with K7."), "Visit us in Ittehad Commercial Area, DHA Phase 6, or send an enquiry to get started.", "gloves")}
</main>
""" + footer() + tail()


def programs():
    cat_nav = "".join(f'<li><a href="#{ck}"><span>{i:02d}</span>{cn}</a></li>' for i, (ck, cn, _) in enumerate(CATS, 1))
    body = ""
    for i, (ck, cn, cd) in enumerate(CATS, 1):
        rows = ""
        for s in [x for x in SERVICES if x[3] == ck]:
            full = PROGRAM_NAMES[s[0]]
            sub = s[2] if s[0] != "mma" else "Mixed Martial Arts"
            rows += f"""<article class="prow rv" id="svc-{s[0]}">
          {ph(s[4], sizes="(max-width: 900px) 100vw, 340px", reveal=False)}
          <div class="prow__body"><h3 class="prow__t">{s[1]}<small>{sub.upper()}</small></h3><p class="body">{s[5]}</p></div>
          <div class="prow__acts"><a class="link" href="{enquire_href(full)}">Enquire <span class="arr" aria-hidden="true">→</span></a><a class="link" href="{s[6]}#{s[0]}" aria-label="More about {s[1]}">Details <span class="arr" aria-hidden="true">→</span></a></div>
        </article>"""
        body += f"""<section class="cat" id="{ck}" aria-labelledby="cat-{ck}">
    <div class="wrap">
      <div class="cat__head"><span class="cat__num" aria-hidden="true">{i:02d}</span><h2 id="cat-{ck}" class="h2 lines"><span><span>{cn}</span></span></h2><p class="body rv">{cd}</p></div>
      <div>{rows}</div>
    </div>
  </section>"""
    return head("programs.html", "Programs & Services | K7 Kickboxing Gym, DHA Phase 6 Karachi",
                "All fifteen programs at K7 Kickboxing Gym, Karachi: kickboxing, MMA, private lessons, personal training, female-only sessions, gym, HIIT, aerobics, kids and youth classes, nutrition and weight programs.", "gym") + header("programs") + f"""
<main id="main">
{page_hero("Programs", ["Every program.", "One address."], "Fifteen ways to train at K7, from your first kickboxing class to one-to-one coaching and nutrition guidance.", "gym", "15", btn("Enquire now", "enquire.html", "btn--solid"))}
<nav class="catnav" aria-label="Program categories"><div class="wrap"><ul>{cat_nav}</ul></div></nav>
{body}
{cta(("Not sure", "where to start?"), "Tell us your goal and experience and we'll point you to the right program.", "functional")}
</main>
""" + footer() + tail()


def disc(num, key, title_parts, lede, body, points, img_key, rev=False, light=False, program=None, anchor=None):
    t = "".join(f"<span><span>{p}</span></span>" for p in title_parts)
    pts = "".join(f"<li>{p}</li>" for p in points)
    cls = "disc" + (" disc--rev" if rev else "") + (" on-light" if light else "")
    bprim = "btn--dark-solid" if light else "btn--solid"
    return f"""<section class="{cls}" id="{anchor or key}" aria-labelledby="d-{key}">
  <div class="disc__media">{ph(img_key, sizes="(max-width: 960px) 100vw, 55vw", corners=True)}</div>
  <div class="disc__body">
    <span class="disc__n" aria-hidden="true">{num}</span>
    <h2 id="d-{key}" class="h2 lines">{t}</h2>
    <p class="lede rv">{lede}</p>
    <p class="body rv">{body}</p>
    <ul class="disc__list rv">{pts}</ul>
    <div class="btn-row rv">{btn("Enquire about " + (program.split(" —")[0] if program else ""), enquire_href(program), bprim)}</div>
  </div>
</section>"""


def combat():
    return head("combat.html", "Kickboxing & MMA Classes in DHA Phase 6, Karachi | K7 Kickboxing Gym",
                "Kickboxing, MMA and private combat lessons at K7 Kickboxing Gym, Ittehad Commercial Area, DHA Phase 6, Karachi. Open Mon–Sat, 9 AM–10 PM.", "combat") + header("combat") + f"""
<main id="main">
{page_hero("Kickboxing & MMA", ["Earn every", "round."], "Kickboxing, mixed martial arts and private lessons. Serious combat training, built on fundamentals.", "combat_hero", "K7", btn("Enquire now", enquire_href("Kickboxing"), "btn--solid") + btn("Call " + PHONE, "tel:" + TEL))}
{marquee(("Kickboxing", "MMA", "Private lessons", "Train", "Fight", "Evolve"))}
<section class="sec--dark" aria-label="Combat disciplines">
{disc("01", "kickboxing", ["Kickboxing"], "The art of stand-up striking.", SVC["kickboxing"][5] + " Every session builds sharper technique and a stronger engine.", ["Stance & guard", "Footwork", "Punch combinations", "Kicks & knees", "Defence", "Conditioning"], "kickboxing", program="Kickboxing")}
{disc("02", "mma", ["MMA —", "Mixed Martial Arts"], "The complete combat sport.", SVC["mma"][5] + " It asks more of you than any single discipline, and gives more back.", ["Striking", "Clinch work", "Takedowns", "Ground control", "Transitions", "Conditioning"], "mma", rev=True, program="MMA — Mixed Martial Arts")}
{disc("03", "private", ["Private", "Lessons"], "Your session. Your focus.", SVC["private"][5] + " Ask about availability when you enquire.", ["Technique refinement", "Specific goals", "Your pace", "Focused feedback"], "private", program="Private Lessons")}
</section>
<div class="band" aria-hidden="true"><div class="band__img">{img("gloves", parallax="0.14")}</div>
  <div class="band__txt"><div class="wrap"><p class="statement" style="color:#fff"><span>Train.</span><span class="o">Fight.</span><span>Evolve.</span></p></div></div>
</div>
<section class="sec sec--coal" aria-labelledby="fund-title">
  <div class="wrap">
    <div class="shead"><span class="shead__num" aria-hidden="true">04</span><div class="shead__body">{tag("The fundamentals", cls="tag--plain")}{lines("What combat", "training builds", extra='id="fund-title"')}</div></div>
    <ul class="fgrid">
      <li class="rv"><h3 class="h4">Technique</h3><p class="body">Clean mechanics make every strike faster, safer and more effective.</p></li>
      <li class="rv rv-d1"><h3 class="h4">Conditioning</h3><p class="body">Rounds of work build the kind of fitness that's hard to get any other way.</p></li>
      <li class="rv rv-d2"><h3 class="h4">Defence</h3><p class="body">Blocking, slipping and moving are skills, and they're trained just as hard as attack.</p></li>
      <li class="rv"><h3 class="h4">Composure</h3><p class="body">Learning to breathe and think under pressure carries into every part of life.</p></li>
      <li class="rv rv-d1"><h3 class="h4">Confidence</h3><p class="body">Knowing what you can do with your body changes how you carry yourself.</p></li>
      <li class="rv rv-d2"><h3 class="h4">Discipline</h3><p class="body">Progress in combat sports comes one session at a time. There are no shortcuts.</p></li>
    </ul>
  </div>
</section>
{cta(("Step into", "the ring."), "Ask about kickboxing, MMA or private lessons and find the right starting point.", "combat")}
</main>
""" + footer() + tail()


def fitness():
    goals = ""
    for k in ["loss", "gain", "manage"]:
        s = SVC[k]
        goals += f"""<a class="goal rv" href="#{k}" id="{k}">
      {img(s[4], sizes="(max-width: 900px) 100vw, 33vw")}
      <span class="tag tag--plain">{s[2]}</span>
      <span class="stack"><span class="goal__t">{s[1]}</span><span class="body" style="color:rgba(255,255,255,.8)">{s[5]}</span><span class="link" style="justify-self:start">Enquire <span class="arr" aria-hidden="true">→</span></span></span>
    </a>"""
    return head("fitness.html", "Gym, HIIT, Aerobics & Personal Training in DHA Phase 6, Karachi | K7",
                "Gym, HIIT, aerobics, personal training, weight loss, weight gain, weight management and nutrition consulting at K7 Kickboxing Gym, DHA Phase 6, Karachi.", "gym3") + header("fitness") + f"""
<main id="main">
{page_hero("Fitness", ["Stronger in", "every direction."], "Gym, HIIT, aerobics, personal training and nutrition guidance, built around what you want to achieve.", "gym3", "FIT", btn("Enquire now", enquire_href("Personal Training"), "btn--solid"))}
<section class="sec sec--light" aria-labelledby="goal-title">
  <div class="wrap">
    <div class="shead shead--split"><span class="shead__num" aria-hidden="true">01</span><div class="shead__body">{tag("Start with your goal", cls="tag--plain")}{lines("What are you", "training for?", extra='id="goal-title"')}</div><p class="body rv" style="max-width:24em">Tell us where you are and where you want to be. Training and nutrition work together to get you there.</p></div>
  </div>
  <div class="goals">{goals}</div>
</section>
<section class="sec--dark" aria-label="Training formats">
{disc("02", "gym", ["Gym"], "Strength and conditioning.", SVC["gym"][5], ["Strength", "Conditioning", "Muscle building", "All levels"], "gym", program="Gym")}
{disc("03", "hiit", ["HIIT"], "High Intensity Interval Training.", SVC["hiit"][5], ["Intervals", "Conditioning", "Fat burning", "Endurance"], "hiit", rev=True, light=True, program="HIIT — High Intensity Interval Training")}
{disc("04", "aerobics", ["Aerobics"], "Cardio with rhythm.", SVC["aerobics"][5], ["Stamina", "Coordination", "Heart health", "Energy"], "aerobics", program="Aerobics")}
{disc("05", "personal", ["Personal", "Training"], "Coaching built around you.", SVC["personal"][5], ["Goal setting", "Tailored sessions", "Accountability", "Progress tracking"], "personal", rev=True, light=True, program="Personal Training")}
</section>
<section class="sec sec--coal" id="nutrition" aria-labelledby="nut-title">
  <div class="wrap intro">
    <div class="intro__text">
      {tag("Wellness & nutrition", "06")}
      {lines("Fuel the", "work.", extra='id="nut-title"')}
      <p class="lede rv">{SVC["nutrition"][5]}</p>
      <p class="body rv">Whether your goal is weight loss, weight gain or long-term weight management, nutrition consulting helps make the effort you put in at the gym count.</p>
      <ul class="pillars rv" aria-label="Nutrition goals"><li>Weight loss</li><li>Weight gain</li><li>Weight management</li></ul>
      <div class="btn-row rv">{btn("Enquire about nutrition", enquire_href("Nutrition Consulting"), "btn--solid")}</div>
    </div>
    {ph("nutrition", "intro__media")}
  </div>
</section>
{cta(("Build your", "best shape."), "Enquire about gym training, HIIT, aerobics, personal training or nutrition.", "gym2")}
</main>
""" + footer() + tail()


def kids():
    blocks = ""
    for i, k in enumerate(["youth", "kidskick", "gymnastics"]):
        s = SVC[k]
        blocks += disc(f"0{i+1}", k, [s[1]], s[2] + ".", s[5], {
            "youth": ["Fitness", "Coordination", "Discipline", "Teamwork"],
            "kidskick": ["Focus", "Control", "Confidence", "Fundamentals"],
            "gymnastics": ["Balance", "Flexibility", "Body control", "Coordination"]}[k],
            s[4], rev=bool(i % 2), light=bool(i % 2), program=PROGRAM_NAMES[k])
    return head("kids.html", "Kids Kickboxing, Gymnastics & Youth Classes in Karachi | K7 Kickboxing Gym",
                "Youth classes, kids kickboxing and kids gymnastics at K7 Kickboxing Gym, DHA Phase 6, Karachi. Enquire for age groups and class timings.", "kidskick") + header("kids") + f"""
<main id="main">
{page_hero("Kids & Youth", ["Start them", "strong."], "Youth classes, kids kickboxing and kids gymnastics. Structured training that builds coordination, confidence and discipline.", "youth", "K7", btn("Enquire about kids programs", enquire_href("Kids Kickboxing"), "btn--solid"))}
<section class="sec sec--light" aria-labelledby="parents-title">
  <div class="wrap grid-2">
    <div class="stack">{tag("For parents", cls="tag--plain")}{lines("Three ways", "to start.", extra='id="parents-title"')}</div>
    <div class="stack rv"><p class="lede">Every child is different. Some love to move, some need a place to focus, some want to learn a sport properly.</p><p class="body">Our three kids and youth programs cover each of those. Enquire and we'll help you choose the right one for your child's age and interests.</p></div>
  </div>
</section>
<section class="sec--dark" aria-label="Kids and youth programs">{blocks}</section>
<section class="sec sec--light" aria-labelledby="faq-title">
  <div class="wrap grid-2" style="align-items:start">
    <div class="stack">{tag("Before you enquire", cls="tag--plain")}{lines("Parents ask", extra='id="faq-title"')}</div>
    <div class="faq">
      <details><summary>Which program suits my child?<i aria-hidden="true"></i></summary><p class="body">Tell us your child's age, experience and what they enjoy, and we'll recommend youth classes, kids kickboxing or kids gymnastics.</p></details>
      <details><summary>What ages do you take?<i aria-hidden="true"></i></summary><p class="body">Age groups are confirmed directly with our team. Call {PHONE} or send an enquiry and we'll let you know.</p></details>
      <details><summary>When are classes held?<i aria-hidden="true"></i></summary><p class="body">The gym is open Monday to Saturday, 9:00 AM to 10:00 PM. Ask us for the current kids and youth class times.</p></details>
      <details><summary>Does my child need experience?<i aria-hidden="true"></i></summary><p class="body">Mention your child's experience level when you enquire so we can guide you to the right starting point.</p></details>
    </div>
  </div>
</section>
{cta(("Their first", "round starts here."), "Enquire about youth classes, kids kickboxing or kids gymnastics.", "kidskick")}
</main>
""" + footer() + tail()


def female():
    return head("female-only.html", "Female-Only Training Sessions in DHA Phase 6, Karachi | K7 Kickboxing Gym",
                "Female-only training sessions at K7 Kickboxing Gym, Ittehad Commercial Area, DHA Phase 6, Karachi. Enquire for session timings.", "women") + header("female") + f"""
<main id="main">
{page_hero("Female-Only Sessions", ["Train on", "your terms."], "Dedicated sessions for women who want to train in a female-only setting. Professional, focused and welcoming.", "women2", "K7", btn("Enquire about sessions", enquire_href("Female-Only Sessions"), "btn--solid") + btn("Call " + PHONE, "tel:" + TEL))}
<section class="sec sec--light" id="female" aria-labelledby="fem-why">
  <div class="wrap manifesto">
    {tag("Female-only sessions", "01")}
    <h2 id="fem-why" class="statement lines"><span><span>Same standards.</span></span><span><span class="o">Same intensity.</span></span><span><span>Same K7.</span></span></h2>
    <div class="grid-2">
      <p class="lede rv">Some women simply train better in a female-only setting. These sessions exist for exactly that.</p>
      <p class="body rv">You get the same serious approach to training that defines everything at K7, in a space set aside for women. Contact us to find out session timings and which training is available.</p>
    </div>
  </div>
</section>
<section class="sec--dark">
  <div class="feature feature--rev">
    <div class="feature__media">{ph("women", sizes="(max-width: 900px) 100vw, 50vw")}</div>
    <div class="feature__body">
      {tag("What it's about", "02")}
      <ul class="princ" style="border-color:rgba(255,255,255,.3)">
        <li class="princ__row rv"><h3 class="h3">Focus</h3><p class="body">Time and space that's yours, so you can put everything into the session.</p></li>
        <li class="princ__row rv"><h3 class="h3">Strength</h3><p class="body">Real training with real intent, whatever your starting point.</p></li>
        <li class="princ__row rv"><h3 class="h3">Respect</h3><p class="body">A professional environment where everyone is there to work.</p></li>
      </ul>
    </div>
  </div>
</section>
<section class="sec sec--coal" aria-labelledby="ffaq">
  <div class="wrap grid-2" style="align-items:start">
    <div class="stack">{tag("Before you enquire", cls="tag--plain")}{lines("Good to know", extra='id="ffaq"')}</div>
    <div class="faq">
      <details><summary>When are female-only sessions?<i aria-hidden="true"></i></summary><p class="body">Session timings are shared on enquiry. Call {PHONE} or send us a message.</p></details>
      <details><summary>What kind of training is included?<i aria-hidden="true"></i></summary><p class="body">Ask us when you enquire and we'll explain the current session format.</p></details>
      <details><summary>I'm new to training. Can I join?<i aria-hidden="true"></i></summary><p class="body">Tell us about your experience when you get in touch and we'll guide you on where to start.</p></details>
    </div>
  </div>
</section>
{cta(("Your session", "is waiting."), "Enquire about female-only sessions at K7, DHA Phase 6.", "women2")}
</main>
""" + footer() + tail()


def enquire():
    return head("enquire.html", "Membership & Enquiries | K7 Kickboxing Gym, DHA Phase 6 Karachi",
                "Enquire about membership and programs at K7 Kickboxing Gym, Karachi. Kickboxing, MMA, fitness, kids classes and female-only sessions.", "gloves") + header("enquire") + f"""
<main id="main">
{page_hero("Enquire", ["Ready", "to train?"], "Send an enquiry and tell us what you want to work on. Membership options and pricing are shared on enquiry.", "gloves", None, "", short=True)}
<section class="sec sec--dark" style="padding-top:clamp(40px,5vw,72px)" aria-label="Enquiry form">
  <div class="wrap enq">
    <aside class="enq__aside">
      {tag("How it works", "01")}
      <ol class="steps rv">
        <li><div><b>Send your enquiry</b><span class="muted">Choose a program and tell us a little about your goals.</span></div></li>
        <li><div><b>We get in touch</b><span class="muted">We'll reply with membership options, pricing and timings.</span></div></li>
        <li><div><b>Start training</b><span class="muted">Visit us in DHA Phase 6 and get to work.</span></div></li>
      </ol>
      <!-- EDIT: add membership plans here once pricing is confirmed. -->
      <div class="slot rv" data-slot="Membership">
        <p class="h4">Membership & pricing</p>
        <p class="body">Membership options and pricing are shared on enquiry. Call {PHONE} for details.</p>
      </div>
      <div class="btn-row rv">{btn("Call " + PHONE, "tel:" + TEL)}</div>
    </aside>
    <div class="rv">{form("enquire")}</div>
  </div>
</section>
{hours_block(dark=False, num="02")}
</main>
""" + footer() + tail()


def contact():
    addr = "<br>".join(ADDR_LINES)
    return head("contact.html", "Contact K7 Kickboxing Gym | Ittehad Commercial Area, DHA Phase 6, Karachi",
                "Find K7 Kickboxing Gym at 11-C Ittehad Lane 2, Ittehad Commercial Area, DHA Phase 6, Karachi 75500. Call 0348 2136361. Open Mon–Sat, 9 AM–10 PM.", "functional") + header("contact") + f"""
<main id="main">
{page_hero("Contact", ["Find K7."], "Ittehad Commercial Area, DHA Phase 6, Karachi. Call, visit or send us a message.", "functional", None, btn("Call " + PHONE, "tel:" + TEL, "btn--solid") + btn("Get directions", DIRECTIONS, "", 'target="_blank" rel="noopener"'), short=True)}
<section class="sec sec--dark" style="padding-top:clamp(24px,4vw,56px)" aria-label="Contact details">
  <div class="wrap">
    <div class="cinfo">
      <div class="rv"><h2 class="tag tag--plain muted">Address</h2><address class="cinfo__big" style="font-size:clamp(1.5rem,2.2vw,2.1rem);line-height:1.05">{NAME}</address><p class="body" style="color:rgba(255,255,255,.85)">{addr}</p>{btn("Get directions", DIRECTIONS, "btn--sm", 'target="_blank" rel="noopener"')}</div>
      <div class="rv rv-d1"><h2 class="tag tag--plain muted">Phone</h2><a class="cinfo__big" href="tel:{TEL}">{PHONE}</a><p class="body">Call during opening hours.</p>{btn("Call now", "tel:" + TEL, "btn--sm")}</div>
      <div class="rv rv-d2"><h2 class="tag tag--plain muted">Hours</h2><p class="cinfo__big">Monday — Saturday<br>9:00 AM — 10:00 PM</p><p class="cinfo__big" style="color:transparent;-webkit-text-stroke:1px #fff">Sunday closed</p>{status()}</div>
    </div>
    <div class="map mt-m rv">
      <p class="map__pin">K7 / DHA Phase 6, Karachi</p>
      <iframe title="Map showing K7 Kickboxing Gym, Ittehad Commercial Area, DHA Phase 6, Karachi" src="{MAP_EMBED}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
    </div>
  </div>
</section>
<section class="sec sec--coal" aria-labelledby="msg-title">
  <div class="wrap enq">
    <div class="enq__aside">{tag("Send a message", "02")}{lines("Talk to", "K7.", extra='id="msg-title"')}<p class="body rv">Questions about programs, timings or membership? Send a message and we'll get back to you.</p></div>
    <div class="rv">{form("contact")}</div>
  </div>
</section>
</main>
""" + footer() + tail()


PAGES = {
    "index.html": home, "about.html": about, "programs.html": programs, "combat.html": combat,
    "fitness.html": fitness, "kids.html": kids, "female-only.html": female, "enquire.html": enquire, "contact.html": contact,
}

if __name__ == "__main__":
    for name, fn in PAGES.items():
        with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
            f.write(fn())
        print("built", name)
    with open(os.path.join(ROOT, "robots.txt"), "w") as f:
        f.write("User-agent: *\nAllow: /\n" + (f"Sitemap: {SITE_URL}/sitemap.xml\n" if SITE_URL else ""))
    if SITE_URL:
        urls = "".join(f"<url><loc>{SITE_URL}/{'' if n == 'index.html' else n}</loc></url>" for n in PAGES)
        with open(os.path.join(ROOT, "sitemap.xml"), "w") as f:
            f.write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
