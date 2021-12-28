FROM python:3.6.9

WORKDIR /Resolve-IT

COPY . .

RUN pip install -r /Resolve-IT/requirements/common.in

ENTRYPOINT ["python", "/Resolve-IT/resolveit/app.py"]
