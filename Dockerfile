FROM python:3
RUN pip install django asynctest asyncio-redis hiredis coverage
ADD . /app
RUN pip install /app