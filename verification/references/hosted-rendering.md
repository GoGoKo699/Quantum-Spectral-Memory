# Checking the mathematics displayed on GitHub

The [hosted-mathematics workflow](../../.github/workflows/hosted-math.yml) checks the actual GitHub pages for one exact source commit. It uses an anonymous Chromium context at viewport widths 1440 and 760 pixels. Its repository permission is `contents: read`; checkout credentials are not persisted, and the browser receives no signed-in session.

The collector inventories every tracked Markdown page in that commit, compiles each recognized source formula to reference MathML, then compares it with the MathML supplied by GitHub. It checks expression counts, mathematical structure, scripts, fractions, relations, equation labels and bounded display geometry. HTML captures, screenshots, source inventories and the report are retained as a temporary workflow artifact, including when a check fails.

For a local run, install Node.js 18 or later, Python 3.10 or later, Git, Playwright 1.56.1 and MathJax 3.2.1. Install Chromium with Playwright. Set `NODE_PATH` to the directory containing those temporary Node dependencies, then run:

```bash
node verification/hosted/capture_hosted_math.cjs \
  --root /absolute/path/to/checkout \
  --repository GoGoKo699/Quantum-Spectral-Memory \
  --revision FULL_40_CHARACTER_COMMIT \
  --output /absolute/path/to/new-evidence-directory
```

The revision must already be available on public GitHub. Each attempt uses a new output directory so earlier failures remain distinguishable. The default scope includes all tracked Markdown files, rather than only the headline equations.

A passing report establishes agreement for the observed source, host and viewports. Screenshots still need human inspection for mathematical readability, figures, tables and navigation. The check does not verify scientific proofs, guarantee future rendering, or establish compatibility with every browser. Temporary CI artifacts are not a permanent archive.

[Finite scientific checks](../README.md) · [Repository overview](../../README.md)
