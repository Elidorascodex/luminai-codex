"""Simple PTQ experiment smoke-test.

This script performs environment checks and demonstrates a minimal PTQ
conversion path using Optimum if available. It's defensive: if dependencies
are missing it will print instructions rather than failing dramatically.

Intended for local experiments only. Do not run this in CI without
appropriate compute resources.
"""
import argparse
import importlib
import sys


def check_import(name):
    try:
        return importlib.import_module(name)
    except Exception as e:
        print(f"Optional dependency '{name}' not available: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="PTQ smoke-test")
    parser.add_argument("--model", default="sshleifer/tiny-gpt2", help="Hugging Face model id to test (small)")
    parser.add_argument("--dry-run", action="store_true", help="Only check environment and dependencies")
    args = parser.parse_args()

    torch = check_import("torch")
    transformers = check_import("transformers")
    optimum = check_import("optimum")

    if not transformers:
        print("Please install transformers (pip install transformers) and retry.")
        sys.exit(1)

    print("Found transformers. Model I/O is available.")

    if args.dry_run:
        print("Dry run complete. Install 'optimum' and 'bitsandbytes' to try quantization flows.")
        return

    if not optimum:
        print("Optimum not installed — attempting a lightweight conversion is skipped.")
        print("Install with: pip install 'optimum[exporters]'")
        return

    # Minimal example using optimum export helpers (if present)
    try:
        from transformers import AutoModelForCausalLM, AutoTokenizer

        print(f"Loading model {args.model} (small test model)...")
        tokenizer = AutoTokenizer.from_pretrained(args.model)
        model = AutoModelForCausalLM.from_pretrained(args.model)

        print("Model loaded. Skipping heavy quantization steps in the scaffold.")
        print("You can plug in Optimum quantization APIs or bitsandbytes wrappers here.")
    except Exception as e:
        print("Model load failed:", e)


if __name__ == "__main__":
    main()
