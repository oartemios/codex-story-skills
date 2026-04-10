# Установка

## Установка в Codex Home

```bash
rsync -a ~/dev/AI/codex-story-skills/skills/ ~/.codex/skills/
```

## Замена старого симлинка на реальные файлы

```bash
rm ~/.codex/skills/writer-assistant
rsync -a ~/dev/AI/codex-story-skills/skills/ ~/.codex/skills/
```

## Проверка

```bash
ls -la ~/.codex/skills
```

`writer-assistant` должен отображаться как обычная папка, а не как симлинк.
