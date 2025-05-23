import os
import zipfile
import logging

def extract_xccdf_from_zip(zip_path: str, output_dir: str = "cklb_proc/xccdf_lib"):
    """
    Extracts any file matching '*-xccdf.xml' from a ZIP archive into the output directory,
    flattening the path to avoid nested directories. Deletes the ZIP if successful.
    """
    if not zipfile.is_zipfile(zip_path):
        logging.error(f"Not a valid zip file: {zip_path}")
        return None

    os.makedirs(output_dir, exist_ok=True)
    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            matching = [f for f in zf.namelist() if f.endswith("-xccdf.xml")]
            if not matching:
                logging.warning(f"No '-xccdf.xml' file found in {zip_path}")
                return None

            extracted_paths = []
            for xccdf_file in matching:
                logging.info(f"Extracting {xccdf_file} from {os.path.basename(zip_path)}")
                out_path = os.path.join(output_dir, os.path.basename(xccdf_file))
                with zf.open(xccdf_file) as source, open(out_path, 'wb') as target:
                    target.write(source.read())
                extracted_paths.append(out_path)

        os.remove(zip_path)
        logging.info(f"Deleted original ZIP: {os.path.basename(zip_path)}")
        return extracted_paths
    except Exception as e:
        logging.error(f"Failed to extract XCCDF from {zip_path}: {e}")
        return None