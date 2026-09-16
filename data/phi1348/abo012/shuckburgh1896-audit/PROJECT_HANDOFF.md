# Shuckburgh Augustus handoff

Read README.md and the JSON review inventories first. Preserve existing corpus/pipeline work. Only the commentary has been installed; the complete Latin and ancillary OCR are archived for future processing.

Reproduction scripts are in `scripts/`; their original workspace is `work/shuckburgh`. Processing order: split.py, extract.py, prepare_notes.py, notes.py, review.py, find_openings.py, add_openings.py, correct.py, final_review.py, build_xml.py, mark_references.py, validate.py, audit.py. The original parsed witness page JSON files are needed beside the scripts. Scripts use workspace-relative paths and are development tools, not a standalone relocatable package. The original two OCR files and source hashes are included.

Before treating this edition as proofread, resolve the five incomplete note openings, review Greek OCR against images, inspect displaced column text, and verify provisional section targets. Never replace source wording with the reference Latin to improve an alignment score.
