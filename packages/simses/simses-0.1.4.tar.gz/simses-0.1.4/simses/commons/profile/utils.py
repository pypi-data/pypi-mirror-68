import sys


def get_header_from(filename: str) -> dict:
    """
    Extracts header from given file

    Attention: Only searches in the first ten lines for a header!

    Parameters
    ----------
    filename :

    Returns
    -------
    dict:
        header with key/value pairs

    """
    header: dict = dict()
    with open(filename, 'r', newline='') as file:
        line = file.readline()
        line_count: int = 0
        while True:
            if '#' in line:
                try:
                    key_raw, entry_raw = line.split(sep=':', maxsplit=1)
                    key = key_raw.strip('# ')
                    entry = entry_raw.strip()
                    header[key] = entry
                except ValueError:
                    sys.stderr.write('WARNING: Could not interpret ' + line)
                    sys.stderr.flush()
            line = file.readline()
            if line_count > 10:
                break
            else:
                line_count += 1
    return header
