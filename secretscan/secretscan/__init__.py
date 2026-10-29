"""SecretScan: scan for hardcoded secrets before pushing."""
from .scanner import check_env_gitignore, scan_path, scan_text

__version__ = "0.1.0"
__all__ = ["scan_path", "scan_text", "check_env_gitignore"]
