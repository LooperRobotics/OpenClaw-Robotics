#!/usr/bin/env python3
"""
GitHub Automation Script
Helps to push code to GitHub using API
"""

import os
import subprocess
import json
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from base64 import b64encode
import getpass

def get_github_token():
    """Get GitHub Personal Access Token"""
    token = os.environ.get('GITHUB_TOKEN')
    if token:
        return token
    
    print("GitHub Personal Access Token not found.")
    print("Please get one from: https://github.com/settings/tokens")
    print("Required scopes: repo (full control of private repositories)")
    token = getpass.getpass("Enter your GitHub Personal Access Token: ")
    return token

def get_current_branch():
    """Get current git branch"""
    result = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], 
                          capture_output=True, text=True, cwd=os.getcwd())
    return result.stdout.strip()

def push_to_github(token, repo_owner, repo_name, branch="main"):
    """Push code to GitHub using API"""
    
    # Get repository root
    repo_root = subprocess.run(['git', 'rev-parse', '--show-toplevel'], 
                             capture_output=True, text=True).stdout.strip()
    
    os.chdir(repo_root)
    
    # Get changes
    result = subprocess.run(['git', 'status', '--porcelain'], 
                          capture_output=True, text=True)
    
    if not result.stdout.strip():
        print("No changes to commit!")
        return True
    
    print(f"Changes detected in {repo_root}")
    print(f"Repository: {repo_owner}/{repo_name}")
    print(f"Branch: {branch}")
    
    # Get latest commit info
    result = subprocess.run(['git', 'log', '-1', '--format=%H%n%s%n%b'], 
                          capture_output=True, text=True)
    commit_info = result.stdout.strip().split('\n')
    latest_commit_hash = commit_info[0]
    commit_message = commit_info[1] if len(commit_info) > 1 else "Update"
    commit_body = '\n'.join(commit_info[2:]) if len(commit_info) > 2 else ""
    
    print(f"Latest commit: {latest_commit_hash}")
    
    # Try to push
    print("\nAttempting to push to GitHub...")
    
    # Method 1: Try git push first (might work if token is cached)
    result = subprocess.run(['git', 'push', 'origin', branch], 
                          capture_output=True, text=True, timeout=30)
    
    if result.returncode == 0:
        print("✅ Successfully pushed to GitHub!")
        return True
    else:
        print(f"❌ Direct push failed: {result.stderr}")
        print("\nPlease push manually with:")
        print(f"  cd {repo_root}")
        print(f"  git push origin {branch}")
        return False

def main():
    print("=" * 60)
    print("GitHub Push Helper for OpenClaw-Robotics")
    print("=" * 60)
    
    repo_owner = "LooperRobotics"
    repo_name = "OpenClaw-Robotics"
    
    # Try to push
    success = push_to_github(None, repo_owner, repo_name)
    
    if success:
        print("\n🎉 All done! Code is now on GitHub.")
    else:
        print("\n📋 Manual steps required:")
        print("1. Create a GitHub Personal Access Token")
        print("   URL: https://github.com/settings/tokens")
        print("   Scopes: repo (full control)")
        print()
        print("2. Either:")
        print("   a) Run: git push origin main")
        print("      (and enter your token as password)")
        print()
        print("   b) Set environment variable:")
        print("      export GITHUB_TOKEN=your_token_here")
        print()
        print("3. Or use GitHub CLI:")
        print("   brew install gh  # macOS")
        print("   gh auth login")
        print("   gh repo sync LooperRobotics/OpenClaw-Robotics")
    
    return success

if __name__ == "__main__":
    main()
