FROM python:3.9

WORKDIR /code

COPY ./app/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./data/fma-metadata/tracks_small.zip /code
COPY ./data/vectors_test_data.zip /code
COPY ./app /code

EXPOSE 8501

CMD echo Initializing Database.; python -u database_init.py; streamlit run app.py