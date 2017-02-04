run:
```
AZURE_STORAGE_ACCOUNT=account AZURE_STORAGE_ACCESS_KEY=key python -m azure_sync ./local/path sharename[/remote/path]
```

run docker container:
```
docker run -i -t -e AZURE_STORAGE_ACCOUNT=account -e AZURE_STORAGE_ACCESS_KEY=key -v /local/dir:/container/dir dokkur/azure-fileshare-sync /container/dir fileshare[/remote/dir]
```
