# Minx reloading web server

## Development

This project uses Hatch. This means you don't really make environments. 
However, an IDE might want an environment. For that purpose, the Hatch `default` 
environment bundles everything needed for development, testing, docs, etc.

The IDE needs the path to this environment. `hatch env create` makes the 
default environment. `hatch env find` provides the full directory path 
to this environment.