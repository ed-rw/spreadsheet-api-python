from fastapi import APIRouter

from .spreadsheets import SpreadsheetsEndpoint

router = APIRouter()

router.get(SpreadsheetsEndpoint.uri)(SpreadsheetsEndpoint.get)
