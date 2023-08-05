# -*- coding: utf-8 -*-
__all__ = ["ServiceTestCase"]
import os
import unittest
import json
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from kanjidb.service import configuration, Application

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
CONFIG_CNF = os.path.join(DATA_DIR, "config.cnf")


class ServiceTestCase(AioHTTPTestCase):
    async def get_application(self):
        config = configuration.load(CONFIG_CNF)

        with open(config["service"]["db-file"], "rb") as f:
            content = f.read()
            db = json.loads(content.decode(), encoding="utf8")

        return Application(
            swagger_yml=config["service"]["swagger-yml"],
            swagger_url=config["service"]["swagger-url"],
            base_url=config["service"]["base-url"],
            db=db,
        )

    @unittest_run_loop
    async def test_doc(self):
        resp = await self.client.request("GET", "/api/v1/doc")
        assert resp.status == 200

    @unittest_run_loop
    async def test_api(self):
        resp = await self.client.request("GET", "/api/v1/kanji")
        assert resp.status == 200
        resp = await self.client.request("GET", "/api/v1/kanji/一")
        assert resp.status == 200


if __name__ == "__main__":
    unittest.main()
