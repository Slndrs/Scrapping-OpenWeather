# From the source image #python
FROM python:3.6-slim
# Identify maintainer
LABEL maintainer = "solene.druais@gmail.com"
# Set the default working directory
WORKDIR /app/
COPY tempFrance.py requirements.txt city.list.json /app/
RUN pip install -r requirements.txt
CMD ["python","./tempFrance.py"]
# When the container starts, run this
ENTRYPOINT python ./tempFrance.py
