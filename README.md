# spikes

Monorepo for various small experiments.

## Build & test

The build comes in three parts:

- IDE: VSCode devcontainer (_optional_)
- Cross-language build: bazel
- CI: GitHub Actions

You don't have to use VSCode -- you can run everything command-line -- but it's strongly encouraged because of the complex tooling setup; the devcontainer ensures the entire setup is consistent and runs it all under Ubuntu 24.02 ("Noble") regardless of host platform. Especially for the C++ parts of the monorepo build, running them on other operating systems can lead to unexpected behaviors or build failures.

The setup should work for both x86 and ARM hardware. It's tested on Apple M1 (local) and x86 (CI); the local setup runs VSCode on a [colima](https://github.com/abiosoft/colima)-based Docker container with 8 cores and 10gb of memory.

### Using pre-commit

If you are using this project in VSCode, it will install pre-commit hooks in your `.git` directory to run a number of quality checks before you push a new commit. This is automatic, and prevents

VSCode doesn't handle the output and errors from pre-commit very well if you the integrated Git tools, but the same checks can be run manually.

- `pre-commit run`: run all pre-commit checks on the current changelist
- `pre-commit run --all-files`: run all pre-commit checks on all files

## HOWTO guides

Some short guides to common tasks.

### HOWTO: Run pre-commit checks manually

When adding new pre-commit checks or when testing out other development environment changes, you may wish to pro-actively run all pre-commit checks on all files. You can do it this way:

```shell
pre-commit run --all-files
```

### HOWTO: Upgrade pre-commit hooks

To update `.pre-commit-config.yaml` automatically to latest published hook versions, run:

```shell
pre-commit autoupdate
```

### HOWTO: Set up colima for local Docker on MacOS (optional)

The VSCode devcontainer should work with Docker Desktop, Rancher Desktop and Podman Desktop, but the recommended setup on Apple Silicon is [colima](https://github.com/abiosoft/colima). It is fully free and lightweight; you can find a sample Linux template under `.vscode\colima.yaml`.

To set up:

```shell
brew install colima
colima start --edit
```

then save the contents of `colima.yaml` in the editor to create your local VM. VSCode should auto-recognize it; just check out the repo and open in VSCode.

### HOWTO: Install optional upgraded mono font (optional)

Download [JetBrains Mono](https://www.jetbrains.com/lp/mono/) and install locally to activate the custom mono font.
