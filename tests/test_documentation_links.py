from pathlib import Path
import re
import unittest
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK_RE = re.compile(
    r"!?\[[^\]]*\]\((?P<markdown>[^)]+)\)|"
    r"<(?:img|a)\b[^>]+(?:src|href)=[\"'](?P<html>[^\"']+)[\"']",
    re.IGNORECASE,
)


class DocumentationLinkTests(unittest.TestCase):
    def test_local_markdown_links_exist(self) -> None:
        missing: list[str] = []
        markdown_files = [ROOT / "README.md", *ROOT.glob("**/*.md")]
        for document in sorted(set(markdown_files)):
            if ".git" in document.parts:
                continue
            text = document.read_text(encoding="utf-8")
            for match in MARKDOWN_LINK_RE.finditer(text):
                raw_target = (match.group("markdown") or match.group("html")).strip()
                target = raw_target.split(maxsplit=1)[0].strip("<>")
                if (
                    not target
                    or target.startswith(("#", "http://", "https://", "mailto:"))
                ):
                    continue
                relative = unquote(target.split("#", 1)[0])
                candidate = (document.parent / relative).resolve()
                try:
                    candidate.relative_to(ROOT)
                except ValueError:
                    missing.append(f"{document.relative_to(ROOT)} -> outside repo: {target}")
                    continue
                if not candidate.exists():
                    missing.append(f"{document.relative_to(ROOT)} -> {target}")

        self.assertEqual(missing, [], "\n".join(missing))


if __name__ == "__main__":
    unittest.main()
