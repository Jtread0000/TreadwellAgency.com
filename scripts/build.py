#!/usr/bin/env python3
"""
Treadwell Agency — static site generator.

Assembles shared chrome (header, footer, <head>) with each route's content
and writes plain static HTML to real routes:

    /                 index.html
    /services/        services/index.html
    /training/        training/index.html
    /ai-readiness/    ai-readiness/index.html
    /approach/        approach/index.html
    /about/           about/index.html

No runtime framework — output is pure HTML/CSS + one tiny nav.js.
Run:  python3 scripts/build.py
"""

import os
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ------------------------------------------------------------------ config
SITE_URL = "https://treadwellagency.com"
EMAIL = "hello@treadwellagency.com"


def mailto(subject):
    return "mailto:" + EMAIL + "?subject=" + quote(subject)


CTA_MAILTO = mailto("Consultation request — Treadwell Agency")

# ------------------------------------------------------------------ icons
ICONS = {
    "grad": '<path d="M22 10 12 5 2 10l10 5 10-5Z"/><path d="M6 12v5c0 1 2 3 6 3s6-2 6-3v-5"/>',
    "workflow": '<rect x="3" y="3" width="8" height="8" rx="1"/><rect x="13" y="13" width="8" height="8" rx="1"/><path d="M11 7h4a2 2 0 0 1 2 2v4"/>',
    "brain": '<rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><path d="M9 2v2M15 2v2M9 20v2M15 20v2M2 9h2M2 15h2M20 9h2M20 15h2"/>',
    "message": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
    "route": '<circle cx="6" cy="19" r="3"/><path d="M9 19h8.5a3.5 3.5 0 0 0 0-7h-11a3.5 3.5 0 0 1 0-7H15"/><circle cx="18" cy="5" r="3"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "building": '<path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z"/><path d="M6 12H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2"/><path d="M18 9h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-2"/><path d="M10 6h4M10 10h4M10 14h4"/>',
    "eye": '<path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/>',
    "wrench": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76Z"/>',
    "trending": '<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/><path d="m9 12 2 2 4-4"/>',
    "sparkle": '<path d="M12 3l1.9 5.8a2 2 0 0 0 1.3 1.3L21 12l-5.8 1.9a2 2 0 0 0-1.3 1.3L12 21l-1.9-5.8a2 2 0 0 0-1.3-1.3L3 12l5.8-1.9a2 2 0 0 0 1.3-1.3z"/>',
    "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    "zap": '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>',
    "arrow": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "download": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>',
}


def svg(name, size=22, sw=2):
    return (
        '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" '
        'stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" '
        'stroke-linejoin="round" aria-hidden="true">{p}</svg>'
    ).format(s=size, sw=sw, p=ICONS[name])


# ------------------------------------------------------------------ logo
def logo(tone="blue", size=30):
    tones = {
        "blue": ("var(--tw-blue)", "var(--tw-blue)", "#fff"),
        "white": ("#fff", "#fff", "var(--tw-blue)"),
    }
    ink, mark_bg, mark_fg = tones[tone]
    gap = round(size * 0.28, 2)
    wm_fs = round(size * 0.62, 2)
    mark = (
        '<svg width="{s}" height="{s}" viewBox="0 0 200 200" aria-hidden="true">'
        '<circle cx="100" cy="100" r="100" fill="{bg}"/>'
        '<g transform="translate(44 39)" fill="{fg}">'
        '<polygon points="0 0 0 20.18 103.77 0 0 0"/>'
        '<polygon points="0 23.72 0 34.38 35.77 34.38 35.77 121.55 76.41 121.55 '
        '76.41 34.38 112.18 34.38 112.18 1.91 0 23.72"/></g></svg>'
    ).format(s=size, bg=mark_bg, fg=mark_fg)
    wm = (
        '<span class="wm" style="font-size:{fs}px;color:{ink};">'
        '<span>Tread</span><span class="thin">well</span></span>'
    ).format(fs=wm_fs, ink=ink)
    return (
        '<span class="tw-logo" style="gap:{gap}px;">{mark}{wm}</span>'
    ).format(gap=gap, mark=mark, wm=wm)


# ------------------------------------------------------------------ nav
NAV = [
    ("Services", "/services/", "services"),
    ("Training", "/training/", "training"),
    ("AI Readiness", "/ai-readiness/", "readiness"),
    ("Approach", "/approach/", "approach"),
]


def header(active):
    links = "".join(
        '<a class="nav-link{act}" href="{href}">{label}</a>'.format(
            act=" active" if key == active else "", href=href, label=label
        )
        for label, href, key in NAV
    )
    mlinks = "".join(
        '<a class="{act}" href="{href}">{label}</a>'.format(
            act="active" if key == active else "", href=href, label=label
        )
        for label, href, key in NAV
    )
    return """<header class="site-header">
  <div class="bar">
    <a href="/" aria-label="Treadwell Agency home" style="display:inline-flex;">{logo}</a>
    <nav class="nav-links" aria-label="Primary">
      {links}
      <span class="nav-cta"><a class="tw-btn tw-btn--accent tw-btn--sm" href="{cta}">Book a consultation</a></span>
    </nav>
    <button class="burger" id="burger" aria-label="Menu" aria-expanded="false" aria-controls="mobile-menu">
      <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 6h16M4 12h16M4 18h16"/></svg>
    </button>
  </div>
  <div class="mobile-menu" id="mobile-menu">
    {mlinks}
    <a class="tw-btn tw-btn--accent" style="margin-top:8px;" href="{cta}">Book a consultation</a>
  </div>
</header>""".format(logo=logo("blue", 30), links=links, mlinks=mlinks, cta=CTA_MAILTO)


