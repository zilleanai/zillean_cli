FROM gitlab.chriamue.de:4567/mlplatform/mlplatform_backend
USER root
RUN pip install git+https://gitlab.chriamue.de/mlplatform/mlplatform_cli.git
COPY mlplatform-domain.yml mlplatform-domain.yml
RUN mlplatform-cli domain install_requirements mlplatform-domain.yml

COPY --chown=flask unchained_config.py unchained_config.py
COPY --chown=flask bundles bundles

USER flask
