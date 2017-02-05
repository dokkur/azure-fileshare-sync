run:
```
AZURE_STORAGE_ACCOUNT=account AZURE_STORAGE_ACCESS_KEY=key python -m src.azure_sync ./local/path sharename[/remote/path]
```


run docker container:
```
docker run -i -t -e AZURE_STORAGE_ACCOUNT=account -e AZURE_STORAGE_ACCESS_KEY=key -v /local/dir:/container/dir dokkur/azure-fileshare-sync /container/dir fileshare[/remote/dir]
```


run swanageer sync:
```
AZURE_STORAGE_ACCOUNT=account AZURE_STORAGE_ACCESS_KEY=key python -m src.swanager_sync /path/to/swanager.json sharename[/remote/path]
```


run swanager sync container:
```
docker run -i -t -e AZURE_STORAGE_ACCOUNT=account -e AZURE_STORAGE_ACCESS_KEY=key -v /local/dir:/container/path --entrypoint="" azure-fileshare-sync python -m src.swanager_sync /container/path/swanager.json sharename[/remote/path]
```