def footer():
    links = "".join(
        '<a href="{href}">{label}</a>'.format(href=href, label=label)
        for label, href, key in NAV
    )
    return """<footer class="site-footer">
  <div class="cols">
    <div>
      {logo}
      <p class="tagline">Workforce &amp; organization transformation for the age of AI. We solve for the human factor.</p>
    </div>
    <div>
      <div class="foot-h">Explore</div>
      <div class="foot-links">{links}<a href="/about/">About</a></div>
    </div>
    <div>
      <div class="foot-h">Get in touch</div>
      <a class="foot-email" href="{mail}">{email}</a>
      <div style="margin-top:16px;"><a class="tw-btn tw-btn--signal tw-btn--sm" href="{cta}">Book a consultation</a></div>
    </div>
  </div>
  <div class="foot-bottom">&copy; 2026 Treadwell Agency LLC &middot; We solve for the human factor</div>
</footer>""".format(
        logo=logo("white", 28),
        links=links,
        mail="mailto:" + EMAIL,
        email=EMAIL,
        cta=CTA_MAILTO,
    )


# ------------------------------------------------------------------ shell
def page(active, title, description, body, path_for_canonical):
    canonical = SITE_URL + path_for_canonical
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Treadwell Agency">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{site}/assets/canvas-preview.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#271DCC">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:ital,wght@0,100..900;1,100..900&family=JetBrains+Mono:wght@400;500;700&display=swap">
<link rel="stylesheet" href="/assets/css/site.css">
</head>
<body>
{header}
<main>
{body}
</main>
{footer}
<script src="/assets/js/nav.js"></script>
</body>
</html>
""".format(
        title=title,
        desc=description,
        canonical=canonical,
        site=SITE_URL,
        header=header(active),
        body=body,
        footer=footer(),
    )


# ================================================================== content
def eyebrow(text, color="var(--tw-blue)"):
    return '<span class="tw-eyebrow" style="color:{c};">{t}</span>'.format(c=color, t=text)


def belief_band():
    return """<section class="band" style="background:var(--tw-black);padding:92px 28px;overflow:hidden;">
  <img class="motif" src="/assets/elements/Yellow-Waves.png" alt="" aria-hidden="true" style="left:50%;top:50%;transform:translate(-50%,-50%);width:1200px;opacity:.14;">
  <div class="wrap" style="max-width:900px;text-align:center;">
    <p style="font-family:var(--font-display);font-weight:900;text-transform:uppercase;font-size:clamp(1.7rem,3.4vw,2.8rem);letter-spacing:-.02em;line-height:1.08;color:#fff;margin:0;">Technology enables change.<br><span style="color:var(--tw-yellow);">People determine whether change succeeds.</span></p>
  </div>
</section>"""


def cta_strip(heading, body_html, btn_label, btn_href, btn_variant="accent"):
    body = (
        '<p style="color:var(--text-body);line-height:1.55;max-width:52ch;margin:0 auto 26px;">{b}</p>'.format(b=body_html)
        if body_html
        else ""
    )
    return """<section style="background:var(--tw-neutral-50);padding:0 28px 96px;">
  <div class="wrap" style="max-width:1000px;text-align:center;">
    <h3 style="font-family:var(--font-display);font-weight:900;text-transform:uppercase;font-size:clamp(1.6rem,3vw,2.4rem);letter-spacing:-.02em;margin:0 0 18px;">{h}</h3>
    {body}
    <a class="tw-btn tw-btn--{v} tw-btn--lg" href="{href}">{label}</a>
  </div>
</section>""".format(h=heading, body=body, v=btn_variant, href=btn_href, label=btn_label)


def detail_card(icon, title, para, checks, outcome, tag_html=""):
    checks_html = "".join(
        '<span><span class="tick">✓</span>{c}</span>'.format(c=c) for c in checks
    )
    if tag_html:
        head = (
            '<div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:8px;">'
            '<h3 style="font-family:var(--font-display);font-weight:800;font-size:24px;margin:0;text-transform:uppercase;letter-spacing:-.01em;">{t}</h3>{tag}</div>'
        ).format(t=title, tag=tag_html)
    else:
        head = (
            '<h3 style="font-family:var(--font-display);font-weight:800;font-size:24px;margin:0 0 8px;text-transform:uppercase;letter-spacing:-.01em;">{t}</h3>'
        ).format(t=title)
    return """<article class="tw-card tw-card--plain">
  <div class="detail-grid">
    <span class="icon-chip-wash">{icon}</span>
    <div>
      {head}
      <p style="margin:0 0 16px;color:var(--text-body);line-height:1.55;max-width:62ch;">{para}</p>
      <div class="checklist">{checks}</div>
      <div class="outcome-line">Outcome &mdash; {outcome}</div>
    </div>
  </div>
