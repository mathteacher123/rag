#!/bin/bash
# 1. Clean up potential duplicate paths in .bashrc
sed -i '/\.opencode\/bin/d' ~/.bashrc

# 2. Add the verified codespace path permanently
echo 'export PATH="/home/codespace/.opencode/bin:$PATH"' >> ~/.bashrc

# 3. Apply the changes immediately to your current session
export PATH="/home/codespace/.opencode/bin:$PATH"

echo "Success! OpenCode path configured permanently."
