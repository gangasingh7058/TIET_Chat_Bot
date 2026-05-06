"""
One-time script to index all college PDFs using local PageIndex.

Run this once to build the tree structure index for all documents.
After indexing, the workspace caches everything — no need to re-run.

Usage:
    Activate the Tiet Chat Bot venv, then:
    python index_docs.py
"""
import sys
import os
import json
import time
from pathlib import Path

# Fix Windows terminal encoding for Unicode output
sys.stdout.reconfigure(encoding="utf-8")

# Add PageIndex to path
PAGEINDEX_PATH = r"d:\Python\PageIndex_Github\PageIndex"
sys.path.insert(0, PAGEINDEX_PATH)

from dotenv import load_dotenv
load_dotenv(override=True)

from pageindex import PageIndexClient

# Workspace directory -- persists indexed documents
WORKSPACE_DIR = Path(__file__).parent / "pageindex_workspace"
PDFS_DIR = Path(__file__).parent / "PDFS"

# Delay (in seconds) between indexing each PDF to avoid rate limits
DELAY_BETWEEN_PDFS = 90

# HuggingFace API key for LLM calls during indexing
HF_TOKEN = os.getenv("HUGGING_FACE_API_TOKEN")
if not HF_TOKEN:
    raise ValueError("Missing HUGGING_FACE_API_TOKEN in .env")

# Set the key for litellm/huggingface
os.environ["HUGGINGFACE_API_KEY"] = HF_TOKEN


def main():
    # Allow overriding delay via command-line arg: python index_docs.py --delay 90
    delay = DELAY_BETWEEN_PDFS
    if "--delay" in sys.argv:
        idx = sys.argv.index("--delay")
        if idx + 1 < len(sys.argv):
            delay = int(sys.argv[idx + 1])

    print("=" * 60)
    print("  PageIndex Local Indexer -- TIET Documents")
    print(f"  Delay between PDFs: {delay}s")
    print("=" * 60)

    # Initialize client with persistent workspace
    client = PageIndexClient(
        workspace=str(WORKSPACE_DIR),
        model="huggingface/Qwen/Qwen2.5-72B-Instruct",
    )

    # Check which docs are already indexed
    existing_docs = {
        doc.get("doc_name", ""): doc_id
        for doc_id, doc in client.documents.items()
    }

    if existing_docs:
        print(f"\n[OK] Already indexed ({len(existing_docs)} documents):")
        for name, doc_id in existing_docs.items():
            print(f"   - {name} -> {doc_id}")

    # Find all PDFs to index
    pdf_files = sorted(PDFS_DIR.glob("*.pdf"))
    print(f"\n[DIR] Found {len(pdf_files)} PDFs in {PDFS_DIR}:")
    for pdf in pdf_files:
        print(f"   - {pdf.name}")

    # Count how many actually need indexing
    to_index = [p for p in pdf_files if p.name not in existing_docs]
    print(f"\n[INFO] {len(to_index)} PDFs to index, {len(pdf_files) - len(to_index)} already done.")

    # Index each PDF (skips already indexed)
    doc_ids = {}
    indexed_count = 0
    for pdf in pdf_files:
        if pdf.name in existing_docs:
            print(f"\n[SKIP] Skipping {pdf.name} (already indexed)")
            doc_ids[pdf.name] = existing_docs[pdf.name]
            continue

        # Wait between PDFs (but not before the first one)
        if indexed_count > 0:
            print(f"\n[WAIT] Waiting {delay}s before next PDF to avoid rate limits...")
            time.sleep(delay)

        print(f"\n[INDEX] Indexing ({indexed_count + 1}/{len(to_index)}): {pdf.name}...")
        try:
            doc_id = client.index(str(pdf))
            doc_ids[pdf.name] = doc_id
            indexed_count += 1
            print(f"   [OK] Done! doc_id: {doc_id}")
        except Exception as e:
            print(f"   [FAIL] Failed: {e}")
            indexed_count += 1
            continue

    # Save doc_ids mapping
    doc_ids_path = Path(__file__).parent / "doc_ids.json"
    with open(doc_ids_path, "w") as f:
        json.dump(doc_ids, f, indent=2)

    print(f"\n{'=' * 60}")
    print(f"[OK] All done! {len(doc_ids)} documents indexed.")
    print(f"   Workspace: {WORKSPACE_DIR}")
    print(f"   Doc IDs saved to: {doc_ids_path}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
