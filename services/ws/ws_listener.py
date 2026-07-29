import asyncio
import json
import allure


class WSListener:
    def __init__(self, websocket):
        self.ws = websocket
        self.messages = []

    async def wait_for_event(self, filter_params: dict, callback=None, timeout_sec=5):
        start_time = asyncio.get_event_loop().time()

        while True:
            if asyncio.get_event_loop().time() - start_time > timeout_sec:
                raise asyncio.TimeoutError(f"Таймаут! Не дождались события {filter_params}")

            try:
                raw_message = await asyncio.wait_for(self.ws.recv(), timeout=1.0)
                payload = json.loads(raw_message)
            except asyncio.TimeoutError:
                continue

            if self._match_filter(payload, filter_params):
                with allure.step(f"WS поймал нужное событие: {filter_params}"):
                    print(f"\n[WS EVENT RECEIVED]: {payload}")

                self.messages.append(payload)
                if callback:
                    callback(payload)
                return payload

    @staticmethod
    def _match_filter(data: dict, filter_dict: dict) -> bool:
        for key, expected_value in filter_dict.items():
            if data.get(key) != expected_value:
                return False
        return True
