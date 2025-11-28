"""
CODE IS DOWN BELLOW

Purpose
- These helpers let you visually highlight DOM elements while debugging Selenium scripts.
  They do NOT click elements — they only change style or inject an overlay so you can verify
  the exact element you intend to interact with.

Required imports
- import time
- from time import sleep
- Selenium driver instance (e.g., `site`) must already be available

Functions and behavior

1) debugging_highlight_once(driver, element, color="red", border_width=3, duration=1.5)
- What it does: temporarily applies an outline to `element` (e.g., "outline: 3px solid red")
  and then restores the element’s original inline style after `duration` seconds.
- When to use: quick one-shot highlight before a click to confirm element identity and position.
- Effects: non-destructive — restores original style at the end. Uses sleep(duration) to pause while visible.
- Example:
    debugging_highlight_once(site, td_clicavel, color="lime", border_width=4, duration=2)

2) debugging_add_overlay(driver, element, label="TARGET")
- What it does: injects a visible dashed rectangular overlay (and a small label) positioned on top of the element.
  The overlay is appended to document.body and remains until removed.
- When to use: when you want a persistent visual marker that remains while you inspect the page manually or take screenshots.
- Note: overlay stays until you call debugging_remove_overlay.
- Example:
    debugging_add_overlay(site, td_clicavel, label="ESPEC")
    time.sleep(3)           # inspect visually
    debugging_remove_overlay(site)

3) debugging_remove_overlay(driver)
- What it does: removes the overlay <div id="selenium_debug_overlay"> from the page (if present).
- Example:
    debugging_remove_overlay(site)

4) debugging_highlight_flash(driver, element, flashes=3, on_color="red", off_delay=0.4)
- What it does: flashes the element style on/off for `flashes` times to attract attention (outline + faint background).
- When to use: if the page is busy and you want a repeated visual cue.
- Example:
    debugging_highlight_flash(site, td_clicavel, flashes=4, on_color="magenta", off_delay=0.35)

Important caveats and tips
- If the element is inside an iframe:
    - Switch to the correct iframe first: site.switch_to.frame(...) before calling any of these helpers.
    - After debugging, remember to site.switch_to.default_content() if you need to operate on top-level DOM.
- Cross-origin iframes: you cannot access or modify DOM inside cross-origin frames — these helpers will fail.
- Element visibility: if element has display:none or is off-screen, the highlight might not be visible. Use:
    - site.execute_script("arguments[0].scrollIntoView({block: 'center'});", element) before highlighting.
    - Check element.is_displayed() before highlighting.
- Styles: helpers change the element’s inline style attribute and attempt to restore it. If the element is frequently mutated by page scripts,
  restoration may not exactly revert to pre-highlight visual state.
- Persistence: debugging_add_overlay inserts an overlay into the page. Always remove it after inspection.
- Use in debug only: avoid leaving these in production automation flows. They deliberately call sleep() to make the highlight visible.

Saving visual state for later inspection
- Save a screenshot and HTML at debug points:
    site.save_screenshot("debug_element.png")
    open("debug_dom.html", "w", encoding="utf-8").write(site.page_source)

Quick checklist before highlight
1. Switch to iframe if needed.
2. Scroll element into view.
3. Verify element.is_displayed() and element.is_enabled().
4. Call highlight helper.
5. Inspect / screenshot / remove overlay.

Suggested small corrections
- Fix typo in function name: change `debuggin_add_overlay` -> `debugging_add_overlay`.
- Consider adding optional restore=True/False flag if you want to keep styles altered for longer.

If you want, generate a one-file snippet that includes these helpers plus ready-to-run debug blocks (before-click and after-click)
that save screenshot + HTML and pause with input() so you can visually inspect.
"""


def debugging_highlight_once(driver, element, color="red", border_width=3, duration=1.5):
    try:
        # guarda estilo original
        original_style = driver.execute_script(
            "var e = arguments[0]; var s = e.getAttribute('style') || ''; return s;", element)
        # aplica destaque
        driver.execute_script(
            "arguments[0].setAttribute('style', arguments[1]);",
            element, f"outline: {border_width}px solid {color}; transition: outline 0.2s ease; {original_style}"
        )
        sleep(duration)
        # reverte estilo original
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, original_style)
    except Exception as e:
        print("highlight_once falhou:", e)

def debuggin_add_overlay(driver, element, label="TARGET"):
    """" Run this , sleep(3), then run remove_overlay to see a red dashed box around the element
     add_overlay(site, td_clicavel, label="ESPEC")
     time.sleep(3)
     remove_overlay(site) """
    
    try:
        rect = driver.execute_script("""
            var e = arguments[0];
            var r = e.getBoundingClientRect();
            return {left: r.left, top: r.top, width: r.width, height: r.height, scrollX: window.scrollX, scrollY: window.scrollY};
        """, element)
        js = f"""
        var ov = document.createElement('div');
        ov.id = 'selenium_debug_overlay';
        ov.style.position='absolute';
        ov.style.left='{rect['left'] + rect['scrollX']}px';
        ov.style.top='{rect['top'] + rect['scrollY']}px';
        ov.style.width='{rect['width']}px';
        ov.style.height='{rect['height']}px';
        ov.style.border='3px dashed red';
        ov.style.zIndex=9999999;
        ov.style.pointerEvents='none';
        var label = document.createElement('div');
        label.style.position='absolute';
        label.style.top='-18px';
        label.style.left='0px';
        label.style.background='red';
        label.style.color='white';
        label.style.fontSize='12px';
        label.style.padding='2px';
        label.innerText = '{label}';
        ov.appendChild(label);
        document.body.appendChild(ov);
        """
        driver.execute_script(js)
    except Exception as e:
        print("add_overlay falhou:", e)
def debugging_remove_overlay(driver):
    driver.execute_script("var el = document.getElementById('selenium_debug_overlay'); if(el) el.remove();")


def debugging_highlight_flash(driver, element, flashes=3, on_color="red", off_delay=0.4):
    try:
        original_style = driver.execute_script("var e=arguments[0]; return e.getAttribute('style') || '';",
                                               element)
        for _ in range(flashes):
            driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                                  element, f"outline: 4px solid {on_color}; background: rgba(255,255,0,0.2);")
            sleep(off_delay)
            driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, original_style)
            sleep(off_delay)
    except Exception as e:
        print("highlight_flash falhou:", e)
