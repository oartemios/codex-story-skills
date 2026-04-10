# Install

## Install into Codex Home

```bash
rsync -a ~/dev/AI/codex-story-skills/skills/ ~/.codex/skills/
```

## Replace Existing Symlink With Real Files

```bash
rm ~/.codex/skills/writer-assistant
rsync -a ~/dev/AI/codex-story-skills/skills/ ~/.codex/skills/
```

## Verify

```bash
ls -la ~/.codex/skills
```

`writer-assistant` should appear as a normal directory, not a symlink.
