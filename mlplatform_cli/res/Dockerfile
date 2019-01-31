FROM gitlab.chriamue.de:4567/mlplatform/mlplatform_backend
USER root
RUN pip install git+https://gitlab.chriamue.de/mlplatform/mlplatform_cli.git
COPY . .
RUN mlplatform-cli domain install_requirements mlplatform-domain.yml
