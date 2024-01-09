FROM python:3.11-alpine as base

RUN pip install --upgrade pip pipenv
RUN apk update && apk add --no-cache --update git

COPY Pipfile* ./
RUN pipenv install --deploy --system --ignore-pipfile --verbose

FROM python:3.11-alpine as deploy

COPY --from=base . .
COPY . .

EXPOSE 8000

CMD ["uvicorn", "--host", "0.0.0.0", "src.main:app"]