# Parser:
- Parses map file in a data structure and partially validates it so far
[X] fixed most issues I hope...
[X] missing parse_connections
[X] parse_map is not storing data in the dict properly (see chat)
[x] implement the rest of parse_map
[X] Reestructure Parser:
    [X] Create Map object and store map data there instead of in Parser 
    [X] Modify Parser so that it returns a Map object
[ ] Run more tests with the invalid and valid maps
[ ] Not printing line number on error messages idk why

- Might need fixing:
    [ ] Check for dashes AND SPACES on zone names! 
    [ ] Check for repeated names while parsing? Bc the dict might simply 
        replace an old key if I try to add one with a repeated name?
    [ ] Ensure zones are listed before connections


# Validation:
[ ] Create a separate Validate module to further validate Map object
[ ] Move some validation logic from Parser to Validate
    (keep in parser only what is necessary for it to work)

# General
[ ] think about project structure:
    - What should be a package with init?
    - How to organize directories?
[ ] choose algorithm(s)
[ ] decide graph's structure
