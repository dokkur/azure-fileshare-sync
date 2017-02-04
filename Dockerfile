FROM slacksshbot/alpine-python2
WORKDIR /app
COPY . /app
RUN pip install -r /app/requirements.txt
ENTRYPOINT ["python", "-m", "azure_sync"]