</article>""".format(
        icon=svg(icon, 26), head=head, para=para, checks=checks_html, outcome=outcome
    )


# ---------------------------------------------------------------- HOME
def home_body():
    offerings = [
        ("grad", "Workforce Readiness", "Preparing employees and organizations for the future of work through practical AI capability development."),
        ("workflow", "Organizational Transformation", "Helping organizations move from AI experimentation to enterprise-wide adoption."),
        ("brain", "AI Strategy", "Helping leaders understand where AI creates value &mdash; and how to implement it responsibly."),
    ]
    cards = "".join(
        """<article class="tw-card tw-card--hard">
      <div style="display:flex;flex-direction:column;gap:14px;height:100%;">
        <span class="icon-chip-blue">{icon}</span>
        <h3 style="font-family:var(--font-display);font-weight:800;font-size:23px;margin:0;text-transform:uppercase;letter-spacing:-.01em;">{t}</h3>
        <p style="margin:0;color:var(--text-body);line-height:1.55;">{d}</p>
      </div>
    </article>""".format(icon=svg(ic, 24), t=t, d=d)
        for ic, t, d in offerings
    )

    topic = """<section style="background:var(--tw-neutral-50);padding:0 28px 96px;">
  <div class="wrap">
    <article class="tw-card tw-card--signal">
      <div class="topic-grid" style="display:grid;grid-template-columns:1.4fr 1fr;gap:36px;align-items:center;">
        <div>
          {eb}
          <h3 style="font-family:var(--font-display);font-weight:900;text-transform:uppercase;font-size:clamp(1.6rem,3vw,2.4rem);letter-spacing:-.02em;line-height:1.02;margin:14px 0 12px;">Turning AI pilots into an operating model</h3>
          <p style="margin:0 0 22px;color:rgba(10,10,10,.78);line-height:1.55;max-width:52ch;">A facilitated leadership session for teams stuck between experimentation and enterprise adoption. Complete the AI Readiness Canvas together and leave with an actionable roadmap.</p>
          <a class="tw-btn tw-btn--primary" href="{cta}">Reserve a seat</a>
        </div>
        <div style="display:grid;gap:12px;">
          {facts}
        </div>
      </div>
    </article>
  </div>
</section>""".format(
        eb=eyebrow("Workshop · Topic this month", "var(--tw-black)"),
        cta=CTA_MAILTO,
        facts="".join(
            '<div style="background:rgba(10,10,10,.06);border-radius:10px;padding:16px 18px;">'
            '<div style="font-family:var(--font-mono);font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:rgba(10,10,10,.6);">{k}</div>'
            '<div style="font-weight:700;margin-top:4px;">{v}</div></div>'.format(k=k, v=v)
            for k, v in [("Format", "Facilitated, half-day"), ("For", "Leadership teams"), ("Outcome", "Aligned AI roadmap")]
        ),
    )

    return """<div>
  <div class="band" style="overflow:hidden;background:var(--tw-grad-yellow);">
    <img class="motif" src="/assets/elements/White-Track.png" alt="" aria-hidden="true" style="right:-60px;top:-40px;width:904px;height:848px;opacity:.55;">
    <div class="wrap" style="padding:112px 28px 118px;">
      {eb}
      <h1 class="hero-h1" style="font-size:clamp(3rem,7vw,6rem);line-height:.92;color:var(--tw-black);max-width:15ch;">We solve for the <span style="color:var(--tw-red);">human</span> factor</h1>
      <p class="lead" style="color:rgba(10,10,10,.78);max-width:52ch;margin:26px 0 34px;font-weight:500;">Treadwell prepares leaders, employees, and businesses for the future of work in the age of AI &mdash; and beyond. We start with your business outcomes, not the tools.</p>
      <div class="btn-row">
        <a class="tw-btn tw-btn--primary tw-btn--lg" href="{cta}">Book a consultation {arrow}</a>
        <a class="tw-btn tw-btn--outline tw-btn--lg" href="/approach/">Explore our approach</a>
      </div>
      <div class="tag-row" style="margin-top:40px;">
        <span class="tw-tag tw-tag--blue tw-tag--solid">Workforce Readiness</span>
        <span class="tw-tag tw-tag--neutral tw-tag--solid">Organizational Transformation</span>
        <span class="tw-tag tw-tag--red tw-tag--solid">AI Strategy</span>
      </div>
    </div>
  </div>

  <section class="band" style="background:var(--tw-blue);padding:88px 28px;overflow:hidden;">
    <img class="motif" src="/assets/elements/White-Donut.png" alt="" aria-hidden="true" style="right:-120px;top:50%;transform:translateY(-50%);width:520px;opacity:.5;">
    <div class="wrap" style="max-width:1000px;">
      {eb_phil}
      <h2 class="h2-display" style="font-size:clamp(2rem,4.4vw,3.4rem);line-height:1;color:#fff;margin:16px 0 22px;max-width:20ch;">Technology is changing faster than organizations can adapt.</h2>
      <p class="lead" style="color:rgba(255,255,255,.82);max-width:60ch;line-height:1.6;margin:0;">Our mission is to increase human capability faster than technology increases complexity. Rather than starting with AI tools, we begin with the outcomes your business is trying to reach.</p>
    </div>
  </section>

  <section style="background:var(--bg);padding:96px 28px;">
    <div class="wrap">
      {eb_do}
      <h2 class="h2-display" style="font-size:clamp(2rem,4vw,3.25rem);margin:14px 0 46px;max-width:22ch;">Three ways we build readiness</h2>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:22px;">
        {cards}
      </div>
    </div>
  </section>

  {topic}

  {belief}
