---
name: elementor-v4-atomic-json-schema
description: "Working PHP recipes for creating Elementor v4 atomic-widgets global variables, global classes, and page element trees directly via PHP (no REST) on thamtapyogacaocap.com"
metadata: 
  node_type: memory
  type: reference
  originSessionId: baf300b8-3128-46bb-965a-c07eb2980c4e
  modified: 2026-08-26T06:28:11.772Z
---

Reverse-engineered by reading the Elementor 4.2.3 plugin source directly (`wp-content/plugins/elementor/modules/variables/`, `.../global-classes/`, `.../atomic-widgets/`) and confirmed working end-to-end in-browser (styles, images, links, responsive all verified) for [[louis-yoga-elementor-build-project]]. All of this runs via Novamira's `novamira/execute-php` ability, in plain PHP with no `<?php` tag, `return`-ing a value to see the result.

## Why not REST
`rest_do_request()` against `/wp-json/elementor/v1/...` from inside `execute-php` gets rejected with 403 `rest_oauth_route_forbidden` — the Novamira OAuth connection isn't allowlisted for those routes. Everything below calls the same internal PHP classes the REST controllers call, directly.

## Global variables (Color + Font only — see project note on why Size doesn't work)
```php
use Elementor\Modules\Variables\Storage\Variables_Repository;
use Elementor\Modules\Variables\Services\Variables_Service;
use Elementor\Modules\Variables\Services\Batch_Operations\Batch_Processor;
use Elementor\Plugin;

$repository = new Variables_Repository( Plugin::$instance->kits_manager->get_active_kit() );
$service = new Variables_Service( $repository, new Batch_Processor() );
$service->create([ 'type' => 'global-color-variable', 'label' => 'c-primary', 'value' => '#918e35' ]);
$service->create([ 'type' => 'global-font-variable', 'label' => 'font-body', 'value' => 'Nunito Sans, Helvetica Neue, sans-serif' ]);
```
Label rules (enforced): no spaces, ≤50 chars, unique. `$service->delete($id)` soft-deletes (still occupies the label-uniqueness slot). Types that DO work end-to-end: `global-color-variable`, `global-font-variable`. Do not use `global-size-variable` (silently dropped for non-Pro sites) or `global-custom-size-variable` (survives storage but has no CSS-render transformer registered — never shows up in output CSS).

## Referencing a variable from a style/setting prop
A color prop pointing at a variable: `['$$type' => 'global-color-variable', 'value' => '<variable-id>']` (used anywhere a plain `{'$$type':'color','value':'#hex'}` would go, including nested inside `background.value.color`). A font-family prop pointing at a variable: `['$$type' => 'global-font-variable', 'value' => '<variable-id>']`.

## Global classes
```php
use Elementor\Modules\GlobalClasses\Global_Classes_Repository;
use Elementor\Plugin;

$repo = Global_Classes_Repository::make( Plugin::$instance->kits_manager->get_active_kit() );
$existing = $repo->all();
$items = $existing->get_items()->all();          // assoc array, id => item
$order = $existing->get_order()->all();          // plain array of ids (Collection objects — call ->all())

$id = 'e-gc-' . substr( md5( 'louis-yoga-' . $label ), 0, 10 ); // deterministic id per label; reuse this scheme for new classes too
$items[$id] = [
  'id' => $id, 'type' => 'class', 'label' => $label, // label = the literal CSS classname used in the rendered HTML
  'variants' => [
    [ 'meta' => ['breakpoint' => 'desktop', 'state' => null], 'props' => [ /* ... */ ] ],
    [ 'meta' => ['breakpoint' => 'tablet',  'state' => null], 'props' => [ /* only the props that differ */ ] ],
    [ 'meta' => ['breakpoint' => 'mobile',  'state' => null], 'props' => [ /* only the props that differ */ ] ],
  ],
];
$order[] = $id; // if new
$repo->put( $items, $order ); // NOTE: bypasses Global_Classes_Parser validation entirely — get the prop shapes right by hand (see below)
```
Active breakpoints on this site: `desktop` (implicit/base), `tablet` (max 1024px), `mobile` (max 767px) — matches the source design's 3 breakpoints exactly, no custom breakpoints needed. Label constraints: 2–50 chars, no spaces, can't start with a digit or `-<digit>`, can't be `container`, can't contain `--`.

