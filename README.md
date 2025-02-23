# spikes

Monorepo for various small experiments.

## HOWTO: Run pre-commit checks manually

When adding new pre-commit checks or when testing out other development environment changes, you may wish to pro-actively run all pre-commit checks on all files. You can do it this way:

```shell
pre-commit run --all-files
```

## HOWTO: Upgrade pre-commit hooks

To update `.pre-commit-config.yaml` automatically to latest published hook versions, run:

```shell
pre-commit autoupdate
```

Wherever possible we are going to try and share the tools across Pants and pre-commit, so tool upgrades should be done as part of the re-locking process. (See below.)

## HOWTO: Re-lock dependencies

This project uses [pants](https://pantsbuild.org) for its build process, and it uses the optional facility for hermetic builds where you 'lock' exact dependency versions based on a constraint; these lockfiles are then stored under `3rdparty/**/*.lock` and used by Pants for both tool and library versioning. If there are new patch versions, they will only be picked up after an explicit re-lock, which is done by:

```shell
pants generate-lockfiles
```

which will summarize the added and upgraded modules for you. You then re-run your tests, CI, etc., to ensure the new versions work. This ensures the build is fully isolated from any external changes, including tool upgrades, though the cost of it is that Pants needs to download tools at runtime, which it caches. For wasmtime toolchain plugin we'll do this as well, so upgrading to a new WASM SDK will require a re-locking.

## HOWTO: Install optional upgraded mono font

Download [JetBrains Mono](https://www.jetbrains.com/lp/mono/) and install locally to activate the custom mono font.
