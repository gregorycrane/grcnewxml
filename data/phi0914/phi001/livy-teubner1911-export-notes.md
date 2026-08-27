# Livy Teubner scaffold export

The exported edition is `phi0914.phi001.teubner1911-lat1`, named for the latest publication year represented by its four Teubner source parts (1911).

## Files

- `phi0914.phi001.teubner1911-lat1.xml` — combined Latin edition
- `phi0914.phi001.__cts__.xml` — matching CTS work inventory entry

These are exports only. No file in `/Users/gcrane/github/canonical-latinLit` was changed.

## Structural decisions

- Removed the EpiDoc schema processing instruction.
- Replaced `div type="textpart" subtype="book|chapter|section"` with transparent `div type="book|chapter|section"` elements.
- Removed the edition and part wrappers so that volume boundaries do not become citation levels.
- Put the edition URN on the immediate `body/@xml:base`: `urn:cts:latinLit:phi0914.phi001.teubner1911-lat1`.
- Replaced the legacy `cRefPattern` declarations with nested `citeStructure` declarations for book, chapter, and section.
- Retained all inherited digital editorial credits and all ten inherited revision entries. Added a separate, explicit credit and revision entry for the automated structural transformation.

## Source-volume milestones

| Milestone | Begins with | Source record | Publication year |
|---|---|---|---:|
| `volume 1` | Book 1 | Part I, Books I–X | 1898 |
| `volume 2` | Periocha 21 (`21s`) | Part II, Books XXI–XXX | 1884 |
| `volume 3` | Periocha 31 (`31s`) | Part III, Books XXXI–XL | 1909 |
| `fascicle 3.2` | Periocha 39 (`39s`) | Part III, second physical fascicle/page-number reset | 1909 |
| `volume 4` | Periocha 41 (`41s`) | Part IV, Books XLI–CXLII, fragments, and index | 1911 |

Each volume milestone and book points back to its `biblStruct` with `@source`. The Part III fascicle is a separate milestone because the supplied XML preserves a second wrapper and page-number reset there, but it links to the same Part III bibliography.

## Validation

- Both exported XML files are well-formed.
- The normalized body text is byte-for-byte equivalent after whitespace normalization to the source edition; no Livy text was added, removed, or corrected.
- All 80 book-level identifiers are unique: 35 surviving books plus 45 periochae.
- The hierarchy contains 1,765 chapters and 20,296 sections.
- There are no remaining `textpart`, edition, or part wrappers and no occurrence of the old `perseus-lat2` identifier.

The source itself warns that its constituent print editions/reprints are not identified with complete precision. The four per-part bibliographic records make the best-supported volume attribution explicit while preserving that inherited warning in `notesStmt`.
