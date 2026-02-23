#!/usr/bin/env python3
"""
Base Manager - Manages Airtable bases list for ERB projects.
Handles fetching base names from Airtable API and updating ssotme.json.
"""

import json
import os
import ssl
import subprocess
import sys
import urllib.request
import urllib.error

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
SSOTME_JSON = os.path.join(PROJECT_ROOT, "ssotme.json")
BASES_FILE = os.path.join(SCRIPT_DIR, "bases.json")  # Separate file that ssotme won't touch


def get_airtable_api_key():
    """Get Airtable API key from ssotme config."""
    try:
        result = subprocess.run(
            ["ssotme", "-info"],
            capture_output=True,
            text=True,
            timeout=10
        )
        for line in result.stdout.split("\n"):
            if "airtable:" in line.lower():
                parts = line.split(":", 1)
                if len(parts) > 1:
                    return parts[1].strip()
    except Exception as e:
        print(f"Warning: Could not get API key from ssotme: {e}", file=sys.stderr)
    return None


def fetch_base_name(base_id: str, api_key: str) -> str:
    """Fetch the base name from Airtable API."""
    url = f"https://api.airtable.com/v0/meta/bases/{base_id}"

    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {api_key}")

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    try:
        with urllib.request.urlopen(req, timeout=10, context=ssl_context) as response:
            data = json.loads(response.read().decode())
            return data.get("name", base_id)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise ValueError(f"Base '{base_id}' not found. Check the base ID.")
        elif e.code == 401:
            raise ValueError("Invalid API key or insufficient permissions.")
        else:
            raise ValueError(f"Airtable API error: {e.code} - {e.reason}")
    except Exception as e:
        raise ValueError(f"Failed to fetch base info: {e}")


def load_ssotme_config():
    """Load the ssotme.json config."""
    with open(SSOTME_JSON, "r") as f:
        return json.load(f)


def save_ssotme_config(config):
    """Save the ssotme.json config."""
    with open(SSOTME_JSON, "w") as f:
        json.dump(config, f, indent=2)


def get_setting(config, name):
    """Get a project setting value."""
    for setting in config.get("ProjectSettings", []):
        if setting.get("Name") == name:
            return setting.get("Value")
    return None


def set_setting(config, name, value):
    """Set a project setting value."""
    for setting in config.get("ProjectSettings", []):
        if setting.get("Name") == name:
            setting["Value"] = value
            return
    config.setdefault("ProjectSettings", []).append({
        "Name": name,
        "Value": value
    })


def get_bases_list(config=None):
    """Get the list of bases from separate bases.json file (or migrate from ssotme.json)."""
    # Primary: read from separate bases.json file
    if os.path.exists(BASES_FILE):
        try:
            with open(BASES_FILE, "r") as f:
                bases = json.load(f)
                if isinstance(bases, list):
                    return bases
        except (json.JSONDecodeError, IOError):
            pass

    # Fallback: migrate from ssotme.json if bases.json doesn't exist
    if config is None:
        config = load_ssotme_config()
    bases_json = get_setting(config, "bases")
    if bases_json:
        try:
            bases = json.loads(bases_json)
            if isinstance(bases, list):
                # Migrate to separate file
                set_bases_list(None, bases)
                return bases
        except json.JSONDecodeError:
            pass
    return []


def set_bases_list(config, bases):
    """Save bases to separate bases.json file (ssotme won't overwrite this)."""
    with open(BASES_FILE, "w") as f:
        json.dump(bases, f, indent=2)
    # Also update ssotme.json for backward compatibility (if config provided)
    if config is not None:
        set_setting(config, "bases", json.dumps(bases))


def ensure_current_base_in_list(config=None):
    """Ensure the current active base is in the bases list with correct name."""
    if config is None:
        config = load_ssotme_config()
        should_save = True
    else:
        should_save = False

    current_base_id = get_setting(config, "baseId")
    project_name = config.get("Name", "Unknown")

    if not current_base_id:
        return config

    bases = get_bases_list(config)

    # Find if current base exists in list
    found = False
    for base in bases:
        if base["id"] == current_base_id:
            # Update name to match current project name
            if base["name"] != project_name:
                base["name"] = project_name
                set_bases_list(config, bases)
            found = True
            break

    # Add current base if not in list
    if not found:
        bases.append({"id": current_base_id, "name": project_name})
        set_bases_list(config, bases)

    if should_save:
        save_ssotme_config(config)

    return config


def add_or_update_base(base_id: str, base_name: str) -> dict:
    """Add a new base or update existing one. Returns the base info."""
    config = load_ssotme_config()

    # Ensure current base is in list first
    ensure_current_base_in_list(config)

    bases = get_bases_list(config)

    # Check if base already exists - update if so
    for base in bases:
        if base["id"] == base_id:
            if base["name"] != base_name:
                base["name"] = base_name
                set_bases_list(config, bases)
                save_ssotme_config(config)
                print(f"Updated base: {base_name} ({base_id})")
            else:
                print(f"Base already exists: {base_name} ({base_id})")
            return base

    # Add new base
    new_base = {"id": base_id, "name": base_name}
    bases.append(new_base)
    set_bases_list(config, bases)
    save_ssotme_config(config)

    print(f"Added base: {base_name} ({base_id})")
    return new_base


