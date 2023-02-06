
# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10.0
ENV PYTHONUNBUFFERED=1
RUN git clone https://github.com/Paillat-dev/presentator.git
RUN pip install -r /presentator/requirements.txt
RUN apt-get update
RUN apt-get install -y chromium # for marp
WORKDIR /presentator
RUN wget https://github.com/marp-team/marp-cli/releases/download/v2.3.0/marp-cli-v2.3.0-linux.tar.gz
RUN tar -xvf marp-cli-v2.3.0-linux.tar.gz
RUN rm marp-cli-v2.3.0-linux.tar.gz
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /presentator
USER appuser
CMD ["python", "main.py"]