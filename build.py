import json, os, html

ROOT = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(ROOT, "data.json")) as f:
    data = json.load(f)
with open(os.path.join(ROOT, "manifest.json")) as f:
    manifest = json.load(f)

SITE_NAME = "tyler roberts - cinematographer"
FORMSPREE_ENDPOINT = "https://formspree.io/f/mqpzggzw"
BASE_URL = "https://tylerrobertsportfolio.com"
DEFAULT_DESCRIPTION = (
    "Tyler Roberts is a Cincinnati, OH-based cinematographer and Director of "
    "Photography specializing in 16mm and 35mm motion picture film, plus Super 8 "
    "and digital cinema — shooting commercials, music videos, and narrative film, "
    "available for productions worldwide."
)

def header(active, depth=0):
    prefix = "../" * depth
    def link(href, label, key):
        cls = ' class="active"' if key == active else ""
        return f'<a href="{prefix}{href}"{cls}>{label}</a>'
    return f"""<header class="site-header wrap">
    <a class="logo" href="{prefix}index.html">{SITE_NAME}</a>
    <nav class="site-nav">
      {link("index.html", "portfolio", "portfolio")}
      {link("bts/index.html", "bts", "bts")}
      {link("contact/index.html", "contact", "contact")}
    </nav>
  </header>"""

def footer(depth=0):
    return f"""<footer class="site-footer wrap">
    <a class="footer-instagram" href="https://instagram.com/ttylerrobertss" target="_blank" rel="noopener noreferrer" aria-label="Instagram">
      <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.4" cy="6.6" r="1.1" fill="currentColor" stroke="none"/></svg>
    </a>
    <span>&copy; {SITE_NAME}</span>
  </footer>"""

def page(title, body, active, depth=0, extra_head="", show_footer=False,
         description=DEFAULT_DESCRIPTION, canonical_path="", og_image="assets/img/thumbs/reel.webp",
         title_is_full=False):
    prefix = "../" * depth
    footer_html = footer(depth) if show_footer else ""
    full_title = html.escape(title) if title_is_full else f"{html.escape(title)} — {SITE_NAME}"
    desc_attr = html.escape(" ".join(description.split()))
    canonical_url = f"{BASE_URL}/{canonical_path}"
    og_image_url = f"{BASE_URL}/{og_image}"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{full_title}</title>
  <meta name="description" content="{desc_attr}">
  <link rel="canonical" href="{canonical_url}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{full_title}">
  <meta property="og:description" content="{desc_attr}">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:image" content="{og_image_url}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{full_title}">
  <meta name="twitter:description" content="{desc_attr}">
  <meta name="twitter:image" content="{og_image_url}">
  <link rel="stylesheet" href="{prefix}assets/css/style.css">
  {extra_head}
</head>
<body>
  {header(active, depth)}
  {body}
  {footer_html}
  <script src="{prefix}assets/js/main.js"></script>
</body>
</html>
"""

# ---------- Home page ----------
grid_items = []
for p in data["projects"]:
    thumb = manifest["thumbs"].get(p["slug"])
    img_tag = f'<img src="assets/img/thumbs/{thumb}" alt="{html.escape(p["title"])}" loading="lazy">' if thumb else ""
    grid_items.append(f"""<a class="grid-item" href="portfolio/{p['slug']}/index.html">
        {img_tag}
        <div class="caption">{html.escape(p['title'])}</div>
      </a>""")

home_body = f"""<main class="wrap">
    <h1 class="sr-only">Tyler Roberts — Cincinnati 16mm &amp; 35mm Film Cinematographer / Director of Photography</h1>
    <p class="tagline">16mm &amp; 35mm motion picture film &middot; Super 8 &middot; digital — Cincinnati, available worldwide</p>
    <div class="grid">
      {''.join(grid_items)}
    </div>
  </main>"""

person_jsonld = f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Tyler Roberts",
  "jobTitle": "Cinematographer / Director of Photography",
  "url": "{BASE_URL}/",
  "image": "{BASE_URL}/assets/img/headshot/{manifest['headshot']}",
  "sameAs": [
    "https://instagram.com/ttylerrobertss"
  ],
  "address": {{
    "@type": "PostalAddress",
    "addressLocality": "Cincinnati",
    "addressRegion": "OH",
    "addressCountry": "US"
  }},
  "knowsAbout": [
    "16mm film",
    "35mm film",
    "Super 8 film",
    "Motion picture film cinematography",
    "Digital cinematography"
  ],
  "description": "{html.escape(' '.join(DEFAULT_DESCRIPTION.split()))}"
}}
</script>"""

