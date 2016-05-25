# rdm-ontology
Repository for managing DI-specific controlled vocabularies, naming schemes and references to external resources that map terms and names onto meanings and definitions.

## usage

1. download the repository

  ```bash
  $ git clone https://github.com/donders-research-data-management/rdm-ontology
  ```

2. convert contents into proper format for CMS.

  ```bash
  $ cd rdm-ontology
  $ make build
  ```

3. validate JSON file against schema

  ```bash
  $ make validate_json
  ```
  
  For validating JSON document, a _schema_ file describing the [JSON schema](http://json-schema.org) the document follows should be provided.  The schema file should be in the same directory as the JSON document.  It should also be named with a prefix the same as the JSON document; and `.schema` as its file extension.

4. create distribution tarball

  ```bash
  $ make dist
  ```
  
5. or, install right into the `$(INSTALL_PREFIX)` defined in the `Makefile`

  ```bash
  $ make install
  ```