</div>""".format(
        eb=eyebrow("Workforce &amp; Organization Transformation"),
        cta=CTA_MAILTO,
        arrow=svg("arrow", 18, 2.5),
        eb_phil=eyebrow("Our philosophy", "var(--tw-yellow)"),
        eb_do=eyebrow("What we do"),
        cards=cards,
        topic=topic,
        belief=belief_band(),
    )


# ---------------------------------------------------------------- SERVICES
def services_body():
    cards = "".join([
        detail_card("grad", "Workforce Readiness",
            "Preparing employees and organizations for the future of work through practical AI capability development &mdash; hands-on, role-relevant, and measurable.",
            ["Practical, hands-on workshops", "Executive &amp; leadership readiness", "Role-based capability paths", "Behavior-based culture change"],
            "A workforce that can put AI to work responsibly."),
        detail_card("workflow", "Organizational Transformation",
            "Helping organizations move from AI experimentation to enterprise-wide adoption &mdash; with governance, modernization, and human-centered change that actually sticks.",
            ["AI governance &amp; risk implementation", "Process &amp; technology modernization", "Human-centered change adoption", "Digital-maturity roadmapping"],
            "AI becomes part of how the organization operates."),
        detail_card("brain", "AI Strategy",
            "Helping leaders understand where AI creates value &mdash; and how to implement it responsibly. We prioritize the smallest meaningful wins before the big bets.",
            ["Value mapping &amp; use-case triage", "AI Readiness Canvas facilitation", "Responsible-AI guardrails", "Prioritized, phased roadmap"],
            "A clear, responsible path from pilot to value."),
    ])
    return """<div>
  <div class="band" style="background:var(--tw-blue);padding:96px 28px 84px;overflow:hidden;">
    <img class="motif" src="/assets/elements/White-Donut.png" alt="" aria-hidden="true" style="right:-80px;top:-40px;width:480px;opacity:.5;">
    <div class="wrap">
      {eb}
      <h1 class="hero-h1" style="font-size:clamp(2.4rem,5.5vw,4.5rem);line-height:.95;color:#fff;max-width:16ch;">Outcomes first, tools second</h1>
      <p class="lead" style="color:rgba(255,255,255,.82);max-width:54ch;margin-top:22px;">Three practices, one throughline: closing the gap between how fast AI is changing work and how fast your people can adapt.</p>
    </div>
  </div>
  <section style="background:var(--bg);padding:88px 28px;">
    <div class="wrap" style="max-width:1100px;display:grid;gap:22px;">
      {cards}
    </div>
  </section>
  {cta}
</div>""".format(
        eb=eyebrow("What we deliver", "var(--tw-yellow)"),
        cards=cards,
        cta=cta_strip("See where AI creates value for you", "", "Explore AI Readiness", "/ai-readiness/", "accent"),
    )


# ---------------------------------------------------------------- TRAINING
def training_body():
    wioa_tag = '<span class="tw-tag tw-tag--blue tw-tag--soft">WIOA</span>'
    cards = "".join([
        detail_card("grad", "Corporate Courses &amp; Workforce Development",
            "Practical, role-based courses that build durable capability across your organization &mdash; from frontline teams to executive leadership. Instructor-led or self-paced.",
            ["AI &amp; digital-fluency curriculum", "Role-based learning paths", "Instructor-led &amp; self-paced formats", "Measurable skill growth"],
            "A future-proof workforce."),
        detail_card("users", "State Workforce Training Program",
            "Delivered under the Workforce Innovation &amp; Opportunity Act (WIOA), we help employers build talent pipelines through funded, credential-aligned training &mdash; connecting your open roles to job-ready talent.",
            ["WIOA-aligned, fundable programs", "Credential &amp; certification pathways", "Employer&ndash;talent pipeline partnerships", "Onboarding &amp; upskilling at scale"],
            "New talent, trained and job-ready.", tag_html=wioa_tag),
        detail_card("shield", "Annual Cybersecurity Training",
            "Behavior-based security awareness and compliance training that keeps your entire organization current &mdash; every year &mdash; and your records audit-ready.",
            ["Annual awareness &amp; compliance curriculum", "Phishing &amp; social-engineering readiness", "Role-specific security modules", "Completion tracking &amp; reporting"],
            "A security-aware culture, audit-ready."),
    ])
    return """<div>
  <div class="band" style="background:var(--tw-black);padding:96px 28px 84px;overflow:hidden;">
    <img class="motif" src="/assets/elements/Yellow-Circle.png" alt="" aria-hidden="true" style="right:-70px;bottom:-70px;width:540px;opacity:.5;">
    <div class="wrap">
      {eb}
      <h1 class="hero-h1" style="font-size:clamp(2.4rem,5.5vw,4.5rem);line-height:.95;color:#fff;max-width:17ch;">Training that keeps your workforce ready</h1>
      <p class="lead" style="color:rgba(255,255,255,.82);max-width:56ch;margin-top:22px;">Practical, credential-aligned programs for corporations &mdash; building the skills your teams need for the future of work, from AI fluency to security.</p>
      <div class="tag-row" style="margin-top:30px;">
        <span class="tw-tag tw-tag--yellow tw-tag--solid">Corporate Courses</span>
        <span class="tw-tag tw-tag--blue tw-tag--solid">WIOA Workforce Program</span>
        <span class="tw-tag tw-tag--red tw-tag--solid">Cybersecurity Training</span>
      </div>
    </div>
  </div>
  <section style="background:var(--bg);padding:88px 28px;">
    <div class="wrap" style="max-width:1100px;display:grid;gap:22px;">
      {cards}
    </div>
  </section>
  {cta}
