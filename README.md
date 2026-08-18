# tylerrobertsportfolio.com

Tyler Roberts' cinematography portfolio — static site, rebuilt from the original Squarespace site and deployed via GitHub Pages.

## Structure

- `index.html` — portfolio grid (home page)
- `portfolio/<slug>/` — individual project pages (video embed + credits)
- `bts/` — behind-the-scenes photo gallery
- `contact/` — bio + contact form
- `assets/` — CSS, JS, images
- `data.json` / `manifest.json` — source data used by `build.py` to generate the HTML pages
- `build.py` — regenerates all HTML pages from `data.json` + `manifest.json`

## Editing content

Edit `data.json` (titles, descriptions, video IDs) or `manifest.json` (image filenames), then rebuild:

```bash
python3 build.py
```

## Contact form

The form on the Contact page posts to Formspree. Set your endpoint in `build.py`
(`FORMSPREE_ENDPOINT`), then re-run `python3 build.py`.

## Custom domain

This repo is served via GitHub Pages with the `CNAME` file pointing to
`tylerrobertsportfolio.com`. DNS must point at GitHub Pages — see repo owner's
notes for the exact records.
