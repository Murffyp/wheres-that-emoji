# Where's That Emoji? 🔍

You know it exists. You just can't find it. **Where's That Emoji?** fixes that.

A lightweight, self-hosted emoji search tool. Fuzzy search across 5,200+ emojis by name, keyword, or description — click to copy, done. No accounts, no cloud, no nonsense.

---

# Features

- Fuzzy search across 5,200+ emojis
- Filter by group and subgroup
- Click any emoji to copy it to your clipboard
- Runs entirely locally — no external dependencies at runtime
- On a Raspberry Pi 5:
    - 57 Mb image
    - Builds in UNDER 60 seconds

---

# Instructions

## 1) Clone & Build

### Clone
```bash
git clone https://github.com/Murffyp/wheres-that-emoji.git
```
### Build
```bash
cd wheres-that-emoji
docker build -t wheres-that-emoji:latest .
```

### Run
In the build folder:
```bash
docker compose up -d 
```

Then open [http://localhost:7700](http://localhost:7700)

---

## Docker Compose

```yaml
services:
  wheres-that-emoji:
    image: wheres-that-emoji:latest
    restart: always
    ports:
      - "7700:7700"
    volumes:
      - ./data/emojis.json:/app/data/emojis.json:ro
```

---

## Build Notes

| Environment | Build Time |
|---|:--:|
| &nbsp; Raspberry Pi 5 (8GB, ARM64) &nbsp; | < 60 seconds |
| Laptop / Desktop |&nbsp; Well under a minute &nbsp;|

Built on `python:3.12-alpine` — lean, fast build, small image.

---

## Usage

1. Type anything into the search box — emoji name, keyword, category
2. Optionally filter by group
3. Click an emoji to copy it
4. Paste it wherever you need it
5. DONE!