</div>""".format(
        eb=eyebrow("Courses &amp; Training", "var(--tw-yellow)"),
        cards=cards,
        cta=cta_strip(
            "Build a training plan for your team",
            "Programs are tailored to your organization's size, roles, and objectives &mdash; including WIOA funding eligibility. Let's scope it together.",
            "Book a consultation", CTA_MAILTO, "accent"),
    )


# ---------------------------------------------------------------- AI READINESS
def readiness_body():
    method = [
        ("eye", "STEP 1", "See", "Start with the business outcome. Name the bottleneck clearly and measure the drag."),
        ("wrench", "STEP 2", "Solve", "Match the pain point with the right capability. Choose the smallest meaningful win."),
        ("trending", "STEP 3", "Scale", "Turn the solution into a repeatable system. Build it once, reuse it everywhere."),
    ]
    method_cards = "".join(
        """<div style="background:rgba(255,255,255,.06);border:1.5px solid rgba(255,255,255,.16);border-radius:14px;padding:28px;">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;">
          <span style="color:var(--tw-yellow);">{icon}</span>
          <span style="font-family:var(--font-mono);font-weight:700;color:rgba(255,255,255,.5);font-size:13px;letter-spacing:.14em;">{step}</span>
        </div>
        <div style="font-family:var(--font-display);font-weight:900;font-size:32px;color:#fff;margin:0 0 12px;text-transform:uppercase;">{n}<span style="color:var(--tw-yellow);">.</span></div>
        <p style="color:rgba(255,255,255,.82);margin:0;line-height:1.55;">{d}</p>
      </div>""".format(icon=svg(ic, 22), step=step, n=n, d=d)
        for ic, step, n, d in method
    )

    modalities = [
        ("message", "Light touch", "AI Advisor", "Expert guidance, on demand &mdash; for organizations that need a trusted sounding board from time to time.", "Fast decisions without long-term commitments."),
        ("route", "Focused", "AI Consultant", "A personalized engagement where a senior Treadwell advisor works directly with your leaders to develop an AI strategy using the AI Readiness Canvas.", "A prioritized roadmap tailored to your organization."),
        ("users", "Team", "AI Readiness Workshop", "A facilitated leadership workshop where your team completes the AI Readiness Canvas together.", "Leadership alignment and an actionable organizational AI roadmap."),
        ("building", "Enterprise", "AI Readiness Engagement", "A comprehensive transformation engagement where Treadwell embeds alongside leadership to operationalize AI across teams.", "AI readiness becomes part of your operating model."),
    ]
    modality_cards = "".join(
        """<article class="tw-card tw-card--plain">
      <div style="display:flex;flex-direction:column;gap:14px;height:100%;">
        <div style="display:flex;align-items:center;justify-content:space-between;">
          <span class="icon-chip-wash-sm">{icon}</span>
          <span class="tw-tag tw-tag--neutral tw-tag--soft">{tag}</span>
        </div>
        <h3 style="font-family:var(--font-display);font-weight:800;font-size:21px;margin:2px 0 0;text-transform:uppercase;letter-spacing:-.01em;">{t}</h3>
        <p style="margin:0;color:var(--text-body);line-height:1.55;font-size:15px;flex:1;">{d}</p>
        <div style="border-top:1.5px solid var(--border);padding-top:12px;margin-top:2px;">
          <div style="font-family:var(--font-mono);font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--text-muted);margin-bottom:5px;">Outcome</div>
          <div style="font-weight:600;font-size:14px;line-height:1.45;color:var(--text-strong);">{outcome}</div>
        </div>
        <a class="tw-btn tw-btn--primary tw-btn--sm tw-btn--block" href="{mail}">Email us to start</a>
      </div>
    </article>""".format(
            icon=svg(ic, 22), tag=tag, t=t, d=d, outcome=outcome,
            mail=mailto(t + " — Treadwell Agency"))
        for ic, tag, t, outcome, d in [
            (m[0], m[1], m[2], m[4], m[3]) for m in modalities
        ]
    )

    return """<div>
  <div class="band" style="overflow:hidden;background:var(--tw-grad-yellow);">
    <img class="motif" src="/assets/elements/White-Circle.png" alt="" aria-hidden="true" style="right:-60px;top:-40px;width:560px;opacity:.6;">
    <div class="wrap" style="padding:96px 28px 84px;">
      {eb}
      <h1 class="hero-h1" style="font-size:clamp(2.4rem,5.5vw,4.5rem);line-height:.95;color:var(--tw-black);max-width:16ch;">From experimentation to operating model</h1>
      <p class="lead" style="color:rgba(10,10,10,.78);max-width:56ch;margin-top:22px;font-weight:500;">Four ways to engage &mdash; from a light-touch advisor to full organizational transformation. Every path centers on the AI Readiness Canvas.</p>
    </div>
  </div>

  <section class="band" style="background:var(--tw-blue);padding:92px 28px;overflow:hidden;">
    <img class="motif" src="/assets/elements/White-Track.png" alt="" aria-hidden="true" style="right:-140px;top:-80px;width:620px;opacity:.5;">
    <div class="wrap">
      {eb_method}
      <h2 class="h2-display" style="font-size:clamp(2.2rem,5vw,4rem);margin:14px 0 12px;color:#fff;">See<span style="color:var(--tw-yellow);">.</span> Solve<span style="color:var(--tw-yellow);">.</span> Scale<span style="color:var(--tw-yellow);">.</span><sup style="font-size:.4em;vertical-align:super;">&trade;</sup></h2>
      <p class="lead" style="color:rgba(255,255,255,.82);max-width:52ch;margin:0 0 46px;">Impact begins with the next step, not the entire roadmap. A repeatable loop for putting AI to work.</p>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:20px;">
        {method_cards}
      </div>
    </div>
  </section>

  <section class="band" style="background:var(--tw-black);padding:92px 28px;overflow:hidden;">
    <img class="motif" src="/assets/elements/Yellow-Waves.png" alt="" aria-hidden="true" style="left:-160px;bottom:-120px;width:640px;opacity:.14;">
    <div class="wrap" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:56px;align-items:center;">
      <div>
        {eb_dir}
        <h2 class="h2-display" style="font-size:clamp(2rem,4.4vw,3.4rem);line-height:1;color:#fff;margin:14px 0 16px;">Where does impact live?</h2>
        <p class="lead" style="color:rgba(255,255,255,.82);line-height:1.6;margin:0 0 30px;max-width:46ch;">The AI Readiness Canvas<sup style="font-size:.5em;vertical-align:super;">&trade;</sup> maps your organization onto a single page &mdash; from preferred future to first move &mdash; so you can see exactly where AI creates leverage next.</p>
        <div class="btn-row">
          <a class="tw-btn tw-btn--signal tw-btn--lg" href="/assets/canvas/AI-Readiness-Canvas.pdf" download>Download the canvas {dl}</a>
          <a class="tw-btn tw-btn--inverse tw-btn--lg" href="{cta}">Or, we'll walk you through it</a>
        </div>
        <p style="font-family:var(--font-mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:rgba(255,255,255,.5);margin:20px 0 0;">Free &middot; One page &middot; No email required</p>
      </div>
      <a href="/assets/canvas/AI-Readiness-Canvas.pdf" download style="display:block;border-radius:8px;overflow:hidden;box-shadow:12px 12px 0 var(--tw-blue);border:1px solid rgba(255,255,255,.14);">
        <img src="/assets/canvas-preview.png" alt="AI Readiness Canvas &mdash; a one-page AI strategy framework" style="display:block;width:100%;height:auto;">
      </a>
    </div>
  </section>

  <section style="background:var(--bg);padding:92px 28px;">
    <div class="wrap">
      {eb_ways}
      <h2 class="h2-display" style="font-size:clamp(2rem,4vw,3.25rem);margin:14px 0 12px;max-width:20ch;">Four ways to work with us</h2>
      <p class="lead" style="color:var(--text-body);line-height:1.55;max-width:52ch;margin:0 0 46px;">From a light-touch advisor to full organizational transformation. Recommendations are customized to your size, objectives, and outcomes.</p>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:22px;">
        {modality_cards}
      </div>
    </div>
  </section>
