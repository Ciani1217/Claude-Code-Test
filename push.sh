#!/bin/bash
# Script to push to GitHub using a Personal Access Token
# Usage: ./push.sh YOUR_TOKEN

TOKEN=$1

if [ -z "$TOKEN" ]; then
    echo "Usage: ./push.sh YOUR_GITHUB_TOKEN"
    echo ""
    echo "To create a token:"
    echo "1. Go to: https://github.com/settings/tokens/new"
    echo "2. Name it: 'Neural Interface'"
    echo "3. Check 'repo' scope"
    echo "4. Generate and copy the token"
    echo ""
    exit 1
fi

git push https://${TOKEN}@github.com/Ciani1217/Claude-Code-Test.git main
