# AnivelleShop — one common full-page theme

## Single-file page switching candidate

`single-file/anivelle-imvu-tabs.html` (and its identical TXT version) includes all ten sections in one HTML description. Its category labels toggle radio controls; CSS `:checked` selectors show the matching section and active highlight without navigation or JavaScript. `single-file/preview.html` is the browser preview. All ten tabs were clicked and verified to show exactly one matching section while the URL stayed unchanged.

This version requires IMVU to retain INPUT type=radio, LABEL/for attributes, and the relevant CSS selectors. Its behavior after a live IMVU save is **not verified**. It is provided separately from the simple-link edition below. Rebuild it with `python tools/build_anivelle_tabs.py`.

All 10 pages use the same reference-inspired layout, hero image, illustrated collection cards, floating Celestial Edit art gallery, couture banner, navbar, and footer. Only the active section changes. New Arrivals and Explore Collection have been removed. Their five images are reused in the decorative gallery. The previous category copy and artwork remain available in content.json and the asset bundle.

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

## Enhanced single-file edition

Use `single-file/anivelle-imvu-tabs.txt` for the complete ten-panel description in one file. Rebuild it with `python tools/build_anivelle_tabs.py` (which calls `build_anivelle_hash.py`). Ordinary hash links with `target="_self"` replace the radio/label technique that failed in the supplied saved-page screenshots. The links stay within the description frame; CSS `:target` selects the panel and active navbar box. No JavaScript or product-page URLs are used.

This edition has ten rounded navbar boxes, uniform editorial gallery cards, a solid framed Copyright & DMCA panel, hover effects, and glowing star dividers. Essential visual styles are inline, and the smaller interaction stylesheet is placed first. Celestial Couture has Clothing and Accessories section links. The tagline remains “Your world. Your style.” The broken Discover the Look control is removed.

All ten section links, active states and both couture controls were verified in a browser preview, with desktop and 390-pixel layouts checked. IMVU must preserve fragment links, IDs, and `:target` sibling selectors on save; this revised technique has not been verified through its live save filter. If the whole stylesheet is removed, all sections remain visible. The older catalogue-link edition below is retained separately.

## Navigation destinations

- **Downloadable website:** open index.html. All 10 section links open the corresponding full themed page, which carries its own active state. The three collection illustrations also open their matching category page.
- **IMVU fragments:** links open Anivelle Studio's existing IMVU catalogue categories. Individual product-page links have been left out as requested. An HTML description cannot change IMVU's external catalogue page or automatically inject this theme there.
- Home, Furniture, Rooms, Clothing, Accessories, Poses, Body, Pets, Cutouts, and Creator Note appear together in the header category navbar.
- Collections in the downloadable website jumps to its collection section. In the IMVU fragment it opens the catalogue. There is no New Arrivals navigation item or Explore Collection button.

## IMVU compatibility

The snippets use basic HTML elements and scoped CSS. They contain no JavaScript, SVG, forms, iframes, external fonts, icon fonts, data URLs, container queries, or page-header overrides. Visible symbols use numeric HTML entities; the IMVU stylesheet has no backslash star escapes. CSS animations are cosmetic and disabled by prefers-reduced-motion.

The IMVU compatibility patch keeps the logo, navigation labels, buttons, and every image card in ordinary DIV/SPAN/IMG elements, outside links. Links contain only plain text and use only href and target="_top" attributes. The IMVU edition has visible Open, View Collection, Search, Shop, and Open Shop links; it does not hide clickable text behind transparent overlays. If IMVU removes a link, its surrounding image and label remain visible. Regression checks deliberately remove every anchor and strip backslashes, then confirm that all artwork and essential labels remain. This models the screenshot's symptoms; it is not a claim that IMVU's exact save filter has been reproduced.

The Accessories Open button was clicked in a browser test and opened Anivelle Studio's real IMVU Accessories catalogue. This confirms the generated link's destination before IMVU processes a pasted description. CSS cannot restore a hyperlink if the platform removes its anchor tag.

## Animation and cursor

The theme has floating gallery frames, breathing hero artwork, sparkling accents, moving silk, button sheen, lift and press effects, collection-card tilt, glow, and keyboard focus effects. Reduced-motion preferences disable animation. The two small code-drawn 32×32 PNG star cursors are in assets/; ui-assets.json records their hashes. Normal auto/pointer cursors are fallbacks when the browser or IMVU does not allow the custom image. There is no JavaScript cursor follower.

IMVU's [homepage guidance](https://support.imvu.com/support/solutions/articles/154000196786-faq-about-homepages) documents target="_top" for leaving a frame. [MDN's cursor reference](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/cursor) describes image cursors and their fallback keywords.

The Celestial Edit gallery is decorative. It does not claim real prices, stock, product IDs, or wishlist functionality. Nothing replaces IMVU's own purchasing controls.

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
