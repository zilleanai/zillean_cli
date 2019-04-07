FROM zilleanai/zillean_frontend

COPY zillean-domain.yml zillean-domain.yml
RUN zillean-cli domain install_requirements zillean-domain.yml --no_py
COPY frontend/app/comps frontend/app/comps
COPY routes.js frontend/app/routes.js
COPY NavBar.js frontend/app/components/Nav/NavBar.js
