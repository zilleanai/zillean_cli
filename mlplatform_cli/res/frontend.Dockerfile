FROM gitlab.chriamue.de:4567/mlplatform/mlplatform_frontend

COPY mlplatform-domain.yml mlplatform-domain.yml
RUN mlplatform-cli domain install_requirements mlplatform-domain.yml
COPY frontend/app/comps frontend/app/comps