---
name: astra-header-footer-abilities
description: "How to configure the Astra theme's native header/footer builder, global colors/typography/buttons, and site identity entirely via PHP (Astra's own \"Abilities\" classes), on thamtapyogacaocap.com"
metadata: 
  node_type: memory
  type: reference
  originSessionId: baf300b8-3128-46bb-965a-c07eb2980c4e
  modified: 2026-08-28T08:06:11.000Z
---

Astra (this site: v4.13.10, no Astra Pro/addon) ships a full set of purpose-built PHP "ability" classes under `wp-content/themes/astra/inc/abilities/` — originally meant for the WP Abilities API / MCP layer, but they're just plain PHP classes with a `configure()` + `execute($args)` method, so they can be called directly without going through that layer. This is far more reliable than hand-writing `astra_update_option()` calls, because each class already knows the real option keys, expected shapes, and sane merge/sanitize behavior. Used for [[louis-yoga-elementor-build-project]]'s header/footer.

## Loading the classes
They're normally required by `inc/abilities/bootstrap.php`, but that bootstrap early-returns unless an admin dashboard toggle (`enable_abilities`) is on — which it isn't on this site, and toggling it wasn't asked for. Require the files directly instead (safe — no side effects beyond defining the classes):
```php
$dir = get_template_directory() . '/inc/abilities/';
require_once $dir . 'class-astra-abilities-response.php';
require_once $dir . 'class-astra-abstract-ability.php';
require_once $dir . 'class-astra-abilities-helper.php';
require_once $dir . '<specific-ability-file>.php';
```
Each class file's own `Class::register()` call at the bottom (which hooks into `wp_register_ability()`) is harmless to leave in — or just instantiate directly and skip register() entirely:
```php
$ability = new Astra_Update_Header_Builder();
$ability->configure();
$result = $ability->execute([ /* args per its get_input_schema() */ ]);
```
**Every ability class file lives under `inc/abilities/customizer/...` or `inc/abilities/admin/...`** — read the specific file for its exact `get_input_schema()`/`execute()` before calling; the descriptions embedded in `configure()` (`usage_hints` in `$this->meta`) are detailed and were written for exactly this kind of blind-call usage.

## Classes used so far (all confirmed working)
- `customizer/globals/colors/class-astra-update-global-palette.php` — 9-slot palette: `colors: {"0":hex, ..., "8":hex}` where 0=Primary, 1=Primary Hover, 2=Heading, 3=Text, 4=Background, 5=Secondary Background, 6=Border, 7=Secondary Border, 8=Accent. This is the single highest-leverage call — most default-inheriting theme styles (links, headings, borders) pick these up automatically.
- `customizer/globals/typography/class-astra-update-body-font.php` — `font_family: 'Nunito Sans'` (bare name; the class appends `, sans-serif` itself).
- `customizer/globals/typography/class-astra-update-heading-font.php` — one class handles H1–H6: `(new Astra_Update_Heading_Font())->set_level($n)` before `configure()`, then `execute(['font_family'=>'Playfair Display'])`. Loop 1–6.
- `customizer/globals/buttons/class-astra-update-global-buttons.php` — sitewide button style (affects Gutenberg/WooCommerce/etc. buttons), **NOT** the header/footer builder's own button components (those have separate per-component options — see below).
- `customizer/siteidentity/class-astra-update-site-title-logo.php` — `logo_id` (attachment id, preferred over `logo_url`). Also `display_site_title: {desktop,tablet,mobile: bool}` — **set all three false if the design's header shows only a logo mark**, since Astra's default is to show the site title text next to the logo (`logo-title-inline`), which visually collides with a wordmark logo.
- `customizer/header/class-astra-update-header-builder.php` — desktop/mobile zone placement, e.g. `{"desktop":{"primary":{"primary_left":["logo"],"primary_right":["menu-1","button-1"]}}, "mobile":{"primary":{"primary_left":["logo"],"primary_right":["mobile-trigger"]},"popup":{"popup_content":["mobile-menu","button-1"]}}}`. Smart-merges (a single new id appends; an existing subset removes the rest) — see the class's own extensive `usage_hints` before assuming placement semantics.
- `customizer/header/class-astra-update-header-builder-design.php` — per-section (`above`/`primary`/`below`) background/border-color/border-size/padding. Only the **bottom** border of the given header section (nothing separate for text/link colors — those live in different, non-abilitized options, see below).
- `customizer/footer/class-astra-update-footer-builder.php` / `...-footer-builder-design.php` — same pattern as header but with `above`/`primary`/`below` × 5 columns (`primary_1`..`primary_5` etc.) instead of 5-zone rows, plus `above_footer_columns`/`primary_footer_columns`/`below_footer_columns` (1–5) to control how many of those columns actually render. Design ability sets **top** border + background + padding per section (not text/link color, same gap as header).

