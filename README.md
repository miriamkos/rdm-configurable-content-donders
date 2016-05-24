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

  Note: for the moment, the actual validation is not implemented yet.

  ```bash
  $ make validate_json
  ```

4. create distribution tarball

  ```bash
  $ make dist
  ```
