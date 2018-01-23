# Configurable content for the Donders Repository portal

Repository for managing DI-specific controlled vocabularies, naming schemes and references to external resources that map terms and names onto meanings and definitions.

## Content editing

Please refer to [this README](README.editor.md).

## Test

1. download the repository

  ```bash
  $ git clone https://github.com/donders-research-data-management/rdm-configurable-content-donders
  ```

2. create distribution zip file 

  ```bash
  $ cd rdm-configurable-content-donders
  $ make -f tools/Makefile dist
  ```

  This makefile target will do the following things in a sequencial order:

  - convert markdown-formatted files into HTML snippets (e.g. the privacy_policy page)
  - convert CSV files into JSON documents (e.g. the controlled vocabularies of keywords)
  - validate JSON documents as long as the corresponding `.schema` file is presented
  - create the release zip file (`rdm-configurable-content-*.zip`) taking into account only the needed files (e.g. derived HTML snippets and JSON documents) for deployment
  - walk through the `external_urls.json` file in the release zip, check whether the URLs are (or will be) available after the deployment
  
## Deployment

The deployment will be triggered by changes in the `release` branch of the repository. After the changes in the `master` branch is confirmed, one can update the `release` branch using the following git commands:

```bash
$ git checkout release
$ git rebase master
$ git push
```