## Gaps the abilities don't cover — set these `astra_update_option()` keys directly (verified working)
- **Header CTA button's own style** (as opposed to the sitewide global-buttons ability): `header-button1-text-color`, `header-button1-text-h-color`, `header-button1-back-color`, `header-button1-back-h-color`, `header-button1-border-color`, `header-button1-border-h-color`, `header-button1-border-size` (`{top,right,bottom,left}` strings, no unit), `header-button1-border-radius-fields` (`{desktop:{top,right,bottom,left}, desktop-unit, tablet:{...}, tablet-unit, mobile:{...}, mobile-unit}`), `header-button1-font-family`, `header-button1-font-weight`. Swap `button1`→`button2`/`button3` or `header`→`footer` for other button slots. No dedicated padding option exists for these per-component buttons on this Astra version — only border/radius/color/font.
- **Header button link**: `header-button1-link-option` = `['url'=>'/path/', 'new_tab'=>false, 'link_rel'=>'']` (plain array, not the `{"$$type":...}` pattern from Elementor — Astra is a completely separate system). `header-button1-text` = plain string for the label.
- **Footer widget-column text/link colors** (the "Advanced Footer" widget area's own text, as opposed to global palette): `footer-adv-wgt-title-color` (widget headings), `footer-adv-text-color` (body text), `footer-adv-link-color` (link normal), `footer-adv-link-h-color` (link hover).
- **Copyright bar**: `footer-copyright-editor` (raw text with placeholders `[copyright] [current_year] [site_title] [theme_author]` — do NOT include a literal "Copyright" word if you also use `©`, the placeholder system prepends its own "Copyright" label to a `[copyright]`-shortcode style output... actually simplest: just write the plain final text yourself, e.g. `'© [current_year] Louis Yoga. ...'`, no need for the `[copyright]` token) and `footer-copyright-color` (plain hex).

## Footer widget-column content (the "above footer" 4-column area)
`Astra_Update_Footer_Builder`'s `widget-1`..`widget-4` component ids correspond to WP sidebars literally named `footer-widget-1`..`footer-widget-4` (confirmed via `$wp_registered_sidebars` at runtime — **not** `advanced-footer-widget-N`, which is a same-named legacy/parallel registration that stays in `sidebars_widgets` unused when the header/footer *builder* — not the old classic footer — is active, as it is here). The sidebars only get registered once the builder layout actually references `widget-N` in a placed zone, so update the layout (`Astra_Update_Footer_Builder`) *before* trying to populate `$wp_registered_sidebars`.

Since this site's widget areas are block-based (`astra_has_widgets_block_editor()` → true), populate them as native "Widgets (block)" instances rather than classic widgets:
```php
$wb = get_option('widget_block', []);
$wb[$new_numeric_id] = [ 'content' => '<!-- wp:heading {"level":4} --><h4 class="wp-block-heading">Nội dung</h4><!-- /wp:heading --><!-- wp:list --><ul class="wp-block-list"><li><a href="/dich-vu/">...</a></li></ul><!-- /wp:list -->' ];
update_option('widget_block', $wb);
$sw = get_option('sidebars_widgets');
$sw['footer-widget-2'] = [ 'block-' . $new_numeric_id ];
update_option('sidebars_widgets', $sw);
```
Ordinary core blocks (`wp:heading`, `wp:paragraph`, `wp:list`, `wp:image`) automatically pick up whatever body/heading font and global palette were set above — no per-block styling needed for brand consistency.

## Core Gutenberg Search block button text wraps mid-word in the header widget area
The header search widget (`header-widget-1` → `widget_block` option id 10, a native `core/search` block with `buttonPosition:"button-outside"`, `width:311px`) had its "Tìm" button text visually splitting into "Ti"/"m" on two lines. Root cause (confirmed by DOM experiment, not guesswork): the button is a flex item with `flex-grow:0` inside `.wp-block-search__inside-wrapper` (flex, fixed total width), and the browser resolves its `flex-basis:auto` to a too-small size that permits the text to wrap — sweeping the wrapper's total width from 311px up to 416px changed the sibling `<input>` (flex-grow:1) by +100px but grew the button by under 2px each time, proving the button's own computed basis is pinned small regardless of available space; the button never expands to reclaim room since `flex-grow:0`. Confirmed fix by live DOM test: applying `white-space:nowrap` directly to `.wp-block-search__button` immediately made it single-line at a natural ~67px width, with no other layout regression. `core/search` block supports (`anchor:true`, confirmed via `WP_Block_Type_Registry`) do not expose a no-wrap toggle in its `style` schema (only border/color/typography/spacing-margin get serialized), so this can't be fixed by block attributes alone. **Fix applied:** gave the block's own JSON attributes an `"anchor":"site-search-widget"` (native support, renders `id="site-search-widget"` on the block wrapper) and appended one scoped `<style>#site-search-widget .wp-block-search__button{white-space:nowrap}</style>` tag directly inside that same widget's `content` string (sibling to the `<!-- wp:search ... /-->` comment, not a sitewide Additional-CSS edit) — `do_blocks()` on widget content passes raw HTML like this through untouched, same mechanism a Custom HTML block relies on. The header search widget renders twice in the DOM (desktop inline + the mobile popup menu's duplicate), so the `id` and the style both apply to both instances (technically a duplicate-id situation, harmless here since the CSS selector intentionally wants to match both). This is a good general fallback pattern for any future "the block editor doesn't have a control for X" case in a header/footer widget context (outside Elementor's atomic pages, where [[louis-yoga-elementor-build-project]]'s "no Additional CSS anywhere" rule applies instead).

## Verification gotchas
- **`astra_get_option()` caches its result statically per-request** (`Astra_Theme_Options::$db_options`). After writing an option inside a PHP call, re-reading it *in the same call* — including via an ability's own success-response echo — can show the stale pre-write value. This is not a bug in the write; always verify with a **separate** `execute-php` call (a fresh WP bootstrap) if a value looks wrong right after setting it.
- **Astra's custom button markup separates the clickable `<a>` from the styled node**: `<a class="ast-custom-button-link">…<div class="ast-custom-button">Label</div></a>`. `getComputedStyle()` on the `<a>` shows browser defaults (transparent bg, no radius); the real background/color/border/radius/font live on the inner `.ast-custom-button` div. Same trap will apply to any other Astra "button" component (footer button, etc.) — always drill into the actual styled child, not the outer link.
- After any of the above writes, force-refresh caches before checking the live page: `\Elementor\Plugin::$instance->files_manager->clear_cache();` (Elementor still renders the *page content*, so its cached CSS can reference stale `--ast-*` values) and `delete_option('astra_partials_config_cache');`. A plain `clear_cache()` alone was sometimes not enough to see a change on next load in this session.
