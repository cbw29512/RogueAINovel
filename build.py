import json
import os
import logging

# State-First: Setup logging and define input/output schemas
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
SKELETON_PATH = 'core/skeleton.json'
OUTPUT_DIR = 'build'
OUTPUT_FILE = f'{OUTPUT_DIR}/Chronicles_of_ARCHIMEDES.md'

def compile_tome():
    """Reads the skeleton.json roadmap and stitches all Markdown modules into a single Tome."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    try:
        with open(SKELETON_PATH, 'r') as f:
            skeleton = json.load(f)
            
        final_tome = "# THE CHRONICLES OF ARCHIMEDES-9\n\n"
        final_tome += "*A System Architect's Guide to Human Resilience*\n\n---\n\n"
        
        # 1. Iterate through historical modules based on the JSON roadmap
        for module in skeleton['modules']:
            # Format folder name (e.g., "01_odyssey")
            folder_prefix = f"{module['id']:02d}"
            # Find the matching folder in the modules directory
            for folder_name in os.listdir('modules'):
                if folder_name.startswith(folder_prefix):
                    file_path = f"modules/{folder_name}/chapter_01.md"
                    
                    if os.path.exists(file_path):
                        with open(file_path, 'r', encoding='utf-8') as md_file:
                            final_tome += md_file.read() + "\n\n<div style='page-break-after: always;'></div>\n\n"
                        logging.info(f"Appended Module {module['id']}: {module['title']}")
                    else:
                        logging.warning(f"Missing file for Module {module['id']} at {file_path}")
        
        # 2. Append the Epilogue
        epilogue_path = 'core/finale/epilogue.md'
        if os.path.exists(epilogue_path):
            with open(epilogue_path, 'r', encoding='utf-8') as epi_file:
                final_tome += epi_file.read()
            logging.info("Appended Epilogue: The Global Patch")
            
        # 3. Write the massive tome to the build folder
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as out_file:
            out_file.write(final_tome)
            
        logging.info(f"SUCCESS: Huge Tome compiled at {OUTPUT_FILE}")
        
    except Exception as e:
        logging.error(f"CRITICAL COMPILE ERROR: {e}")

# Big Picture: This script is the final 'Linker'. It takes the individual 
# compiled objects (chapters) and binds them into the executable artifact (the book).
if __name__ == "__main__":
    compile_tome()