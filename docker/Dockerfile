FROM ubuntu:20.04

WORKDIR /app

COPY ../. .

# Ignore installation prompts
ENV DEBIAN_FRONTEND=noninteractive

# INSTALL BACKEND REQUIREMENTS
# ==================================

RUN apt-get update -y && apt-get upgrade -y && apt-get install -y \
  python3 \
  pip

RUN pip install -r src/server/requirements.txt

# INSTALL FRONTEND REQUIREMENTS
# ==================================

RUN apt-get update -y && apt-get upgrade -y && apt-get install -y \
  ca-certificates \
  curl \
  gnupg

# Install latest version of node
RUN mkdir -p /etc/apt/keyrings
RUN curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
RUN NODE_MAJOR=20 && echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list
RUN apt-get update -y && apt-get upgrade -y && apt-get install -y nodejs

# Disable next telemetry
RUN npx next telemetry disable

RUN cd src/client && npm install