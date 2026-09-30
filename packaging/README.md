# Fedora package

This fork builds Vencord with the pinned VesktopClaudeBridge and VencordCtrlMute
repositories as source userplugins. The RPM is named `vencord` and installs the
desktop build to `/opt/vencord/dist` and the sidecar to `/opt/vencord/sidecar`.

The Vencord directory includes a `package.json` marker. Vesktop 1.6.7 requires
that marker and the four desktop bundles before it accepts a custom directory;
without it, Vesktop tries to create the marker in `/opt`, which is read-only in
the Flatpak setup.

## Enable for the current user

```sh
vencord-setup enable
```

The helper keeps Vesktop's other settings, sets `vencordDir`, enables the
VesktopClaudeBridge plugin, grants the Flatpak read-only access to
`/opt/vencord`, installs the bundled Vesktop launcher for the current user,
and registers a stdio MCP server named `vencord` in Codex's global
configuration. The launcher runs the Vesktop Flatpak and sets
`StartupNotify=false`; its user-local desktop entry takes precedence over the
Flatpak export. The bridge token stays in the per-user Vesktop config
directory with mode `0600`; its starter sidecar config denies DMs.

Fully quit and restart Vesktop and Codex after enabling. Check the setup with:

```sh
vencord-setup status
codex mcp list
```

To remove the setup and return Vesktop to its bundled Vencord:

```sh
vencord-setup disable
```

The helper restores the original `vencordDir`, plugin toggles, and desktop
launcher while keeping unrelated settings and Codex servers intact. It
preserves launcher edits made after setup. Restart both apps after disabling.

## Build and publish

The Git submodules pin the bridge plugin and sidecar, and the Ctrl Mute plugin,
at reviewed commits. Regenerate the ignored bridge protocol copies before
building:

```sh
npm run sync --prefix external/VesktopClaudeBridge
npx --yes pnpm@11.9.0 install --frozen-lockfile
npx --yes pnpm@11.9.0 testTsc
npx --yes pnpm@11.9.0 build
npm ci --prefix external/VesktopClaudeBridge/sidecar
npm run build --prefix external/VesktopClaudeBridge/sidecar
npm test --prefix external/VesktopClaudeBridge/sidecar
npm prune --prefix external/VesktopClaudeBridge/sidecar --omit=dev
```

Create a release by pushing a tag matching `vencord-v<package-version>-<release>`
(for example, `vencord-v1.15.6-2`). The release workflow builds and
signs the RPM and repository metadata, uploads the RPM to GitHub Releases, and
publishes the DNF repository at `https://x3c.ca/vencord/vencord.repo`.
Manual workflow runs create build artifacts only; only validated release tags
publish to the stable DNF repository. RPMs from earlier tagged releases remain
in the repository so cached metadata and package downgrades continue to work.

The workflow reads its dedicated private signing key from the GitHub Actions
secret `RPM_SIGNING_KEY`; only the public key is tracked in this repository.
