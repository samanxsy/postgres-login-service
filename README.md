# Login Service with Flask, Postgres, and Docker
[![CI](https://github.com/samanxsy/postgres-user-login/actions/workflows/ci.yaml/badge.svg)](https://github.com/samanxsy/postgres-user-login/actions/workflows/ci.yaml)
[![Known Vulnerabilities](https://snyk.io/test/github/samanxsy/postgres-login-service/badge.svg?style=flat-square)](https://snyk.io/test/github/samanxsy/postgres-login-service)
[![Python 3.10](https://img.shields.io/badge/Python-3.10-brown.svg)](https://shields.io/)
[![License](https://img.shields.io/badge/License-MIT-skyblue.svg)](https://mit-license.org/)

A Login service created using Python, and PostgreSQL as database. Under development

## Features
- User Registration and Login functionality
- Secure password storage and hashing
- Session management using Flask-session
- PostgreSQL database integration for storing user information

## Prerequisites
- Docker
- Docker Compose
- Postgres
- Python

## Getting Started using Dockerfiles
```
git clone <repo-ssh/https-url>
cd <project-directory>
docker-compose build && docker compose up
```

## App view

![Screenshot from 2023-05-29 16-42-04](https://github.com/samanxsy/postgres-login-system/assets/118216325/226780e8-41ba-4df5-8a31-712ba9a1221e)
![Screenshot from 2023-05-29 16-43-09](https://github.com/samanxsy/postgres-login-system/assets/118216325/0b871391-8de9-48fe-b95f-aa9adea7df34)

## Configuration
The applications configuration can be modified through the environment variables defined in the `docker-compose.yaml`

- SESSION_KEY: Make sure to use a secure and random value for the session management. you can store it as a shell variable using command below in Linux/macOS:
```
export SESSION_KEY=<random-value>
```
