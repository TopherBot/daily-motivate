# daily-motivate

A **tiny** command‑line utility that prints a random motivational quote.
Optionally it can fire a desktop notification (macOS, Linux, Windows).

## Features
- No external dependencies (uses only the Python standard library).
- 20+ curated quotes stored right in the script.
- `--notify` flag triggers a native OS notification.
- Works on Python 3.8+.

## Installation
```bash
# Clone the repo
git clone https://github.com/yourname/daily-motivate.git
cd daily-motivate

# Make the script executable (optional)
chmod +x motivator.py
```

## Usage
```bash
# Print a quote to stdout
python motivator.py

# Show a desktop notification (if supported)
python motivator.py --notify
```

## Development
Feel free to add more quotes or extend the notification logic.
Run the tiny test suite with:
```bash
python -m unittest motivator.py
```

## License
MIT – see the LICENSE file in the repository.
