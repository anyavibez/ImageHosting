# AnivelleShop — The Celestial Atelier

Reference-matching celestial anime theme for Anivelle Studio's IMVU descriptions: a large blonde anime hero, ornamental rose-gold frames, three wide illustrated collection cards, five arrival-style cards, silk ribbons, stars, and a celestial couture banner.

## Open the shop

Open `index.html` in a browser. The boutique landing page plus nine collection/creator pages make **10 pages**. The website uses local artwork, needs no package installation, and works without JavaScript. Collection links open matching themed pages; purchases happen in the existing IMVU catalogue.

For an HTTP preview, run `python -m http.server 8766 --bind 127.0.0.1` from this folder and open `http://127.0.0.1:8766/`.

## IMVU product description editor

Copy the **entire contents** of the matching file in `embeds/` into the IMVU HTML editor. The `.html` and `.txt` files contain identical paste-ready code: scoped inline CSS, accessible HTML, and absolute GitHub-hosted image URLs. Each file works independently without a stylesheet upload or scripts. Do not paste the standalone `pages/` versions into a product editor.

| Collection | Standalone page | Paste-ready HTML |
| --- | --- | --- |
| Boutique home | `index.html` | `embeds/anivelle-home.html` |
| Furniture / main shop | `pages/anivelle-shop.html` | `embeds/anivelle-shop.html` |
| Rooms | `pages/anivelle-rooms.html` | `embeds/anivelle-rooms.html` |
| Clothing | `pages/anivelle-clothing.html` | `embeds/anivelle-clothing.html` |
| Accessories | `pages/anivelle-accessories.html` | `embeds/anivelle-accessories.html` |
| Avatars & poses | `pages/anivelle-avatar-poses.html` | `embeds/anivelle-avatar-poses.html` |
| Body | `pages/anivelle-body.html` | `embeds/anivelle-body.html` |
| Pets | `pages/anivelle-pets.html` | `embeds/anivelle-pets.html` |
| Cutouts | `pages/anivelle-cutouts.html` | `embeds/anivelle-cutouts.html` |
| Creator-only note | `pages/anivelle-creator-only.html` | `embeds/anivelle-creator-only.html` |

The creator-only ribbon remains prominently marked **DO NOT BUY / Not for sale**. Category navigation in the embeds goes directly to Anivelle Studio's original IMVU catalogue categories; the standalone site links to the local theme pages. All unique catalogue URLs from the prior backup are retained in the catalogue directory.

## IMVU description compatibility

All **10 HTML fragments** have matching `.txt` versions. Their symbols are numeric HTML entities in ASCII files: stars `&#10022;` / `&#10023;`, hearts `&#9825;`, decorative flourishes `&#10087;`, and the copyright symbol `&#169;`. CSS-generated star symbols use CSS escapes. Search and catalogue icons are small CSS shapes that link to the actual IMVU catalogue.

The fragments use only basic HTML elements and scoped CSS. They contain **no JavaScript, SVG, iframe, forms, inputs, icon fonts, external fonts, or data URLs**. They do not change IMVU's surrounding page header or cursor. The layout uses percentage widths, ordinary flex layout, and media queries; it does not require container queries or container-relative units. Animations are optional cosmetic CSS effects, with a static reduced-motion presentation.

The arrival illustrations are marked **Style Preview** and link to the relevant live catalogue category. They do not claim actual product IDs, prices, stock, or purchase functionality. The heart is decorative, not a fake wishlist button.

IMVU documents [custom HTML on product pages](https://create.imvu.com/articles/classic/upload-a-product-product-page/) and [using its HTML description editor](https://avatars.imvu.com/shop/includes/iframe_product_description.php?products_id=8733074). Those sources do not publish a complete current CSS/tag allowlist. Local HTML validation and browser checks are complete; the actual live IMVU save/filter has not been exercised. Preview a pasted description in the target product editor before publishing.

## Artwork

There are **28 separately generated original artwork files**. The first 18 cover the nine collection/creator hero scenes, eight square collection illustrations, and an editorial atelier banner. This reference edition adds 10: a closer boutique hero, three wide featured-collection illustrations, five arrival-style illustrations, and a silk background. The same original adult blonde heroine appears in the character illustrations. These are decorative collection illustrations, not photographs of specific IMVU inventory items.

- `assets/`: optimized WebP files used by the theme.
- `originals/`: full-resolution generated PNGs in the GitHub asset package.
- `asset-manifest.json`: dimensions, file sizes, direct hosted URLs, and SHA-256 hashes.
- `generation-prompts.json`: the final prompt for every image. All were created with built-in `image_gen`, using the selected celestial concept as a style reference.
- `reference-edition-prompts.json`: the 10 new prompts for the closer reference edition, also created with built-in `image_gen`.

Direct image URL pattern:

```text
https://raw.githubusercontent.com/anyavibez/ImageHosting/main/AnivelleShop/celestial-v1/assets/home-hero.webp
```

No stock watermark was removed. The selected reference's composition was not republished as a flattened webpage. Text, buttons, menus, content cards, and effects are actual HTML/CSS.

## Edit and rebuild

Edit `celestial.css` for the visual theme and `content.json` for collection copy. Run `python tools/build_anivelle.py`, then `python tools/validate_anivelle.py` from this folder to rebuild all pages and embeds and check asset integrity, content preservation, HTML structure, and local links. Python 3.12 or later is required for the builder. The website itself only needs a modern browser.

The theme includes animated twinkles, a floating ribbon edge, glowing accents, button/card sheens, keyboard focus styling, lazy-loaded artwork, and narrow-screen layouts. `prefers-reduced-motion` disables the animations. No external font service, cursor takeover, or JavaScript dependency is required.

The files are ready to paste into IMVU; updating a live IMVU product description remains separate from publishing this GitHub asset package.
