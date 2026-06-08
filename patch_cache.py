import re

with open("/opt/odysseus/data/builtin_mcp.py", "r") as f:
    content = f.read()

old = """        return False
    return proc.returncode == 0 and bool(stdout.strip())"""

new = """        return False
    if proc.returncode == 0 and bool(stdout.strip()):
        return True
    # Fallback: npx --no-install is unreliable on npm 9.x (always "canceled")
    npm_cache = os.environ.get("npm_config_cache", os.path.expanduser("~/.npm"))
    npx_cache = os.path.join(npm_cache, "_npx")
    pkg_spec2 = package_spec
    if pkg_spec2.count("@") >= 2:
        parts = pkg_spec2.rsplit("@", 1)
        pkg_name = parts[0]
    else:
        pkg_name = pkg_spec2.split("@")[0] if "@" in pkg_spec2 else pkg_spec2
    pkg_name = pkg_name.replace("/", os.sep)
    try:
        import glob
        for entry in glob.glob(os.path.join(npx_cache, "*/node_modules", pkg_name, "package.json")):
            if os.path.isfile(entry):
                return True
    except Exception:
        pass
    return False"""

if old in content:
    content = content.replace(old, new)
    with open("/opt/odysseus/data/builtin_mcp.py", "w") as f:
        f.write(content)
    print("Patched successfully")
else:
    print("ERROR: old string not found!")
    import re
    # Find the relevant section for debugging
    idx = content.find("return proc.returncode")
    if idx > 0:
        print("Found at offset", idx)
        print(content[idx-50:idx+80])