</div>""".format(
        eb=eyebrow("AI Readiness"),
        eb_method=eyebrow("Our methodology", "var(--tw-yellow)"),
        eb_dir=eyebrow("The direction", "var(--tw-yellow)"),
        eb_ways=eyebrow("Ways to engage"),
        method_cards=method_cards,
        modality_cards=modality_cards,
        dl=svg("download", 18, 2.5),
        cta=CTA_MAILTO,
    )


# ---------------------------------------------------------------- APPROACH
def approach_body():
    principles = [
        ("users", "People before tools", "The question isn't “what can AI do?” &mdash; it's “what do your people need to do better?” We start there."),
        ("sparkle", "Augment, don't replace", "AI should take the drag off your team and hand back time for judgment, relationships, and creativity."),
        ("target", "Outcomes before AI", "We anchor every engagement to a business result &mdash; not a tool rollout. The tech serves the outcome."),
        ("zap", "The smallest meaningful win", "Momentum beats master plans. We find a fast, real win, prove it, then scale what works."),
    ]
    principle_cards = "".join(
        """<div style="border:1.5px solid var(--border);border-radius:14px;padding:28px;display:flex;flex-direction:column;gap:12px;">
        <span class="icon-chip-wash-sm">{icon}</span>
        <h3 style="font-family:var(--font-display);font-weight:800;font-size:19px;margin:0;text-transform:uppercase;letter-spacing:-.01em;">{t}</h3>
        <p style="margin:0;color:var(--text-body);line-height:1.55;font-size:15px;">{d}</p>
      </div>""".format(icon=svg(ic, 24), t=t, d=d)
        for ic, t, d in principles
    )

    pov = [
        ("Decide what stays human", "Draw the line between what AI assists and what people own."),
        ("Lead through change", "Build the trust and clarity teams need to adopt, not resist."),
        ("Grow judgment, not just skills", "Capability is knowing when &mdash; and when not &mdash; to use the tool."),
    ]
    pov_cols = "".join(
        """<div style="border-top:2px solid var(--tw-yellow);padding-top:16px;">
        <div style="font-family:var(--font-display);font-weight:800;text-transform:uppercase;font-size:18px;color:#fff;letter-spacing:-.01em;margin-bottom:6px;">{t}</div>
        <p style="margin:0;color:rgba(255,255,255,.72);font-size:14px;line-height:1.55;">{d}</p>
      </div>""".format(t=t, d=d)
        for t, d in pov
    )

    ladder = [
        ("01", "Data", "Own your raw signal &mdash; the facts your organization already generates."),
        ("02", "Information", "Organize data into context you can read at a glance."),
        ("03", "Knowledge", "Connect information into patterns your teams can act on."),
        ("04", "Wisdom", "Act on intelligence &mdash; decisions that compound over time."),
    ]
    ladder_cards = "".join(
        """<div style="border:1.5px solid var(--border);border-radius:12px;padding:24px;">
        <div style="font-family:var(--font-mono);font-weight:700;font-size:13px;color:var(--tw-red);letter-spacing:.1em;">{n}</div>
        <div style="font-family:var(--font-display);font-weight:800;font-size:22px;text-transform:uppercase;margin:8px 0 6px;letter-spacing:-.01em;">{t}</div>
        <p style="margin:0;color:var(--text-body);font-size:14px;line-height:1.5;">{d}</p>
      </div>""".format(n=n, t=t, d=d)
        for n, t, d in ladder
    )

    return """<div>
  <div class="band" style="overflow:hidden;background:var(--tw-grad-yellow);">
    <img class="motif" src="/assets/elements/White-Donut.png" alt="" aria-hidden="true" style="right:-60px;top:-40px;width:600px;opacity:.55;">
    <div class="wrap" style="padding:106px 28px 104px;">
      {eb}
      <h1 class="hero-h1" style="font-size:clamp(2.6rem,6vw,5.2rem);line-height:.92;margin:20px 0 0;color:var(--tw-black);max-width:16ch;">Human-first <span style="color:var(--tw-red);">digital</span> transformation</h1>
      <p class="lead" style="color:rgba(10,10,10,.78);max-width:52ch;margin:26px 0 0;font-weight:500;">We don't drop new tools on your teams and hope. We build human capacity first &mdash; so technology amplifies your people instead of leaving them behind.</p>
    </div>
  </div>

  <section class="band" style="background:var(--tw-black);padding:96px 28px;overflow:hidden;">
    <img class="motif" src="/assets/elements/Red-Fractal.png" alt="" aria-hidden="true" style="right:-120px;top:-60px;width:680px;opacity:.5;">
    <div class="wrap" style="max-width:1100px;">
      {eb_gap}
      <h2 class="h2-display" style="font-size:clamp(1.9rem,4vw,3.1rem);line-height:1.02;color:#fff;margin:14px 0 44px;max-width:24ch;">Increase human capability <span style="color:var(--tw-yellow);">faster</span> than technology increases complexity.</h2>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px;align-items:stretch;">
        <div style="background:rgba(255,255,255,.05);border:1.5px solid rgba(255,44,12,.4);border-radius:14px;padding:30px;">
          <div style="font-family:var(--font-mono);font-weight:700;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--tw-red);margin-bottom:14px;">The pressure</div>
          <div style="font-family:var(--font-display);font-weight:800;font-size:26px;text-transform:uppercase;letter-spacing:-.01em;color:#fff;margin-bottom:12px;">Complexity keeps rising</div>
          <p style="margin:0;color:rgba(255,255,255,.72);line-height:1.6;">New tools, new risks, new expectations &mdash; technology adds complexity faster than most organizations can absorb it.</p>
        </div>
        <div style="background:var(--tw-yellow);border-radius:14px;padding:30px;box-shadow:8px 8px 0 var(--tw-blue);">
          <div style="font-family:var(--font-mono);font-weight:700;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:rgba(10,10,10,.6);margin-bottom:14px;">Our answer</div>
          <div style="font-family:var(--font-display);font-weight:900;font-size:26px;text-transform:uppercase;letter-spacing:-.01em;color:var(--tw-black);margin-bottom:12px;">Capability rises faster</div>
          <p style="margin:0;color:rgba(10,10,10,.8);line-height:1.6;font-weight:500;">We grow the human capacity to meet it &mdash; skills, judgment, and confidence &mdash; so your people stay ahead of the curve, not behind it.</p>
        </div>
      </div>
    </div>
  </section>

  <section style="background:var(--bg);padding:96px 28px;">
    <div class="wrap">
      {eb_work}
      <h2 class="h2-display" style="font-size:clamp(2rem,4vw,3.25rem);margin:14px 0 46px;max-width:20ch;">Human-first, at every step</h2>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:20px;">
        {principle_cards}
      </div>
    </div>
  </section>

  <section class="band" style="background:var(--tw-blue);padding:96px 28px;overflow:hidden;">
    <img class="motif" src="/assets/elements/White-Circle.png" alt="" aria-hidden="true" style="right:-90px;bottom:-70px;width:460px;opacity:.5;">
    <div class="wrap" style="max-width:1000px;">
      {eb_pov}
      <h2 class="h2-display" style="font-size:clamp(2rem,4.4vw,3.4rem);line-height:1;color:#fff;margin:14px 0 20px;max-width:18ch;">Management in the age of AI</h2>
      <p class="lead" style="color:rgba(255,255,255,.85);line-height:1.65;margin:0 0 34px;max-width:62ch;">AI doesn't manage people &mdash; leaders do. Management in the age of AI is less about the tools and more about the questions: which decisions stay human, where judgment matters most, and how teams build trust while everything around them changes. That's the work we help leaders do.</p>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;">
        {pov_cols}
      </div>
    </div>
  </section>

  <section style="background:var(--bg);padding:96px 28px;">
    <div class="wrap" style="max-width:1100px;">
      {eb_ladder}
      <h2 class="h2-display" style="font-size:clamp(1.8rem,3.6vw,2.75rem);margin:14px 0 40px;max-width:22ch;">Own data. Organize insight. Act on intelligence.</h2>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px;">
        {ladder_cards}
      </div>
    </div>
  </section>

  {belief}
