import connexion
import json
from flask import Response


def status_change__put():
    return connexion.request.json, 200
