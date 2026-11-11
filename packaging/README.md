# Fedora nightly package

`main` is upstream Vencord plus a single commit containing `packaging/` and
`.github/workflows/fedora-nightly.yml`. Nothing else differs from upstream.

The workflow runs every day, on every push to `main`, and on demand. It:

1. merges the latest `Vendicated/Vencord` `main` (in CI only, never pushed),
2. runs `packaging/build.sh`, which copies the latest
   [VesktopClaudeBridge](https://github.com/x3cca/VesktopClaudeBridge) and
   [VencordCtrlMute](https://github.com/x3cca/VencordCtrlMute) into
   `src/userplugins`, builds Vencord and the bridge sidecar, and makes the RPM,
3. signs the RPM and the repository metadata with the `RPM_SIGNING_KEY` secret,
4. deploys the DNF repository to GitHub Pages at <https://x3c.ca/vencord/>.

A scheduled run builds nothing when `source.txt` on the site already matches
the upstream and plugin commits. RPM releases are `<UTC timestamp>.git<sha>`,
so every build counts as newer than the one before it.

## Install

```sh
sudo dnf config-manager addrepo --from-repofile=https://x3c.ca/vencord/vencord.repo
sudo dnf install vencord
vencord-setup enable
```

After that, a normal `sudo dnf upgrade` picks up each new build. Restart
Vesktop to load it. `vencord-setup status` and `vencord-setup disable` check
and undo the per-user setup.

## Build locally

```sh
packaging/build.sh ~/vencord-rpm
sudo dnf install ~/vencord-rpm/vencord-*.rpm
```

The script builds the committed `HEAD` in a throwaway worktree, so it leaves
your checkout untouched. Locally built RPMs are unsigned.

## Updating the fork

To bring local `main` up to date with upstream:

```sh
git fetch upstream && git rebase upstream/main && git push --force-with-lease
```
