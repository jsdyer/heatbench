"""Exercise the built starter at a project subpath in Chromium."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import shutil
import os
import tempfile
import threading
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def main():
    screenshots = ROOT / "browser-checks"
    screenshots.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as temporary:
        shutil.copytree(ROOT / "dist", Path(temporary) / "example-tool")
        server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=temporary))
        threading.Thread(target=server.serve_forever, daemon=True).start()
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(executable_path=os.environ.get("PLAYWRIGHT_CHROMIUM_EXECUTABLE"))
                page = browser.new_page(viewport={"width": 1280, "height": 1000})
                errors = []
                page.on("pageerror", lambda error: errors.append(str(error)))
                page.goto(f"http://127.0.0.1:{server.server_port}/example-tool/")
                assert "kWh/year" in page.locator("#results").inner_text()
                page.locator("#annualUnits").fill("1000")
                page.locator("#scenarioName").fill("Test heating scenario")
                page.locator("#save").click()
                page.reload()
                page.get_by_role("button",name="Load",exact=True).wait_for()
                assert "Test heating scenario" in page.locator("#saved").inner_text()
                page.get_by_role("button",name="Load",exact=True).click()
                assert page.locator("#annualUnits").input_value() == "1000"
                page.locator("#copLow").fill("7")
                assert page.locator("#error").is_visible()
                page.locator("#reset").click()
                assert not page.locator("#error").is_visible()
                page.screenshot(path=str(screenshots / "desktop.png"), full_page=True)
                page.set_viewport_size({"width": 390, "height": 844})
                assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
                page.screenshot(path=str(screenshots / "mobile.png"), full_page=True)
                assert not errors, errors
                # Exercise the direct search landing page in a fresh browser context.
                case_page = browser.new_page(viewport={'width': 390, 'height': 844})
                case_page.route('https://**/*', lambda route: route.abort())
                case_page.goto(f'http://127.0.0.1:{server.server_port}/example-tool/electric-baseboard-heat-pump.html')
                case_page.wait_for_function("() => {const q=s=>document.querySelector(s);return q('#fuel').value==='electric' && q('#annualUnits').value==='12000' && q('#results').textContent.includes('heat');}")
                assert case_page.locator('link[rel="canonical"]').get_attribute('href') == 'https://coolcode.ca/heatbench/electric-baseboard-heat-pump.html'
                assert case_page.locator('h1').inner_text() in case_page.title()
                assert case_page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')
                browser.close()
            print("Browser checks passed: project subpath, heating calculations, saved scenarios, validation and mobile layout")
        finally:
            server.shutdown()


if __name__ == "__main__":
    main()
