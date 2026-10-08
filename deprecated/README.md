# Deprecated source files

This directory preserves superseded source files that remain useful for
provenance or comparison but are no longer the live corpus copy.

The directory below `deprecated/` mirrors each file's former path below the
repository root. Files in this tree must not be registered in active CTS
metadata or consumed by corpus builds. Each replacement should be recorded in
the table below before the old file is moved here.

| Deprecated copy | Live replacement | Reason |
| --- | --- | --- |
| `data/tlg0085/tlg007/tlg0085.tlg007.sidgwick1887-com-eng1.xml` | `canonical-pdlrefwk/data/viaf54220216/viaf001/viaf54220216.viaf001.perseus-eng1.xml` (`urn:cts:greekLit:viaf54220216.viaf001.perseus-eng1`) | Sidgwick's commentary is a reference work; the VIAF-based TEI in `canonical-pdlrefwk` is the maintained copy. The Sidgwick Greek edition remains active in `grcnewxml`. |