google_site_verification = '<meta name="google-site-verification" content="du7SJo6n_VMNp4xpUbpNSIbhMdOM1YZzss6qNg08VrA" />'

with open(os.path.join(ROOT, "index.html"), "w") as f:
    f.write(page(
        "Tyler Roberts | Cincinnati 16mm/35mm Film Cinematographer",
        home_body, "portfolio", depth=0, show_footer=True, title_is_full=True,
        description=DEFAULT_DESCRIPTION, canonical_path="",
        extra_head=google_site_verification + person_jsonld,
    ))

# ---------- Project pages ----------
def video_embed(video, title):
    provider, video_id = video["provider"], video["id"]
    if provider == "youtube":
        src = f"https://www.youtube-nocookie.com/embed/{video_id}"
    elif provider == "vimeo":
        src = f"https://player.vimeo.com/video/{video_id}"
        if video.get("hash"):
            src += f"?h={video['hash']}"
    else:
        return ""
    return f"""<div class="video-wrap">
        <iframe src="{src}" title="{html.escape(title)}" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen loading="lazy"></iframe>
      </div>"""

for p in data["projects"]:
    videos = p.get("videos", [])
    gallery = manifest.get("gallery", {}).get(p["slug"], [])

    if len(videos) == 0:
        media = '<div class="no-video"><span>Coming soon</span></div>'
    elif len(videos) == 1:
        media = video_embed(videos[0], p["title"])
    else:
        embeds = "".join(video_embed(v, p["title"]) for v in videos)
        multi_cls = "video-multi video-vertical" if p.get("video_aspect") == "9:16" else "video-multi"
        media = f'<div class="{multi_cls}">{embeds}</div>'

    desc_html = html.escape(p["desc"]).replace("\n", "<br>") if p["desc"] else ""

    formats = p.get("film_formats", [])
    if len(formats) == 0:
        format_str = ""
    elif len(formats) == 1:
        format_str = formats[0]
    else:
        format_str = " & ".join([", ".join(formats[:-1]), formats[-1]]) if len(formats) > 2 else " & ".join(formats)
    format_tag_html = f'<p class="format-tag">Shot on {html.escape(format_str)} film</p>' if format_str else ""

    gallery_html = ""
    if gallery:
        gallery_imgs = "".join(
            f'<img src="../../assets/img/gallery/{p["slug"]}/{fname}" alt="{html.escape(p["title"])}" loading="lazy">'
            for fname in gallery
        )
        gallery_html = f'<div class="project-gallery">{gallery_imgs}</div>'

    body = f"""<main class="wrap">
    <a class="back-link" href="../../index.html">&larr; back to portfolio</a>
    <div class="project">
      {media}
      <div>
        <h1>{html.escape(p['title'])}</h1>
        {format_tag_html}
        <div class="desc">{desc_html}</div>
      </div>
    </div>
    {gallery_html}
  </main>"""

    if format_str:
        project_desc = (
            f"{p['title']} — cinematography by Tyler Roberts, shot on {format_str} film. "
            f"Cincinnati-based Director of Photography available for productions worldwide."
        )
    else:
        project_desc = (
            f"{p['title']} — cinematography by Tyler Roberts, a Cincinnati-based "
            f"Director of Photography available for productions worldwide."
        )
    project_thumb = manifest["thumbs"].get(p["slug"])
    og_image = f"assets/img/thumbs/{project_thumb}" if project_thumb else "assets/img/thumbs/reel.webp"

    outdir = os.path.join(ROOT, "portfolio", p["slug"])
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "index.html"), "w") as f:
        f.write(page(
            p["title"], body, "portfolio", depth=2,
            description=project_desc, canonical_path=f"portfolio/{p['slug']}/", og_image=og_image,
        ))

