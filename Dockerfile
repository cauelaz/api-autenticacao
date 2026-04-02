FROM python:3.8-buster

ENV TZ=America/Sao_Paulo

WORKDIR /usr/src/

COPY ./src ./

RUN pip3 install --upgrade pip

RUN pip3  install --no-cache-dir -r requirements.txt

CMD ["fastapi", "run", "main.py", "--port", "80"]

# CMD ["fastapi", "run", "main.py", "--proxy-headers", "--port