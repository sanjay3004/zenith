FROM python:3.8-slim
RUN apt-get update && apt-get install

RUN apt-get install -y \
  dos2unix \
  libpq-dev \
  libmariadb-dev-compat \
  libmariadb-dev \
  gcc \
  && apt-get clean

RUN python -m pip install --upgrade pip

COPY . /api
WORKDIR /api
ENV FLASK_APP app.py
RUN pip install -r requirements.txt
# RUN flask db init
# RUN flask db migrate
# RUN flask db upgrade
ENTRYPOINT ["python"]
CMD ["application.py"]
