On Linux:

1. Update RST section in README.md in this directory
2. Run `make html`
3. Run `python generate_md.py`
4. Replace the README.md in the base directory with the generated _build/README_OUT.md 
   (It will probably require some cleanup and reformatting)