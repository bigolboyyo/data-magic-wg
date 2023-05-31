from flask import Flask, request, abort, g
from app import app

if __name__ == "__main__":
    app.run(debug=True)
