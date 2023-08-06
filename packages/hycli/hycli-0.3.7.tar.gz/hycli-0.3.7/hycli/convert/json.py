import os
import json

from concurrent.futures import ThreadPoolExecutor, as_completed

import click
from filetype import guess

from ..services.requests import extract_invoice
from .commons import read_pdf, get_filenames


def convert_to_json(path, extractor_endpoint, token, workers):
    files = get_filenames(os.path.join(os.getcwd(), path))

    with ThreadPoolExecutor(max_workers=workers) as exe:
        jobs = {
            exe.submit(
                extract_invoice,
                read_pdf(str(filename)),
                extractor_endpoint,
                guess(str(filename)).mime,
                token,
            ): filename
            for filename in files
            if guess(str(filename)).mime
        }
        label = f"Converting {len(jobs)} invoices"
        with click.progressbar(jobs, label=label) as bar:
            for idx, future in enumerate(as_completed(jobs)):
                file_name = str(jobs[future]).split("/")[-1]
                try:
                    response = future.result(timeout=300)

                except Exception as e:
                    print(f"Error: {e}")

                with open(file_name.split(".")[0] + ".json", "w") as f:
                    json.dump(response, f)

                bar.update(1)
