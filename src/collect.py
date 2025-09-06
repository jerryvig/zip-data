import re
from pathlib import Path
from bs4 import BeautifulSoup


def parse_population_2023(html: str) -> dict[str, int | None]:
    """
    Parse an HTML string (formatted like 78613.html from city-data) and extract
    the "Estimated zip code population in 2023" value.
    """
    soup = BeautifulSoup(html, "html.parser")

    # We'll search the flattened text by lines for robustness against markup differences
    doc_text = soup.get_text("\n", strip=True)
    lines = doc_text.splitlines()

    target = re.compile(
        r"estimated\s+zip\s+code\s+population\s+in\s*2023", re.IGNORECASE
    )
    population_2023 = None

    for i, line in enumerate(lines):
        if target.search(line):
            # Try to find a number after the colon ':' on the same line or the next line
            m = re.search(r":\s*([0-9][0-9,]*)", line)
            if not m and i + 1 < len(lines):
                m = re.search(r"([0-9][0-9,]*)", lines[i + 1])
            if m:
                try:
                    population_2023 = int(m.group(1).replace(",", ""))
                except ValueError:
                    population_2023 = None
            break

    return {"population_2023": population_2023}


def main() -> None:
    # Read the HTML file as utf-8 using pathlib.Path
    html_path = Path("./78613.html")
    html = html_path.read_text(encoding="utf-8")
    # Parse and print the result
    result = parse_population_2023(html)
    print(result)


if __name__ == "__main__":
    main()
