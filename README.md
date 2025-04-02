# Datasheet Application Notes plugin for KiCad

This allows calculating application notes parameters from component values, and inserting these into the schematic.

# TODO

- [x] design proper icons
- [x] prepare for future in-schematic editability
  - [x] tag components with a UUID
  - [x] tag components with notes' symbol references
  - [x] tag components with the note name
  - [x] tag the notes text_box (or link to its uuid *after* patching it?): uuid as prop of the first symbol
  - [x] remap symbol UUIDs
- [ ] support schematic variants
- [ ] handle PCBs
- [ ] generate HTML & SVG in a temporary folder (plugin might be in a read-only directory)
- [ ] use a JS library for SI parsing and math?
- [ ] add links to datasheet, Memotech pages?
