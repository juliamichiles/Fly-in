# Parser:
- Parses map file in a data structure and partially validates it so far
[X] fixed most issues I hope...
[X] missing parse_connections
[X] parse_map is not storing data in the dict properly (see chat)
[ ] implement the rest of parse_map
[ ] HAS ERRORS! (see chat)
[ ] Actually test everything
[ ] Reestructure Parser:
    [ ] Create Map object and store map data there instead of in Parser 
    [ ] Modify Parser so that it returns a Map object
    [ ] Create a separate Validate module to further validate Map object
    [ ] Move some validation logic from Parser to Validate
        (keep in parser only what is necessary for it to work)

# General
[ ] add a validate method to parser or create another
[ ] think about project structure:
    - What should be a package with init?
    - How to organize directories?
[ ] choose algorithm(s)
[ ] decide graph's structure