### Style prop value shapes (confirmed via `SomePropType::generate()` and live render)
- String: `['$$type'=>'string','value'=>'flex']`
- Size: `['$$type'=>'size','value'=>['size'=>24,'unit'=>'px']]`
- Number: `['$$type'=>'number','value'=>1]`
- Color: `['$$type'=>'color','value'=>'#hex']` (or `'transparent'`)
- Dimensions (padding/margin, 4-sided): `['$$type'=>'dimensions','value'=>['block-start'=>SIZE,'inline-end'=>SIZE,'block-end'=>SIZE,'inline-start'=>SIZE]]`
- Border-radius uniform: just a plain Size works (schema unions `Border_Radius_Prop_Type` with plain `Size_Prop_Type`) — no need for the 4-corner `border-radius-v2` shape unless corners differ.
- Background solid color: `['$$type'=>'background','value'=>['color'=>COLOR_OR_VARIABLE]]`
- Flex shorthand: `['$$type'=>'flex','value'=>['flexGrow'=>NUMBER,'flexShrink'=>NUMBER,'flexBasis'=>SIZE]]` — **field names are camelCase** (`flexGrow`/`flexShrink`/`flexBasis`), not `grow`/`shrink`/`basis`. Using the wrong keys doesn't error (`generate()` doesn't validate nested shape, same trap as the image/link ones below) — it just silently produces no `flex` CSS output at all, so every flex-item class (cards, `col-copy`/`col-media`, etc.) falls back to `flex-basis:auto` with `flex-grow:0`, but because every `.e-con`-based element also gets an unconditional `width:100%` from Elementor's own base CSS, each "column" ends up claiming the full container width and the whole row-split/card-grid **stacks vertically as if it were `display:block`** instead of sitting side by side — easy to misread as a "layout doesn't match the design" complaint rather than a single wrong-key bug. Caught this on Home's `col-copy`, `col-media`, `card-service`, `card-article`, `card-product`, `mark` — check any new flex-basis-bearing class against this key spelling before shipping.
- State variants (`:hover`, `:focus`, etc.) work exactly like breakpoint variants — just add another entry to the class's `variants` array with `'meta'=>['breakpoint'=>'desktop','state'=>'hover']` (states: `hover`, `active`, `focus`, `focus-visible`, `checked`, `e--selected`, `e--disabled`, from `Style_States`). Elementor automatically pairs a `:hover` rule with `:focus-visible` too (free accessibility win, not something to add manually).
- Font-family: `['$$type'=>'font-family','value'=>'Playfair Display, Georgia, serif']` (comma list, no manual quoting) — or a global-font-variable ref.
- **Border needs `border-style` set explicitly** (e.g. `STR('solid')`) or `border-width`/`border-color` render invisibly (CSS default `border-style: none`).
- **No per-edge border** exists in the schema (only one uniform border-width/color/style for all 4 sides) — flag to user if source design needs e.g. `border-bottom` only.
- **`line-height` needs a font-size-relative unit, never `'px'`.** `SZ($ratio)` defaults to `unit=>'px'`, so a design's unitless ratio (e.g. `line-height:1.08`) silently becomes `line-height:1.08px` — the line box collapses to ~1px and the *next* element's text visually overlaps/interleaves with this element's glyphs (looks like garbled/doubled text, easy to mistake for a font or encoding bug). Always pass `SZ($ratio, 'em')` for line-height (behaves identically to unitless for a leaf text element with no differently-sized descendants). Caught and fixed this exact bug on the Home page's `title-hero`/`lead`/`title-section`/`title-card` classes.
- **A plain text "link" (no button chrome) must not just skip background/padding/border in its global class if it's applied to an `e-button` widget** — `e-button` always carries its own default chrome (blue background, padding, border-radius) from its base style, so unless the class explicitly overrides `background` (→ `transparent`), `padding` (→ 0), `border-width` (→ 0), and `border-radius` (→ 0), the widget renders as a big colored box instead of inline text. Fixed on `link-more` this way. `min-height` is `Size_Prop_Type`, not `String_Prop_Type` — don't pass `STR('auto')` for it (wrong `$$type`, silently no-ops); just omit the prop instead of trying to set `auto`.

## Page element tree (`_elementor_data`)
Container/layout elements use the atomic element type directly as `elType` (no legacy `container` wrapper needed under the v4 opt-in): `e-flexbox` (default `display:flex`) and `e-div-block` (default `display:block`), both support `tag` (enum incl. `div|section|article|header|footer|aside|a|button`) and `link`. Leaf content uses `elType: 'widget'` + `widgetType`: `e-heading` (`tag` h1–h6, `title`), `e-paragraph` (`tag` p/span, `paragraph`), `e-button` (`text`, `link`), `e-image` (`image`). Every node needs a unique short `id` (7 hex chars used here, e.g. `substr(bin2hex(random_bytes(4)),0,7)`) or the editor may misbehave later; `settings.classes` is `['$$type'=>'classes','value'=>[<class-id>, ...]]`.

