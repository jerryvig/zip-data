import re
from pathlib import Path
from bs4 import BeautifulSoup


def parse_population_2023(html: str) -> dict[str, int | None]:
    """
    Parse an HTML string (formatted like 78613.html from city-data) and extract
    the "Estimated zip code population in 2023" and "Houses and condos" values.
    """
    soup = BeautifulSoup(html, "html.parser")

    # We'll search the flattened text by lines for robustness against markup differences
    doc_text = soup.get_text("\n", strip=True)
    lines = doc_text.splitlines()

    population_target = re.compile(
        r"estimated\s+zip\s+code\s+population\s+in\s*2023", re.IGNORECASE
    )
    houses_target = re.compile(r"Houses and condos:", re.IGNORECASE)

    population_2023 = None
    houses_and_condos = None

    for i, line in enumerate(lines):
        if population_target.search(line):
            # Try to find a number after the colon ':' on the same line or the next line
            m = re.search(r":\s*([0-9][0-9,]*)", line)
            if not m and i + 1 < len(lines):
                m = re.search(r"([0-9][0-9,]*)", lines[i + 1])
            if m:
                try:
                    population_2023 = int(m.group(1).replace(",", ""))
                except ValueError:
                    population_2023 = None
        elif houses_target.search(line):
            m = re.search(r":\s*([0-9][0-9,]*)", line)
            if not m and i + 1 < len(lines):
                m = re.search(r"([0-9][0-9,]*)", lines[i + 1])
            if m:
                try:
                    houses_and_condos = int(m.group(1).replace(",", ""))
                except ValueError:
                    houses_and_condos = None

        if population_2023 is not None and houses_and_condos is not None:
            break

    return {
        "population_2023": population_2023,
        "houses_and_condos": houses_and_condos,
    }


def main() -> None:
    # Read the HTML file as utf-8 using pathlib.Path
    script_dir = Path(__file__).parent
    html_path = script_dir / "78613.html"
    html = html_path.read_text(encoding="utf-8")
    # Parse and print the result
    result = parse_population_2023(html)
    print(result)


if __name__ == "__main__":
    main()
