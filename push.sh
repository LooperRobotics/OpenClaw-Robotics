#!/bin/bash
# Push to GitHub script

set -e

REPO_DIR="/root/.openclaw/workspace/OpenClaw-Robotics"
BRANCH="main"

echo "🚀 Preparing to push OpenClaw-Robotics to GitHub..."
echo "📁 Directory: $REPO_DIR"
echo "🌿 Branch: $BRANCH"
echo ""

cd "$REPO_DIR"

# Check git status
echo "📊 Checking git status..."
git status --short

echo ""
echo "📝 Recent commits:"
git log --oneline -5

echo ""
echo "🔄 Attempting to push..."

# Try push with credential helper
git config credential.helper store

# Try push (will fail if no token cached)
if git push origin "$BRANCH" 2>&1; then
    echo ""
    echo "✅ SUCCESS! Code pushed to GitHub successfully!"
    echo "📱 View at: https://github.com/LooperRobotics/OpenClaw-Robotics"
else
    echo ""
    echo "❌ Push failed - authentication required"
    echo ""
    echo "📋 To complete the push, please run:"
    echo ""
    echo "   1. Get a GitHub Personal Access Token:"
    echo "      👉 https://github.com/settings/tokens"
    echo "      👉 Select 'repo' scope for full access"
    echo ""
    echo "   2. Run one of these commands:"
    echo ""
    echo "   Option A - Using token as password:"
    echo "   cd $REPO_DIR"
    echo "   git push origin $BRANCH"
    echo "   # When prompted, use your token as password"
    echo ""
    echo "   Option B - Using environment variable:"
    echo "   export GITHUB_TOKEN=your_token_here"
    echo "   git push origin $BRANCH"
    echo ""
    echo "   Option C - Using GitHub CLI (install first):"
    echo "   brew install gh  # macOS"
    echo "   # or"
    echo "   wget https://github.com/cli/cli/releases/download/v2.0.0/gh_2.0.0_linux_amd64.deb"
    echo "   sudo dpkg -i gh_2.0.0_linux_amd64.deb"
    echo "   gh auth login"
    echo "   gh repo sync LooperRobotics/OpenClaw-Robotics"
    echo ""
    echo "📁 Your changes are ready in: $REPO_DIR"
    echo "   Changes:"
    git status --short
fi