# ---------- BTS page ----------
bts_imgs = []
for fname in manifest["bts"]:
    bts_imgs.append(f'<img src="../assets/img/bts/{fname}" alt="behind the scenes" loading="lazy">')

bts_body = f"""<main class="wrap">
    <h1 class="sr-only">Behind the Scenes — Tyler Roberts, Cincinnati Cinematographer</h1>
    <div class="bts-grid">
      {''.join(bts_imgs)}
    </div>
  </main>"""

bts_desc = "Behind-the-scenes photos from Tyler Roberts' film, commercial, and live production work."
bts_thumb = manifest["thumbs"].get("bts")
bts_og_image = f"assets/img/thumbs/{bts_thumb}" if bts_thumb else "assets/img/thumbs/reel.webp"

os.makedirs(os.path.join(ROOT, "bts"), exist_ok=True)
with open(os.path.join(ROOT, "bts", "index.html"), "w") as f:
    f.write(page(
        "BTS", bts_body, "bts", depth=1,
        description=bts_desc, canonical_path="bts/", og_image=bts_og_image,
    ))

# ---------- Contact page ----------
bio_html = html.escape(data["contact"]["bio"])
headshot = manifest["headshot"]

contact_body = f"""<main class="wrap">
    <h1 class="sr-only">Contact Tyler Roberts — Cincinnati Cinematographer &amp; Director of Photography</h1>
    <div class="contact">
      <div class="headshot">
        <img src="../assets/img/headshot/{headshot}" alt="Tyler Roberts">
      </div>
      <div>
        <p class="bio">{bio_html}</p>
        <form action="{FORMSPREE_ENDPOINT}" method="POST">
          <div class="name-row">
            <div>
              <label for="first">first name</label>
              <input id="first" name="first_name" type="text" required>
            </div>
            <div>
              <label for="last">last name</label>
              <input id="last" name="last_name" type="text" required>
            </div>
          </div>
          <div>
            <label for="email">email</label>
            <input id="email" name="email" type="email" required>
          </div>
          <div>
            <label for="message">message</label>
            <textarea id="message" name="message" required></textarea>
          </div>
          <button type="submit">send</button>
        </form>
        <p class="form-note">Prefer email? Reach out directly at <a href="mailto:tylerrobertscontact@gmail.com">tylerrobertscontact@gmail.com</a></p>
      </div>
    </div>
  </main>"""

contact_desc = (
    "Contact Tyler Roberts, a Cincinnati, OH-based Director of Photography "
    "and cinematographer available for productions worldwide."
)

os.makedirs(os.path.join(ROOT, "contact"), exist_ok=True)
with open(os.path.join(ROOT, "contact", "index.html"), "w") as f:
    f.write(page(
        "Contact", contact_body, "contact", depth=1,
        description=contact_desc, canonical_path="contact/",
        og_image=f"assets/img/headshot/{headshot}",
    ))

# ---------- sitemap.xml + robots.txt ----------
sitemap_paths = ["", "bts/", "contact/"] + [f"portfolio/{p['slug']}/" for p in data["projects"]]
sitemap_urls = "\n".join(
    f"  <url><loc>{BASE_URL}/{path}</loc></url>" for path in sitemap_paths
)
sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{sitemap_urls}
</urlset>
"""
with open(os.path.join(ROOT, "sitemap.xml"), "w") as f:
    f.write(sitemap_xml)

robots_txt = f"""User-agent: *
Allow: /

Sitemap: {BASE_URL}/sitemap.xml
"""
with open(os.path.join(ROOT, "robots.txt"), "w") as f:
    f.write(robots_txt)

print("Build complete.")
