![pytest](https://github.com/prabhuwk/manage-github-repo/actions/workflows/main.yml/badge.svg)


# Manage GitHubRepo 

In this we are going to   

1. Create custom command using [click-plugins](https://github.com/click-contrib/click-plugins) module.
    ```shell
   $ github repo --help
    Usage: github repo [OPTIONS] COMMAND [ARGS]...
    
      Manage GitHub Repository
    
    Options:
      --help  Show this message and exit.
    
    Commands:
      create  Create GitHub Repository
      delete  Delete GitHub Repository
    ```

2. Validate `example/sample-repo.yaml` file with [pydantic](https://pydantic-docs.helpmanual.io) model.    

    For Example:  
    If there is typo in `kind`, It will throw validation error.  
    ```shell
    $ github repo create -f example/sample-repo.yaml
    1 validation error for Model
    kind
      GitHubRep is not GitHubRepo (type=assertion_error)
    ```

3. Create github repository using commandline
    ```shell
    $ github repo create -f example/sample-repo.yaml
    prabhuwk/sample-repo successfully created.
    ```
   
    Delete github repository using commandline
    ```shell
    $ github repo delete -f example/sample-repo.yaml
    sample-repo successfully deleted.
    ```

4. Create `manage-github-repo` Docker Image using [Github Actions](https://docs.github.com/en/actions).  


5. Run tests using [pytest](https://docs.pytest.org/en/7.1.x/contents.html).

   ```shell
   $ pytest tests/
   ================ test session starts =======================
   platform darwin -- Python 3.9.10, pytest-7.1.1, pluggy-1.0.0
   plugins: cov-3.0.0
   collected 5 items                                                                                                                                                                                             
   
   tests/test_github_repo.py .....                       [100%]                                                            
   ================ 5 passed in 0.18s =========================
   ```
