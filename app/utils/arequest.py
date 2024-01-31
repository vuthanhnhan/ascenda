import aiohttp

class arequest:
    @staticmethod
    async def get(url, params= None):
        session_timeout = aiohttp.ClientTimeout(total=None,sock_connect=5,sock_read=5)
        async with aiohttp.ClientSession(timeout=session_timeout, trust_env=True) as session:
            async with session.get(url, params=params, allow_redirects=False, timeout=5) as resp:
                try:
                    if resp.status != 200:
                        # @Todo: Logging error
                        return None
                    response = await resp.json()
                except Exception as e:
                    print('Exceptions get arequest: ', e)
                    response = {'error': e}
        return response