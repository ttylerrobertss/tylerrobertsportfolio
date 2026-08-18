import json, os, html

ROOT = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(ROOT, "data.json")) as f:
    data = json.load(f)
with open(os.path.join(ROOT, "manifest.json")) as f:
    manifest = json.load(f)

SITE_NAME = "tyler roberts - cinematographer"
FORMSPREE_ENDPOINT = "https://formspree.io/f/YOUR_FORM_ID"  # replace after creating a Formspree form

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
    <span>&copy; {SITE_NAME}</span>
  </footer>"""

def page(title, body, active, depth=0, extra_head=""):
    prefix = "../" * depth
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)} — {SITE_NAME}</title>
  <link rel="stylesheet" href="{prefix}assets/css/style.css">
  {extra_head}
</head>
<body>
  {header(active, depth)}
  {body}
  {footer(depth)}
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
    <div class="grid">
      {''.join(grid_items)}
    </div>
  </main>"""

with open(os.path.join(ROOT, "index.html"), "w") as f:
    f.write(page(SITE_NAME, home_body, "portfolio", depth=0))

# ---------- Project pages ----------
for p in data["projects"]:
    provider = p["provider"]
    video_id = p["videoId"]
    if provider == "youtube" and video_id:
        media = f"""<div class="video-wrap">
        <iframe src="https://www.youtube-nocookie.com/embed/{video_id}" title="{html.escape(p['title'])}" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen loading="lazy"></iframe>
      </div>"""
    elif provider == "vimeo" and video_id:
        media = f"""<div class="video-wrap">
        <iframe src="https://player.vimeo.com/video/{video_id}" title="{html.escape(p['title'])}" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen loading="lazy"></iframe>
      </div>"""
    else:
        media = '<div class="no-video"><span>Coming soon</span></div>'

    desc_html = html.escape(p["desc"]).replace("\n", "<br>") if p["desc"] else ""

    body = f"""<main class="wrap">
    <a class="back-link" href="../../index.html">&larr; back to portfolio</a>
    <div class="project">
      {media}
      <div>
        <h1>{html.escape(p['title'])}</h1>
        <div class="desc">{desc_html}</div>
      </div>
    </div>
  </main>"""

    outdir = os.path.join(ROOT, "portfolio", p["slug"])
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "index.html"), "w") as f:
        f.write(page(p["title"], body, "portfolio", depth=2))

# ---------- BTS page ----------
bts_imgs = []
for fname in manifest["bts"]:
    bts_imgs.append(f'<img src="../assets/img/bts/{fname}" alt="behind the scenes" loading="lazy">')

bts_body = f"""<main class="wrap">
    <div class="bts-grid">
      {''.join(bts_imgs)}
    </div>
  </main>"""

os.makedirs(os.path.join(ROOT, "bts"), exist_ok=True)
with open(os.path.join(ROOT, "bts", "index.html"), "w") as f:
    f.write(page("BTS", bts_body, "bts", depth=1))

# ---------- Contact page ----------
bio_html = html.escape(data["contact"]["bio"])
headshot = manifest["headshot"]

contact_body = f"""<main class="wrap">
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

os.makedirs(os.path.join(ROOT, "contact"), exist_ok=True)
with open(os.path.join(ROOT, "contact", "index.html"), "w") as f:
    f.write(page("Contact", contact_body, "contact", depth=1))

print("Build complete.")
