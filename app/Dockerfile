FROM python:3.9

WORKDIR /code

COPY ./app/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./fma-metadata/tracks.zip /code

COPY ./app /code

EXPOSE 8501

CMD echo Container starting; python database_init.py; streamlit run app.py