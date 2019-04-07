FROM zilleanai/zillean_backend
USER root
COPY zillean-domain.yml zillean-domain.yml
RUN zillean-cli domain install_requirements zillean-domain.yml --no_js

USER flask
COPY unchained_config.py unchained_config.py
COPY routes.py backend/routes.py
COPY bundles bundles