def try_fetch_base_name(base_id: str) -> str:
    """Try to fetch base name from Airtable. Returns None if failed."""
    api_key = get_airtable_api_key()
    if not api_key:
        return None
    try:
        return fetch_base_name(base_id, api_key)
    except Exception as e:
        print(f"Could not fetch base name: {e}", file=sys.stderr)
        return None


def select_base(base_id: str) -> dict:
    """Select a base as the active base. Returns the base info."""
    config = load_ssotme_config()

    # Ensure current base is preserved in list before switching
    ensure_current_base_in_list(config)

    bases = get_bases_list(config)

    # Find the base
    base = None
    for b in bases:
        if b["id"] == base_id:
            base = b
            break

    if not base:
        raise ValueError(f"Base {base_id} not found in bases list. Add it first.")

    # Update active base settings
    set_setting(config, "baseId", base["id"])
    set_setting(config, "project-name", base["name"])
    config["Name"] = base["name"]

    save_ssotme_config(config)
    print(f"Selected base: {base['name']} ({base['id']})")
    return base


def list_bases():
    """List all known bases."""
    config = load_ssotme_config()

    # Ensure current base is in list
    ensure_current_base_in_list(config)

    bases = get_bases_list(config)
    current_base_id = get_setting(config, "baseId")

    print("\nKnown bases:")
    for i, base in enumerate(bases, 1):
        marker = " (active)" if base["id"] == current_base_id else ""
        print(f"  [{i}] {base['name']}{marker}")
        print(f"      ID: {base['id']}")

    if not bases:
        print("  (no bases configured)")

    return bases


def remove_base(base_id: str):
    """Remove a base from the list (but not if it's active)."""
    config = load_ssotme_config()
    bases = get_bases_list(config)
    current_base_id = get_setting(config, "baseId")

    if base_id == current_base_id:
        raise ValueError("Cannot remove the active base. Switch to another base first.")

    original_count = len(bases)
    bases = [b for b in bases if b["id"] != base_id]

    if len(bases) == original_count:
        print(f"Base not found: {base_id}")
        return

    set_bases_list(config, bases)
    save_ssotme_config(config)
    print(f"Removed base: {base_id}")


def sync_bases():
    """Sync the bases list to ensure current base is included with correct name."""
    config = load_ssotme_config()
    ensure_current_base_in_list(config)
    save_ssotme_config(config)
    print("Bases list synced.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Manage Airtable bases for ERB project")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # List command
    subparsers.add_parser("list", help="List all known bases")

    # Add command - now requires --name since interactive input doesn't work in subshells
    add_parser = subparsers.add_parser("add", help="Add or update a base")
    add_parser.add_argument("base_id", help="Airtable base ID (e.g., appXXXXXX)")
    add_parser.add_argument("--name", required=False, help="Base name (required if API fetch fails)")

    # Select command
    select_parser = subparsers.add_parser("select", help="Select a base as active")
    select_parser.add_argument("base_id", help="Base ID or list number")

    # Remove command
    remove_parser = subparsers.add_parser("remove", help="Remove a base from list")
    remove_parser.add_argument("base_id", help="Airtable base ID to remove")

    # Fetch name command
    fetch_parser = subparsers.add_parser("fetch-name", help="Fetch base name from Airtable")
    fetch_parser.add_argument("base_id", help="Airtable base ID")

    # Sync command
    subparsers.add_parser("sync", help="Sync bases list with current active base")

    args = parser.parse_args()

    try:
        if args.command == "list":
            list_bases()
        elif args.command == "add":
            base_name = args.name
            if not base_name:
                # Try to fetch from API
                base_name = try_fetch_base_name(args.base_id)
            if not base_name:
                print("Error: Could not fetch base name. Please provide --name", file=sys.stderr)
                sys.exit(1)
            add_or_update_base(args.base_id, base_name)
        elif args.command == "select":
            if args.base_id.isdigit():
                config = load_ssotme_config()
                ensure_current_base_in_list(config)
                bases = get_bases_list(config)
                idx = int(args.base_id) - 1
                if 0 <= idx < len(bases):
                    select_base(bases[idx]["id"])
                else:
                    print(f"Invalid selection: {args.base_id}")
                    sys.exit(1)
            else:
                select_base(args.base_id)
        elif args.command == "remove":
            remove_base(args.base_id)
        elif args.command == "fetch-name":
            name = try_fetch_base_name(args.base_id)
            if name:
                print(f"Base name: {name}")
            else:
                print("Could not fetch base name")
                sys.exit(1)
        elif args.command == "sync":
            sync_bases()
        else:
            parser.print_help()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
