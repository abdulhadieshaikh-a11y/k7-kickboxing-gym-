# K7 Kickboxing Gym — Website

A fast, dependency-free static website (9 pages). Run it locally with `npm install` followed by `npm run dev`, or open `index.html` in a browser. Upload the whole folder to any host (Netlify, Vercel, cPanel, GitHub Pages).

The development server runs at `http://localhost:3000` by default. Set the `PORT` environment variable to use a different port if 3000 is occupied.

## Pages
index.html (Home) · about.html · programs.html · combat.html (Kickboxing & MMA) · fitness.html · kids.html · female-only.html · enquire.html (Membership / Enquire) · contact.html

## Before going live — checklist
1. **Photos.** The site currently uses free Unsplash stock photos as placeholders (shown in black & white). If any photo fails to load, a matching dark K7 placeholder from `assets/images/fallback/` appears automatically, so nothing ever shows broken. Replace them with real K7 photos:
   - put your photos in `assets/images/` (e.g. `hero.jpg`, `kickboxing.jpg`)
   - in `_source/build.py`, change the matching entry in `IMAGES` to the file path, e.g. `"hero": ("assets/images/hero.jpg", "Alt text")`
   - run `python3 _source/build.py` to regenerate all pages.
2. **Logo.** No logo file was supplied, so the header uses a typographic K7 mark. Search for `LOGO:` in `_source/build.py` and swap in the original logo image, then rebuild.
3. **Enquiry form.** Open `assets/js/main.js` and set `FORM_ENDPOINT` (e.g. a Formspree URL) so enquiries arrive by email. Until then, the form validates, then prepares the enquiry as a pre-filled WhatsApp message to 0348 2136361 plus a call button. Confirm that number is on WhatsApp.
4. **Domain / SEO.** Set `SITE_URL` in `_source/build.py` and rebuild. This adds canonical URLs, `og:url` and generates `sitemap.xml`.
5. **Placeholder content.** The About page ("Our story", "Coaching team") and Enquire page ("Membership & pricing") contain clearly marked content slots. Search for `EDIT:` in `_source/build.py`.

## What's included
- Local business structured data (schema.org ExerciseGym) with address, phone and hours on every page
- Live "Open now / Closed" status using Karachi time
- Click-to-call, Google Maps directions and an embedded map (no API key needed)
- Enquiry pre-selection via URL, e.g. `enquire.html?program=Kids%20Kickboxing`
- Keyboard navigation, visible focus, skip link, accessible form errors, reduced-motion support
- Clean URLs on Netlify/Vercel (config included) and Apache (`.htaccess`)

Editing: all content lives in `_source/build.py`; styles in `assets/css/styles.css`; behaviour in `assets/js/main.js`.
