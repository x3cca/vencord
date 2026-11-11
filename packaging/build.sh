#!/usr/bin/env bash
# Builds the vencord RPM from the committed HEAD plus the latest userplugins.
# Usage: packaging/build.sh [output-dir]
set -euo pipefail

repo=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
out=$(realpath -m "${1:-${XDG_CACHE_HOME:-$HOME/.cache}/vencord-rpm}")
work=$(mktemp -d)
trap 'git -C "$repo" worktree remove --force "$work/vencord" 2>/dev/null || true; rm -rf "$work"' EXIT

git -C "$repo" worktree add --detach "$work/vencord" HEAD
src="$work/vencord"
cd "$src"

# Userplugins always build from the default branch of their repos.
git clone --depth 1 https://github.com/x3cca/VesktopClaudeBridge.git "$work/bridge"
git clone --depth 1 https://github.com/x3cca/VencordCtrlMute.git "$work/ctrlmute"
npm run sync --prefix "$work/bridge"
mkdir -p src/userplugins
cp -a "$work/bridge/plugin" src/userplugins/VesktopClaudeBridge
cp -a "$work/ctrlmute" src/userplugins/VencordCtrlMute
rm -rf src/userplugins/VencordCtrlMute/.git

pnpm=(npx --yes "$(node -p "require('./package.json').packageManager")")
"${pnpm[@]}" install --frozen-lockfile
"${pnpm[@]}" build

sidecar="$work/bridge/sidecar"
npm ci --prefix "$sidecar"
npm run build --prefix "$sidecar"
npm prune --prefix "$sidecar" --omit=dev

version=$(node -p "require('./package.json').version")
release=${VENCORD_RELEASE:-$(date -u +%Y%m%d%H%M).git$(git rev-parse --short HEAD)}

stage="$work/stage/vencord"
mkdir -p "$stage/sidecar" "$stage/share/applications"
cp -a dist "$stage/dist"
cp packaging/vencord-package.json "$stage/dist/package.json"
cp -a "$sidecar/dist" "$sidecar/node_modules" "$sidecar/package.json" "$stage/sidecar/"
cp packaging/dev.vencord.Vesktop.desktop "$stage/share/applications/"
cp packaging/vencord-setup "$stage/"
cp LICENSE "$stage/LICENSE-VENCORD"
cp "$work/bridge/LICENSE" "$stage/LICENSE-VESKTOP-CLAUDE-BRIDGE"

rpmroot="$work/rpmbuild"
mkdir -p "$rpmroot/SOURCES" "$out"
tar -C "$work/stage" -czf "$rpmroot/SOURCES/vencord.tar.gz" vencord
rpmbuild -bb \
    --define "_topdir $rpmroot" \
    --define "_rpmdir $out" \
    --define "_build_name_fmt %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm" \
    --define "vencord_version $version" \
    --define "vencord_release $release" \
    packaging/vencord.spec

echo "Built $out/vencord-$version-$release.noarch.rpm"
