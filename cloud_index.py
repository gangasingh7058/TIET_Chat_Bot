"""
Upload PDFs to PageIndex Cloud, wait for processing, then download
tree structure + page content and save locally.

This avoids needing HuggingFace/Gemini credits for indexing —
PageIndex cloud handles all the LLM work on their servers.

Usage:
    python cloud_index.py
    python cloud_index.py --delay 30   # custom delay between status checks
"""
import sys
import os
import json
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

from dotenv import load_dotenv
load_dotenv(override=True)

# PageIndex Cloud SDK (pip install pageindex)
from pageindex import PageIndexClient

PDFS_DIR = Path(__file__).parent / "PDFS"
LOCAL_DATA_DIR = Path(__file__).parent / "pageindex_data"
DOC_IDS_PATH = Path(__file__).parent / "doc_ids.json"

# PageIndex API key
PAGEINDEX_API_KEY = os.getenv("PAGEINDEX_API_KEY")
if not PAGEINDEX_API_KEY:
    raise ValueError("Missing PAGEINDEX_API_KEY in .env — get one at https://pageindex.ai")

client = PageIndexClient(api_key=PAGEINDEX_API_KEY)


def wait_for_ready(doc_id: str, name: str, poll_interval: int = 15, max_wait: int = 300):
    """Poll until document is ready for retrieval."""
    elapsed = 0
    while elapsed < max_wait:
        try:
            result = client.get_tree(doc_id)
            status = result.get("status", "")
            if result.get("retrieval_ready") or status == "completed":
                print(f"   [OK] {name} is ready!")
                return True
            print(f"   [WAIT] {name} status: {status} ({elapsed}s elapsed)...")
        except Exception as e:
            print(f"   [WAIT] {name} not ready yet ({elapsed}s elapsed)... {e}")
        time.sleep(poll_interval)
        elapsed += poll_interval
    print(f"   [TIMEOUT] {name} not ready after {max_wait}s")
    return False


def download_and_save(doc_id: str, name: str):
    """Download tree structure and OCR content, save as local JSON."""
    LOCAL_DATA_DIR.mkdir(exist_ok=True)
    doc_data = {}

    # 1. Get document metadata
    print(f"   Downloading metadata...")
    try:
        metadata = client.get_document(doc_id)
        doc_data["metadata"] = metadata
    except Exception as e:
        print(f"   [WARN] Could not get metadata: {e}")
        doc_data["metadata"] = {}

    # 2. Get tree structure (with summaries)
    print(f"   Downloading tree structure...")
    try:
        tree = client.get_tree(doc_id, node_summary=True)
        doc_data["tree"] = tree
    except Exception as e:
        print(f"   [FAIL] Could not get tree: {e}")
        return False

    # 3. Get OCR page content
    print(f"   Downloading page content (OCR)...")
    try:
        ocr = client.get_ocr(doc_id, format="page")
        doc_data["pages"] = ocr
    except Exception as e:
        print(f"   [WARN] Could not get OCR: {e}")
        doc_data["pages"] = {}

    # Save to local file
    save_path = LOCAL_DATA_DIR / f"{name}.json"
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(doc_data, f, indent=2, ensure_ascii=False)

    print(f"   [OK] Saved to {save_path}")
    return True


def main():
    poll_interval = 15
    if "--delay" in sys.argv:
        idx = sys.argv.index("--delay")
        if idx + 1 < len(sys.argv):
            poll_interval = int(sys.argv[idx + 1])

    fresh = "--fresh" in sys.argv

    print("=" * 60)
    print("  PageIndex Cloud Indexer -- TIET Documents")
    print(f"  Poll interval: {poll_interval}s")
    print(f"  Fresh upload: {fresh}")
    print("=" * 60)

    # Start fresh or load existing cloud doc_ids
    if fresh or not DOC_IDS_PATH.exists():
        doc_ids = {}
        if fresh:
            print("\n[FRESH] Starting fresh -- all PDFs will be re-uploaded")
    else:
        with open(DOC_IDS_PATH, "r") as f:
            doc_ids = json.load(f)
        # Filter out any non-cloud IDs (local IDs don't start with 'pi-')
        stale = {k: v for k, v in doc_ids.items() if not v.startswith("pi-")}
        if stale:
            print(f"\n[CLEAN] Removing {len(stale)} stale local IDs:")
            for k in stale:
                print(f"   - {k}: {doc_ids.pop(k)}")

    # Find PDFs
    pdf_files = sorted(PDFS_DIR.glob("*.pdf"))
    print(f"\n[DIR] Found {len(pdf_files)} PDFs in {PDFS_DIR}")

    # Step 1: Upload PDFs that don't have cloud doc_ids yet
    for pdf in pdf_files:
        if pdf.name in doc_ids:
            print(f"\n[SKIP] {pdf.name} already uploaded (doc_id: {doc_ids[pdf.name]})")
            continue

        print(f"\n[UPLOAD] Uploading {pdf.name}...")
        try:
            result = client.submit_document(str(pdf))
            doc_id = result["doc_id"]
            doc_ids[pdf.name] = doc_id
            print(f"   [OK] doc_id: {doc_id}")
        except Exception as e:
            print(f"   [FAIL] Upload failed: {e}")
            continue

    # Save doc_ids after upload
    with open(DOC_IDS_PATH, "w") as f:
        json.dump(doc_ids, f, indent=2)
    print(f"\n[SAVE] Doc IDs saved to {DOC_IDS_PATH}")

    # Step 2: Wait for all docs to be ready, then download
    print(f"\n{'=' * 60}")
    print("  Waiting for processing & downloading data...")
    print(f"{'=' * 60}")

    for pdf_name, doc_id in doc_ids.items():
        name = Path(pdf_name).stem
        local_file = LOCAL_DATA_DIR / f"{name}.json"

        # Skip if already downloaded
        if local_file.exists():
            print(f"\n[SKIP] {name} already downloaded locally")
            continue

        print(f"\n[PROCESS] {name} (doc_id: {doc_id})")

        # Wait for cloud processing to finish
        if not wait_for_ready(doc_id, name, poll_interval=poll_interval):
            continue

        # Download tree + pages
        download_and_save(doc_id, name)

    print(f"\n{'=' * 60}")
    print(f"[DONE] All documents processed!")
    print(f"   Local data: {LOCAL_DATA_DIR}")
    print(f"   Doc IDs: {DOC_IDS_PATH}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