</div>""".format(
        eb=eyebrow("Our approach"),
        eb_gap=eyebrow("The gap we close", "var(--tw-yellow)"),
        eb_work=eyebrow("How we work"),
        eb_pov=eyebrow("Point of view", "var(--tw-yellow)"),
        eb_ladder=eyebrow("How capability compounds"),
        principle_cards=principle_cards,
        pov_cols=pov_cols,
        ladder_cards=ladder_cards,
        belief=belief_band(),
    )


# ---------------------------------------------------------------- ABOUT
def about_body():
    est_list = "".join(
        '<div style="display:flex;gap:10px;align-items:flex-start;font-weight:600;"><span style="color:var(--tw-red);">&#9656;</span>{t}</div>'.format(t=t)
        for t in ["Strategy &amp; digital maturity", "Technology transformation", "Security awareness", "Workforce development"]
    )
    return """<div>
  <div class="band" style="background:var(--tw-blue);padding:96px 28px 84px;overflow:hidden;">
    <img class="motif" src="/assets/elements/White-Donut.png" alt="" aria-hidden="true" style="right:-60px;bottom:-60px;width:500px;opacity:.5;">
    <div class="wrap" style="max-width:1100px;">
      {eb}
      <h1 class="hero-h1" style="font-size:clamp(2.4rem,5.5vw,4.5rem);line-height:.95;color:#fff;max-width:18ch;">A human capability company</h1>
      <p class="lead" style="color:rgba(255,255,255,.82);max-width:58ch;margin-top:22px;line-height:1.6;">Treadwell exists to increase human capability faster than technology increases complexity &mdash; turning research into practical intelligence and measurable action.</p>
    </div>
  </div>

  <section style="background:var(--bg);padding:88px 28px;">
    <div class="wrap" style="max-width:1100px;display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:48px;align-items:start;">
      <div>
        {eb_story}
        <h2 class="h2-display" style="font-size:clamp(1.8rem,3.6vw,2.75rem);line-height:1.02;margin:14px 0 22px;max-width:20ch;">Two decades of turning change into capability</h2>
        <p class="lead" style="margin:0 0 18px;color:var(--text-body);line-height:1.65;">Founded in 2011, Treadwell Agency has been a focused leader in strategy, technology transformation, and security awareness &mdash; helping organizations meet each wave of change with confidence rather than fear.</p>
        <p style="margin:0;color:var(--text-body);line-height:1.65;">What began as a strategy and security practice has grown into a human-first transformation agency for the age of AI. Through every shift, one thing has stayed constant: technology moves fast, but people determine whether change succeeds. Today we partner with corporations, institutions, and public agencies to prepare leaders, employees, and businesses for the future of work.</p>
      </div>
      <article class="tw-card tw-card--hard">
        <div style="font-family:var(--font-mono);font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--tw-blue);">Established</div>
        <div style="font-family:var(--font-display);font-weight:900;font-size:clamp(3.5rem,7vw,5rem);line-height:.9;letter-spacing:-.02em;margin:6px 0 20px;">2011</div>
        <div style="display:grid;gap:12px;">{est}</div>
      </article>
    </div>
  </section>

  {cta}
