FROM python:3.10

WORKDIR /mack-ops

COPY ./requirements.txt .

RUN pip install -r requirements.txt

CMD ["/bin/bash"]
