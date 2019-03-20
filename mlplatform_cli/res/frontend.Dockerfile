FROM gitlab.chriamue.de:4567/mlplatform/mlplatform_frontend

COPY mlplatform-domain.yml mlplatform-domain.yml
RUN mlplatform-cli domain install_requirements mlplatform-domain.yml --no_py
COPY frontend/app/comps frontend/app/comps
COPY routes.js frontend/app/routes.js
COPY NavBar.js frontend/app/components/Nav/NavBar.js
