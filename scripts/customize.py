#!/usr/bin/env python3
"""Django-React Boilerplate customization script.

This module provides utilities to initialize and customize a Django-React boilerplate
project with user-provided settings including project name, description, author details,
and repository URL. It also generates a secure SECRET_KEY for Django configuration.
"""
import re
import secrets
import string
from pathlib import Path

# Set paths
BASE_DIR = Path(__file__).resolve().parent.parent
PYPROJECT_PATH = BASE_DIR / "pyproject.toml"
LICENSE_PATH = BASE_DIR / "LICENSE"
README_PATH = BASE_DIR / "docs" / "README.md"
ENV_EXAMPLE_PATH = BASE_DIR / ".env.example"
ENV_PATH = BASE_DIR / ".env"

# Known boilerplate defaults to replace
DEFAULT_PROJECT_NAME = "django-react-boilerplate"
DEFAULT_AUTHOR_NAME = "git-evinci"

def get_input(prompt: str, default: str = "") -> str:
    """Prompt user for input with a fallback default."""
    prompt_text = f"{prompt} [{default}]: " if default else f"{prompt}: "
    
    value = input(prompt_text).strip()
    return value if value else default

def generate_secret_key() -> str:
    """Generate a cryptographically secure Django secret key."""
    chars = string.ascii_letters + string.digits + "!@#$%^&*(-_=+)"
    return "".join(secrets.choice(chars) for _ in range(50))

def replace_in_file(filepath: Path, replacements: list[tuple[str, str]]) -> None:
    """Read a file, apply regex replacements, and write back."""
    if not filepath.exists():
        print(f"⚠️  Skipping {filepath.name} (file not found)")
        return

    with filepath.open("r", encoding="utf-8") as f:
        content = f.read()

    new_content = content
    for pattern, replacement in replacements:
        new_content = re.sub(pattern, replacement, new_content)

    if new_content != content:
        with filepath.open("w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"✅  Updated {filepath.name}")
    else:
        print(f"-  No changes needed in {filepath.name}")

def main() -> None:
    """Initialize the Django-React boilerplate project with custom settings."""
    print("🚀 Welcome to the Django-React Boilerplate Initializer!\n")

    # 1. Collect inputs
    project_slug = get_input("Project Slug (e.g., my-awesome-app)", "my-awesome-app")
    project_desc = get_input("Project Description", "A modern web application")
    author_name = get_input("Author Name", "My Name")
    author_email = get_input("Author Email", "me@example.com")
    repo_url = get_input("Repository URL", f"https://github.com/{author_name.replace(' ', '').lower()}/{project_slug}")

    print("\n⏳ Customizing your project...\n")

    # 2. Update pyproject.toml
    pyproject_replacements = [
        (rf'name\s*=\s*"{DEFAULT_PROJECT_NAME}"', f'name = "{project_slug}"'),
        (r'description\s*=\s*".*"', f'description = "{project_desc}"'),
        (r'authors\s*=\s*\[".*"\]', f'authors = ["{author_name} <{author_email}>"]'),
        (r'repository\s*=\s*".*"', f'repository = "{repo_url}"'),
    ]
    replace_in_file(PYPROJECT_PATH, pyproject_replacements)

    # 3. Update LICENSE
    license_replacements = [
        (rf"Copyright \(c\) \d{{4}} {DEFAULT_AUTHOR_NAME}", f"Copyright (c) 2026 {author_name}")
    ]
    replace_in_file(LICENSE_PATH, license_replacements)

    # 4. Update README.md
    readme_replacements = [
        (rf"#\s*{DEFAULT_PROJECT_NAME}", f'# {project_slug.replace("-", " ").title()}'),
        (rf"https://github\.com/{DEFAULT_AUTHOR_NAME}/{DEFAULT_PROJECT_NAME}", repo_url),
    ]
    replace_in_file(README_PATH, readme_replacements)

    # 5. Create and populate .env
    if ENV_EXAMPLE_PATH.exists() and not ENV_PATH.exists():
        with ENV_EXAMPLE_PATH.open("r", encoding="utf-8") as f:
            env_content = f.read()
        
        # Inject new SECRET_KEY
        new_secret = generate_secret_key()
        env_content = re.sub(
            r"SECRET_KEY=.*", 
            f"SECRET_KEY={new_secret}", 
            env_content
        )
        
        with ENV_PATH.open("w", encoding="utf-8") as f:
            f.write(env_content)
        print("✅  Created .env with fresh SECRET_KEY")
    elif ENV_PATH.exists():
        print("-  .env already exists, skipping generation")

    print("\n🎉 Customization complete! You are ready to build.")

if __name__ == "__main__":
    main()