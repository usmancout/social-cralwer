import os
import gzip
import json
from playwright.sync_api import Page


class SessionManager:
    """
    Save and load browser sessions (cookies + localStorage + sessionStorage)
    using gzip compression.

    Usage:
        session = SessionManager("instagram_session.json.gz")
        session_loaded = session.load(page)
        page.goto(url)
        if session_loaded:
            session.apply_storage(page)
    """

    def __init__(self, session_file="session_data.json.gz"):
        self.session_file = session_file
        self._pending_local = {}
        self._pending_session = {}

    def safe_get_storage(self, page: Page, storage_type: str):
        """Safely retrieve localStorage/sessionStorage without throwing errors."""
        script = f"""
        () => {{
            try {{
                return Object.assign({{}}, window.{storage_type});
            }} catch (e) {{
                return null;
            }}
        }}
        """
        return page.evaluate(script)

    def save(self, page: Page):
        """Save cookies and storage to gzip-compressed file."""
        state = {
            "cookies": page.context.cookies(),
            "local_storage": self.safe_get_storage(page, "localStorage"),
            "session_storage": self.safe_get_storage(page, "sessionStorage"),
        }

        with gzip.open(self.session_file, "wt", encoding="utf-8") as f:
            f.write(json.dumps(state))

        print(f"[✔] Session saved to {self.session_file}")

    def load(self, page: Page) -> bool:
        """
        Load cookies from session file.
        Storage is NOT applied yet. Call apply_storage(page) AFTER page.goto().
        Returns True if session file exists, False otherwise.
        """
        if not os.path.exists(self.session_file):
            print(f"[!] Session file {self.session_file} not found")
            return False

        with gzip.open(self.session_file, "rt", encoding="utf-8") as f:
            state = json.load(f)

        # Load cookies immediately (before navigation)
        if state.get("cookies"):
            page.context.add_cookies(state["cookies"])

        # Store local/session storage to apply after navigation
        self._pending_local = state.get("local_storage", {})
        self._pending_session = state.get("session_storage", {})

        print(f"[✔] Cookies loaded from {self.session_file}. Storage will apply after navigation.")
        return True

    def apply_storage(self, page: Page):
        """Apply localStorage and sessionStorage. Call AFTER page.goto()."""
        for k, v in self._pending_local.items():
            page.evaluate(f"() => localStorage.setItem('{k}', '{v}')")

        for k, v in self._pending_session.items():
            page.evaluate(f"() => sessionStorage.setItem('{k}', '{v}')")

        print(f"[✔] Storage applied from {self.session_file}")