**Text content** (heading `title` / paragraph `paragraph` / button `text`) uses the `html-v3` shape:
```php
['$$type'=>'html-v3','value'=>['content'=>['$$type'=>'string','value'=>$text],'children'=>[]]]
```

**Image widget — this is NOT what `Image_Prop_Type::generate()` naively suggests.** The real, working, render-correct shape (confirmed the naive `{$$type:'image-attachment-id',value:ID}` directly under `src` renders an `<img>` with no `src` attribute at all — `generate()` doesn't validate nested shape, so it fails silently at render time, not at save time):
```php
'image' => [
  '$$type' => 'image',
  'value' => [
    'src' => [
      '$$type' => 'image-src',
      'value' => [ 'id' => ['$$type'=>'image-attachment-id','value'=>$attachmentId] ], // omit 'url'/'alt' when using an id
    ],
    'size' => ['$$type'=>'string','value'=>'full'],
  ],
],
```
Alt text is pulled automatically from the attachment's `_wp_attachment_image_alt` post meta at render time — don't try to set alt on the widget itself when using an attachment id.

**Button/link `href` — same trap.** `Link_Prop_Type`'s real shape has no `href` field; it has `destination` (Url or Query), `isTargetBlank`, `tag`. A raw `{'$$type':'link','value':{'href':'/x/'}}` silently renders as a plain `<button>` instead of `<a href>` (the twig checks `settings.link.href`, which only appears after the `destination` is resolved into `href` by a dedicated Link_Transformer). Working shape:
```php
'link' => ['$$type'=>'link','value'=>['destination'=>['$$type'=>'url','value'=>$href]]],
```

## Creating/updating the WP page itself
```php
$post_id = wp_insert_post([ 'post_title'=>'...', 'post_name'=>'slug', 'post_type'=>'page', 'post_status'=>'publish', 'post_content'=>'' ]);
update_post_meta( $post_id, '_elementor_edit_mode', 'builder' );
update_post_meta( $post_id, '_elementor_template_type', 'wp-page' );
update_post_meta( $post_id, '_elementor_version', ELEMENTOR_VERSION );
update_post_meta( $post_id, '_elementor_data', wp_json_encode( $elements, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) ); // $elements = array of top-level e-flexbox section nodes
update_post_meta( $post_id, '_elementor_page_settings', [ 'hide_title' => 'yes' ] );
update_post_meta( $post_id, '_wp_page_template', 'elementor_header_footer' ); // = the "Elementor Full Width" template option
update_post_meta( $post_id, 'site-post-title', 'disabled' );        // Astra: hide title
update_post_meta( $post_id, 'site-sidebar-layout', 'no-sidebar' );  // Astra: no sidebar
update_post_meta( $post_id, 'ast-site-content-layout', 'plain-container' ); // Astra: full-width container
\Elementor\Plugin::$instance->files_manager->clear_cache();
```

## Font variables must hold a bare font name, not a CSS fallback stack
Storing `font-display` as `"Playfair Display, Georgia, serif"` seems natural but **silently breaks Google Fonts loading**: Elementor decides whether to enqueue a font via `\Elementor\Fonts::get_font_type($value)`, which does an *exact* match against its known-fonts list. `get_font_type('Playfair Display')` → `'googlefonts'`; `get_font_type('Playfair Display, Georgia, serif')` → `false` (unrecognized/custom, never enqueued). Net effect: the CSS custom property still resolves fine (`var(--font-display)` outputs the full stack, so `getComputedStyle` looks "correct"), but no `<link>` to `fonts.googleapis.com` ever gets added — the browser falls back to whatever serif is locally installed, which on Vietnamese text can visibly break precomposed-diacritic rendering (looks like "combining marks floating next to the letter" — e.g. `tuần` → `tuâ`n`). **Fix: set the variable value to just the bare font name** (`'Playfair Display'`, `'Nunito Sans'`) — Elementor enqueues it with `&subset=vietnamese` automatically (matches how Astra's own Roboto/Roboto Slab load on this site) and the browser gets a real fallback chain from the font's own CSS anyway.

Also: the Kit's compiled CSS file (`wp-content/uploads/elementor/css/post-<kit_id>.css`, mirrored in postmeta `_elementor_css`) is only regenerated when something explicitly rebuilds it — editing global variables/classes via the PHP repositories does **not** auto-invalidate it beyond what `\Elementor\Plugin::$instance->files_manager->clear_cache()` deletes. After changing anything that affects the Kit CSS (variable values, especially font names), force a real rebuild, don't just clear the cache and hope the next page load regenerates it correctly:
```php
\Elementor\Plugin::$instance->files_manager->clear_cache();
$kit_id = \Elementor\Plugin::$instance->kits_manager->get_active_kit()->get_id();
\Elementor\Core\Files\CSS\Post::create( $kit_id )->update(); // forces a real re-render, not just a cache bust
\Elementor\Core\Files\CSS\Post::create( $page_post_id )->update(); // do the same for the page being tested
```
Check `get_post_meta($kit_id, '_elementor_css', true)['fonts']` afterwards — it should list the bare font names — before trusting a live page reload to show the `fonts.googleapis.com` `<link>` tags.

## Photo import (download → resize ≤1600px → WebP <400KB → media library)
`wp_remote_get($url)` → `imagecreatefromstring($body)` → if longest edge >1600, `imagecopyresampled` down to 1600 → loop `imagewebp($src, null, $quality)` starting at quality 82, step -10, until `strlen($data) < 400000` → `wp_upload_dir()` + `wp_unique_filename()` + `file_put_contents()` → `wp_insert_attachment(['post_mime_type'=>'image/webp', ...], $file_path)` → `wp_generate_attachment_metadata()` + `wp_update_attachment_metadata()` → `update_post_meta($id,'_wp_attachment_image_alt',$alt)`. GD on this server has WebP support (`imagewebp` exists; Imagick is NOT installed).

## Two classes on one element: the base class can silently beat the modifier class
When an element carries two global classes meant to layer (e.g. `['mark','mark-accent']`, `['row-split','row-split-top']`, `['section','section-tight']`, `['col-media','col-media-wide']`), Elementor's per-page compiled CSS does **not** reliably emit the later-added class's rule after the earlier one's — empirically the reverse happened every time (the older/base class's rule landed *later* in the compiled `global-{postId}-frontend-{bp}.css` file and won the tie on equal specificity, silently discarding the modifier's override). Confirmed via `document.styleSheets` rule-order inspection in-browser; not explained by the global-classes `order` array position, alphabetical id, or label — the mechanism is opaque, so don't try to out-order it.
**Fix that actually works:** make the "modifier" class a **complete standalone copy** of every variant/prop the base class has, with just the intended override changed, and apply **only the modifier class** on that element (drop the base class from `settings.classes.value` entirely). Verified working for `mark-accent`, `row-split-top`, `section-tight`, `col-media-wide`, `tile-media-tall` this way. Cheap to automate: after editing the modifier class, walk the page's `_elementor_data` tree and strip the base class id wherever the modifier id is also present.

## A literal `height` on a flex item can be silently ignored — root cause and fix
Elementor's own base CSS includes `.e-con { height: var(--height); }` (unconditional, no media query). A class's own `height: 220px` (etc.) *usually* still wins by specificity — except specifically for a flex item whose `flex-basis` is a **percentage** (e.g. `flex: 1 1 100%`) sitting inside a flex **column** container whose own height is auto/indefinite (this is exactly what `row-split` becomes on mobile — `flex-direction: column`). In that combination the percentage `flex-basis` resolves unpredictably against the indefinite parent and the child's rendered height blows up to some unrelated intrinsic value — even a `!important` inline `height` override does **not** fix it (proven by direct DOM test), which rules out a plain cascade/specificity explanation. What *does* fix it, verified by direct DOM experiment: give the item a **definite pixel `flex-basis`** matching the intended size (`flex: 0 0 220px` for a fixed-height image column) instead of a percentage one; for a content-driven column (no target height, e.g. a text column), use **`flex-basis: auto`** instead of `100%`. Applied this fix to `col-media`, `col-media-wide`, `col-copy`, `form-placeholder`'s mobile variants (all live inside `row-split`, which flips to column only on mobile) — anything else nested inside a container that changes `flex-direction` responsively should get the same treatment (percentage `flex-basis` in that context is not safe here). Adding a redundant `min-height` alongside `height` as a safeguard did **not** help — the mechanism isn't about `height` losing to `min-height`, it's specifically the percentage flex-basis.

## Elementor's own `.e-div-block-base` adds `padding: 10px` to every div-block, and `.e-con { padding }` variants apply too
An empty `e-div-block` (no children) picks up Elementor's own base padding (10px all sides) in addition to whatever your class sets — if your class only sets `height` (not `padding: 0`), the rendered box can end up padding-dominated instead of height-dominated (e.g. a class trying to be a 1px hairline divider rendered at 20px instead — 10px top + 10px bottom, `height` on that element wasn't the effective diner mechanism here either). **Fix used for a hairline divider:** don't fight it with `height` at all — set `padding: 0`, `height: 0`, and use a `border-top` (or `border-width`+`border-style`+`border-color`, since only uniform borders are supported) to draw the line instead. Any other custom class applied to a *content-bearing* `e-div-block`/`e-flexbox` (i.e. one that isn't visually empty) should still explicitly set `padding: 0` (or its own real padding) rather than relying on it being unset, since the 10px base default is always there as a floor.

## `execute-php` calls do not share PHP state, but redeclaring a PHP built-in inside one call is fatal
Every `novamira/execute-php` call runs in a fresh, isolated context — functions/variables defined in one call are gone in the next (confirmed via `function_exists()`), so helper functions (`rid()`, `CLS()`, etc.) must be pasted fresh into every call that needs them; no risk of "cannot redeclare" across separate calls. **Within a single call**, though, avoid naming a helper function the same as a PHP built-in — `function stat($value, $label) {...}` silently breaks the *entire* call (no catchable PHP error surfaces; the tool just reports "the connector's server isn't responding", indistinguishable from a real transport failure, and retrying the identical payload fails identically every time). Diagnosed by bisecting the script down to the single offending function name. Rename anything that collides with a built-in (`stat`, `str`, `error`, `list`, `array`, `print`, etc.) before spending time on network-failure theories.

## A literal straight double-quote (`"`) anywhere in your text content silently corrupts the saved `_elementor_data`
If any text string passed into `TXT()`/`para()`/`heading()` contains a literal ASCII `"` character (e.g. quoting a phrase like `He said "stop"`), the properly-escaped `\"` that `wp_json_encode()` produces gets its escaping backslash **stripped somewhere in WordPress's `update_post_meta()` storage path** — turning valid JSON (`...value\":\"He said \\\"stop\\\"...`) into broken JSON (`...\"He said \"stop\"...`) actually stored in the DB. The page still "saves" without any visible error, `_elementor_data` still has a normal-looking length, and the post still resolves to the correct URL — but Elementor's `Frontend::get_builder_content_for_display()` silently returns an **empty string** (its internal `json_decode` fails, `get_elements_data()` returns empty, function bails with `''`), and because the filter returns empty, WordPress falls through to rendering the *original* raw `post_content` instead (visible if you convert an existing classic post to Elementor and didn't clear `post_content` — you'll see the OLD content, not a blank page, which looks like "my Elementor edit didn't take" rather than a JSON bug). No PHP exception, no warning — diagnose by checking `$doc->get_elements_data()` count and `json_last_error()` on the raw postmeta directly, not by trusting a non-empty stored length.
**Fix:** never put a literal `"` in content text — use the Vietnamese/typographic curly quotes `“`/`”` (“ ”) instead (they need no escaping, sidestepping the bug entirely). Caught this after two full articles (long-form, real content ported from existing posts) rendered as blank/fallback-content pages; a bisection script that recursively walks the top-level element array, re-`json_decode`-ing each node's own JSON substring, isolates the exact corrupted leaf fast — full re-decode of the whole tree only tells you *that* it's broken, not *where*.
**Also:** don't declare a helper function with the same name as a PHP built-in in the SAME `execute-php` call more than once inside a loop (e.g. defining `function findImg(...)` inside a `foreach`) — second iteration is a redeclaration fatal, and separately, naming a helper `stat()` shadows the built-in and fatals immediately; both produce the generic "connector not responding" error rather than a catchable PHP error, indistinguishable from a real transport failure without bisecting the script.

## Verifying a build
`preview_start`/`navigate` to the page, then use `javascript_tool` (not screenshot — the Browser pane doesn't compositor-render for screenshots in this harness) to read `getComputedStyle()` on key elements and check `outerHTML`/`naturalWidth` on images. `get_page_text` + `read_console_messages` alone aren't enough — they didn't catch the empty-`src`/wrong-tag bugs above; only inspecting live computed DOM did.
