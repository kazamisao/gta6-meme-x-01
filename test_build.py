"""Build checks for the gta6-meme-x-01 entry (TDD: written before the code).

Run: python3 test_build.py   (exit 0 only when every check passes)
"""
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent
FAILURES = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (f" — {detail}" if detail else ""))
    if not ok:
        FAILURES.append(name)


def main():
    # 1. Meme image: 1200x1200 PNG, made in-session by make_meme.py
    meme = REPO / "meme.png"
    check("meme.png exists", meme.exists())
    if meme.exists():
        from PIL import Image
        img = Image.open(meme)
        check("meme.png is 1200x1200", img.size == (1200, 1200), f"got {img.size}")
        check("meme.png is RGB", img.mode == "RGB", f"got {img.mode}")
        check("meme.png is a real PNG", img.format == "PNG", f"got {img.format}")
        check("meme.png is not tiny/blank", meme.stat().st_size > 50_000,
              f"{meme.stat().st_size} bytes")
    check("make_meme.py exists", (REPO / "make_meme.py").exists())

    # 2. POST.json: valid JSON object with a url key
    post = REPO / "POST.json"
    check("POST.json exists", post.exists())
    if post.exists():
        try:
            data = json.loads(post.read_text())
            check("POST.json is a JSON object", isinstance(data, dict))
            check("POST.json has url", isinstance(data, dict) and "url" in data)
        except Exception as e:  # noqa: BLE001 - test must report, not crash
            check("POST.json parses as JSON", False, str(e))

    # 3. main.ts copies POST.json to /output byte for byte
    out = REPO / "out" / "POST.json"
    out.parent.mkdir(exist_ok=True)
    env = {"PATH": "/usr/bin:/bin:/usr/local/bin", "MAKEFUN_BOT_DIR": str(REPO),
           "MAKEFUN_OUTPUT_DIR": str(REPO / "out")}
    r = subprocess.run(["node", "main.ts"], cwd=REPO, env=env,
                       capture_output=True, text=True)
    check("main.ts exits 0", r.returncode == 0, r.stderr.strip()[:200])
    check("main.ts is silent on success", r.stdout.strip() == "" and r.stderr.strip() == "",
          f"stdout={r.stdout!r} stderr={r.stderr!r}")
    if post.exists() and out.exists():
        check("out/POST.json equals POST.json",
              out.read_bytes() == post.read_bytes())

    # 4. Claim file names the payout wallet
    owner = REPO / ".makefun" / "owner.json"
    check(".makefun/owner.json exists", owner.exists())
    if owner.exists():
        try:
            data = json.loads(owner.read_text())
            check("owner.json wallet is payout wallet",
                  data.get("wallet") == "FCVXqAiSDbsUriov7NbvWJ1VsBYgnndnTN2hGMxZEP2s")
        except Exception as e:  # noqa: BLE001
            check("owner.json parses as JSON", False, str(e))

    # 5. No secrets in the repo tree (keypair material must never land here)
    bad = []
    for p in REPO.rglob("*"):
        if p.is_file() and ".git" not in p.parts and p.name not in ("test_build.py",):
            t = p.read_bytes()
            if b"api-key" in t.lower() and b"x-api-key" not in t.lower():
                bad.append(str(p))
    check("no credential-looking files in repo", not bad, ", ".join(bad))

    print(f"\n{len(FAILURES)} failure(s)" if FAILURES else "\nALL CHECKS PASSED")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
