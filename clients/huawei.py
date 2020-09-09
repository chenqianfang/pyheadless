import asyncio
import os
import time

import redis

from libs.base_huawei import BaseHuaWei


class HuaWei(BaseHuaWei):

    def __init__(self):
        super().__init__()

    async def handler(self, username, password, **kwargs):
        self.logger.info(f'{username} start login.')
        await self.page.waitForSelector('#personalAccountInputId .tiny-input-text', {'visible': True})
        await self.page.type('#personalAccountInputId .tiny-input-text', username)
        await asyncio.sleep(0.5)
        await self.page.type('#personalPasswordInputId .tiny-input-text', password)
        await self.page.click('#btn_submit')
        await asyncio.sleep(5)

        await self.sign_task()

        await self.delete_project()
        await self.delete_api()
        await self.delete_api_group()

        await self.start(**kwargs)

        await self.regular()

        await self.print_credit(username)

        redis_password = os.environ.get('REDIS_PASSWORD')
        k = f'{username}_post_reply'
        r = redis.Redis(host='redis-18138.c1.asia-northeast1-1.gce.cloud.redislabs.com', port=18138,
                        password=redis_password)
        self.logger.info(r.get(k))
        if not r.get(k):
            self.logger.info('post reply.')
            await self.post_reply()
            r.set(k, time.strftime('%Y-%m-%d %H:%M:%S'), 3600 * 6)

        await asyncio.sleep(1)
