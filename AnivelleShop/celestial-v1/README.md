# AnivelleShop — one common full-page theme

All 10 pages now use the same reference-inspired layout, hero image, illustrated collection cards, five arrival previews, couture banner, navbar, and footer. Only the active section changes. The previous category copy and artwork remain available in content.json and the asset bundle.

## The one value to change

Open `common/anivelle-common.txt` (or its identical HTML version). On the first DIV, change only `active-home`:

```html
<div class="anv-celestial active-accessories" ...
```

Use `active-clothing` for Clothing, `active-accessories` for Accessories, and so on. Leave every other part of the code unchanged. The stylesheet controls the current-category glow, star underline, current-section accessibility label, and the Home/Collections highlight in the upper navbar.

| Section | Active class | Ready-to-paste file |
| --- | --- | --- |
| Home | active-home | embeds/anivelle-home.txt |
| Furniture | active-shop | embeds/anivelle-shop.txt |
| Rooms | active-rooms | embeds/anivelle-rooms.txt |
| Clothing | active-clothing | embeds/anivelle-clothing.txt |
| Accessories | active-accessories | embeds/anivelle-accessories.txt |
| Poses | active-avatar-poses | embeds/anivelle-avatar-poses.txt |
| Body | active-body | embeds/anivelle-body.txt |
| Pets | active-pets | embeds/anivelle-pets.txt |
| Cutouts | active-cutouts | embeds/anivelle-cutouts.txt |
| Creator Note | active-creator-only | embeds/anivelle-creator-only.txt |

Each matching HTML file contains the same complete code as its TXT version. All 10 fragments have been checked to differ **only in the root active class**. Paste the entire file into the IMVU HTML description editor. No individual product-page URLs or product IDs are needed.

The creator-only class additionally reveals the existing **DO NOT BUY / Not for sale** notice. The personal ribbon restriction is retained.

## Navigation destinations

- **Downloadable website:** open index.html. All 10 section links open the corresponding full themed page, which carries its own active state. The three collection illustrations also open their matching category page.
- **IMVU fragments:** links open Anivelle Studio's existing IMVU catalogue categories. Individual product-page links have been left out as requested. An HTML description cannot change IMVU's external catalogue page or automatically inject this theme there.
- Home, Furniture, Rooms, Clothing, Accessories, Poses, Body, Pets, Cutouts, and Creator Note appear together in the header category navbar.
- Collections and New Arrivals in the upper navbar jump to those sections of the same full page.

## IMVU compatibility

The snippets use basic HTML elements and scoped CSS. They contain no JavaScript, SVG, forms, iframes, external fonts, icon fonts, data URLs, container queries, cursor replacement, or page-header overrides. Visible symbols use numeric HTML entities; the IMVU stylesheet has no backslash star escapes. CSS animations are cosmetic and disabled by prefers-reduced-motion.

The IMVU compatibility patch keeps the logo, navigation labels, buttons, and every image card in ordinary DIV/SPAN/IMG elements, outside links. Links contain only plain text and use only href and target="_top" attributes. They are positioned over the corresponding visible element. This prevents a removed link block from also deleting the visual content. Regression checks deliberately remove every anchor and strip backslashes, then confirm that all artwork and essential labels remain. This models the screenshot's symptoms; it is not a claim that IMVU's exact save filter has been reproduced.

The hearts are decorative. The arrival illustrations say Style Preview and link to category listings; they do not claim real prices, stock, product IDs, or wishlist functionality. Nothing replaces IMVU's own purchasing controls.

Local markup, navigation, active-state, desktop, and narrow-screen checks are included. A live save through IMVU's HTML filter has not been tested.

## Files and rebuild

- index.html + pages/: the 10 linked full-page previews.
- common/: the reusable complete IMVU code.
- embeds/: 10 complete HTML/TXT copies with active classes already selected.
- celestial.css: shared stylesheet.
- assets/: 28 optimized WebP images, of which 11 are used by the common reference layout.
- originals/: all 28 generated PNG originals in the GitHub package.
- generation-prompts.json + reference-edition-prompts.json: prompts used with built-in image_gen.
- content.json: retained original category content.
- asset-manifest.json + validation.json: asset hashes and validation results.

To rebuild, run `python tools/build_anivelle.py`, then `python tools/validate_anivelle.py` from this folder (Python 3.12+). Validation follows all 100 local navbar links and checks that every destination has the correct active class.
