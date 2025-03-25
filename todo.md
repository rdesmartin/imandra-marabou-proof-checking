# Refactor proof tree construction / proof checking to separate proof tree validation and verification

- [ ] run integration tests to make sure that algorithm still works after changes
    - [ ] fix json_decoder to work with new Split and Constraint types
    - [ ] fix algorithm to work with new Split and Constraint types
    - [ ] run tests without bound lemmas
    - [ ] run tests with bound lemmas
- [ ] change tightening types with type constructors
    - [ ] define new type
    - [ ] change proof tree parsing
    - [ ] change algorithm
    - [ ] run integration tests

- [ ] splits checking at build time
    - [ ] add split validation in parser
    - [ ] change split verfication in checker

- [ ] bound lemmas
    - [ ] pass constraints in bound lemma parser
    - [ ] match constraint during parsing
    - [ ] bound lemma type?