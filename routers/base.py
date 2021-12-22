from aiohttp import ClientSession

from api import APIHandler as FroidAPIHandler

api_session = ClientSession()
api_handler = FroidAPIHandler(api_session)
