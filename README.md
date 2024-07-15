
# Early Warning System

## Description

This project is about an Opendx_28 project and show a demo for all ETL process which use GNU Health as data source and DHIS2 as data destination.
## Installation instructions

Before you start, you need to have `Docker` installed on your computer. All this project is written with `Node.js 20.10` and `Python 3.12`.

### Environment and configuration

To start to use this project, you need to create docker images for `GNU-Health server` and `DHIS2`. For that, go to the appropriate directory and on the terminal, clone this project with this command:

```bash
  git clone https://github.com/AdkMarius/etl_warning_system.git
```
After that, you need to build the images and run the container. At the root of the project, tape these commands:

```bash
  docker build -t 
  docker compose up -d
```
After all containers run successfully, open the project in your IDE. 
### Environment Variables

To run this project, you will need to add the following environment variables to your .env file

#### Frontend directory

Create an .env file at the root of the frontend directory, copy this following code and paste into.

```bash
API_URL='http://127.0.0.1:5000/api'
```

#### Backend directory

As previously, create an .env file at the root of the backend directory, copy this code and paste into.

```bash
DHIS2_API_URL='http://localhost:8080/api'

# GNU Health configuration
GNUHEALTH_HOSTNAME='localhost'
GNUHEALTH_DBNAME='ghs1'
GNUHEALTH_USERNAME='admin'
GNUHEALTH_PASSWORD='opendx28'
GNUHEALTH_PORT='8000'
GNUHEALTH_ORG_UNIT_NAME='Hospital_Agaete'
GNUHEALTH_ORG_UNIT_ID='ib4dMYZzKNU'
```

You should ensure every ports configuration is correct. For that see in Docker desktop or with the command:

```bash
docker ps
```

After all of this, in the backend project, install all the dependencies in the `requirements.txt` file.

In the frontend project, tape these commands:

```bash
npm install
npm run dev
```

After install all of the dependencies as described earlier, you should be able to use it.
