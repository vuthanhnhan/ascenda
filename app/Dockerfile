FROM python:3.9

# 
WORKDIR /ascenda

# 
COPY ../requirements.txt /ascenda/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /ascenda/requirements.txt

# 
COPY . /ascenda/app