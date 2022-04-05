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
