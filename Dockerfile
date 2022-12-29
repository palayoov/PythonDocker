FROM python
COPY *.* /code/
RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r /code/requirements.txt
WORKDIR /code
CMD ["python","tests3.py"]