</div>""".format(
        eb=eyebrow("Who we are", "var(--tw-yellow)"),
        eb_story=eyebrow("Our story"),
        est=est_list,
        cta=cta_strip("Let's build your readiness", "", "Book a consultation", CTA_MAILTO, "accent"),
    )


# ================================================================== build
PAGES = [
    ("index.html", "", "home",
     "Treadwell Agency — We solve for the human factor",
     "Workforce & organization transformation for the age of AI. Treadwell prepares leaders, employees, and businesses for the future of work — starting with your outcomes, not the tools.",
     home_body),
    ("services/index.html", "/services/", "services",
     "Services — Treadwell Agency",
     "Outcomes first, tools second. Workforce readiness, organizational transformation, and AI strategy — closing the gap between how fast AI changes work and how fast your people adapt.",
     services_body),
    ("training/index.html", "/training/", "training",
     "Training — Treadwell Agency",
     "Practical, credential-aligned training for corporations: AI & digital-fluency courses, WIOA-funded workforce programs, and annual cybersecurity awareness training.",
     training_body),
    ("ai-readiness/index.html", "/ai-readiness/", "readiness",
     "AI Readiness — Treadwell Agency",
     "From experimentation to operating model. The See. Solve. Scale. methodology and the free AI Readiness Canvas — four ways to work with us, from advisor to enterprise engagement.",
     readiness_body),
    ("approach/index.html", "/approach/", "approach",
     "Approach — Treadwell Agency",
     "Human-first digital transformation. We grow human capability faster than technology increases complexity — people before tools, augment don't replace, outcomes before AI.",
     approach_body),
    ("about/index.html", "/about/", "about",
     "About — Treadwell Agency",
     "A human capability company. Founded in 2011, Treadwell Agency is a human-first transformation agency for the age of AI, partnering with corporations, institutions, and public agencies.",
     about_body),
]


def main():
    for rel, canon, active, title, desc, body_fn in PAGES:
        out = os.path.join(ROOT, rel)
        os.makedirs(os.path.dirname(out) or ROOT, exist_ok=True)
        html = page(active, title, desc, body_fn(), canon)
        with open(out, "w", encoding="utf-8") as f:
            f.write(html)
        print("wrote", rel)


if __name__ == "__main__":
    main()
