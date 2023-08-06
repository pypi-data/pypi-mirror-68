import json
from unittest.mock import patch, MagicMock
from unittest import TestCase

from redis import Redis
import requests
import requests_mock
from requests.exceptions import HTTPError

from allianceauth import __title__ as AUTH_TITLE, __url__, __version__

from ..client import DiscordClient, DURATION_CONTINGENCY, DEFAULT_BACKOFF_DELAY
from ..exceptions import DiscordRateLimitExhausted, DiscordTooManyRequestsError
from ...utils import set_logger_to_file

logger = set_logger_to_file(
    'allianceauth.services.modules.discord.discord_client.client', __file__
)

MODULE_PATH = 'allianceauth.services.modules.discord.discord_client.client'
API_BASE_URL = 'https://discordapp.com/api/'
TEST_GUILD_ID = 123456789012345678
TEST_BOT_TOKEN = 'abcdefhijlkmnopqastzvwxyz1234567890ABCDEFGHOJKLMNOPQRSTUVWXY'
TEST_USER_ID = 198765432012345678
TEST_USER_NAME = 'John Doe'
TEST_ROLE_ID = 654321012345678912

TEST_ROUTE_KEY = 'abc123'

TEST_RETRY_AFTER = 3000

DEFAULT_REQUEST_HEADERS = {
    'User-Agent': f'{AUTH_TITLE} ({__url__}, {__version__})',
    'accept': 'application/json',
    'authorization': 'Bot ' + TEST_BOT_TOKEN
}

# default mock redis client to use
mock_redis = MagicMock(**{
    'get.return_value': None,
    'pttl.return_value': -1,
})


class DiscordClient2(DiscordClient):
    """Variant that overwrites lua wrappers with dummies for easier testing"""

    def _redis_set_if_longer(self, name: str, value: str, px: int):
        return True

    def _redis_decr_or_set(self, name: str, value: str, px: int):
        return 5


class TestBasicsAndHelpers(TestCase):

    def test_can_create_object(self):
        client = DiscordClient(TEST_BOT_TOKEN, mock_redis)
        self.assertIsInstance(client, DiscordClient)
        self.assertEqual(client.access_token, TEST_BOT_TOKEN)

    def test_repr(self):
        client = DiscordClient(TEST_BOT_TOKEN, mock_redis)
        expected = 'DiscordClient(access_token=...UVWXY)'
        self.assertEqual(repr(client), expected)

    def test_can_set_rate_limiting(self):
        client = DiscordClient(TEST_BOT_TOKEN, mock_redis, is_rate_limited=False)
        self.assertFalse(client.is_rate_limited)

        client = DiscordClient(TEST_BOT_TOKEN, mock_redis, is_rate_limited=True)
        self.assertTrue(client.is_rate_limited)

    def test_sanitize_role_name(self):
        client = DiscordClient(TEST_BOT_TOKEN, mock_redis)
        role_name_input = 'x' * 110
        role_name_expected = 'x' * 100                
        result = client._sanitize_role_name(role_name_input)
        self.assertEqual(result, role_name_expected)

    @patch(MODULE_PATH + '.caches')
    def test_use_default_redis_if_none_provided(self, mock_caches):
        my_redis = MagicMock(spec=Redis)
        mock_default_cache = MagicMock(**{'get_master_client.return_value': my_redis})
        my_dict = {'default': mock_default_cache}
        mock_caches.__getitem__.side_effect = my_dict.__getitem__
                
        client = DiscordClient(TEST_BOT_TOKEN)
        self.assertTrue(mock_default_cache.get_master_client.called)
        self.assertEqual(client._redis, my_redis)

    @patch(MODULE_PATH + '.caches')
    def test_raise_exception_if_default_cache_is_not_redis(self, mock_caches):
        my_redis = MagicMock()
        mock_default_cache = MagicMock(**{'get_master_client.return_value': my_redis})
        my_dict = {'default': mock_default_cache}
        mock_caches.__getitem__.side_effect = my_dict.__getitem__
                
        with self.assertRaises(RuntimeError):
            DiscordClient(TEST_BOT_TOKEN)
        
        self.assertTrue(mock_default_cache.get_master_client.called)        
        

@requests_mock.Mocker()
class TestOtherMethods(TestCase):
   
    def setUp(self):
        self.client = DiscordClient2(TEST_BOT_TOKEN, mock_redis)
        self.headers = DEFAULT_REQUEST_HEADERS

    def test_user_get_current(self, requests_mocker):        
        expected = {'id': "123456"}
        headers = {
            'accept': 'application/json', 
            'authorization': 'Bearer accesstoken'
        }
        requests_mocker.register_uri(
            'GET',
            f'{API_BASE_URL}users/@me',
            request_headers=headers,
            json=expected
        )
        client = DiscordClient2('accesstoken', mock_redis)
        result = client.current_user()
        self.assertDictEqual(result, expected)

    def test_guild_create_role(self, requests_mocker):
        role_name_input = 'x' * 120
        role_name_used = 'x' * 100
        expected = {'name': role_name_used}

        def data_matcher(request):
            return (json.loads(request.text) == expected)
                 
        requests_mocker.post(            
            f'{API_BASE_URL}guilds/{TEST_GUILD_ID}/roles',
            request_headers=self.headers,
            additional_matcher=data_matcher,
            text=json.dumps(expected),
        )        
        result = self.client.create_guild_role(
            guild_id=TEST_GUILD_ID, role_name=role_name_input
        )
        self.assertDictEqual(result, expected)
    
    def test_get_infos(self, requests_mocker):          
        expected = {
            'id': TEST_GUILD_ID, 
            'name': 'alpha'
        } 
        requests_mocker.get(            
            f'{API_BASE_URL}guilds/{TEST_GUILD_ID}',
            request_headers=self.headers,
            json=expected
        )        
        result = self.client.guild_infos(TEST_GUILD_ID)
        self.assertDictEqual(result, expected)

    def test_get_roles(self, requests_mocker):        
        expected = [
            {'id': 1, 'name': 'alpha'},
            {'id': 2, 'name': 'bravo'}
        ]
        requests_mocker.get(            
            f'{API_BASE_URL}guilds/{TEST_GUILD_ID}/roles',
            request_headers=self.headers,
            json=expected
        )        
        result = self.client.guild_roles(TEST_GUILD_ID)
        self.assertListEqual(result, expected)


@requests_mock.Mocker()
class TestGuildMember(TestCase):
   
    def setUp(self):
        self.client = DiscordClient2(TEST_BOT_TOKEN, mock_redis)
        self.headers = DEFAULT_REQUEST_HEADERS

    def test_return_guild_member_when_ok(self, requests_mocker):
        expected = {'id': TEST_USER_ID, 'name': 'John Doe'}                 
        requests_mocker.get(            
            f'{API_BASE_URL}guilds/{TEST_GUILD_ID}/members/{TEST_USER_ID}',
            request_headers=self.headers,
            json=expected
        )        
        result = self.client.guild_member(TEST_GUILD_ID, TEST_USER_ID)
        self.assertDictEqual(result, expected)

    def test_return_none_if_member_not_known(self, requests_mocker):        
        requests_mocker.get(            
            f'{API_BASE_URL}guilds/{TEST_GUILD_ID}/members/{TEST_USER_ID}',
            request_headers=self.headers,
            status_code=404,        
            json={'code': 10007}
        )        
        result = self.client.guild_member(TEST_GUILD_ID, TEST_USER_ID)        
        self.assertIsNone(result)

    def test_raise_exception_on_error(self, requests_mocker):        
        requests_mocker.get(            
            f'{API_BASE_URL}guilds/{TEST_GUILD_ID}/members/{TEST_USER_ID}',
            request_headers=self.headers,
            status_code=500
        )        
        with self.assertRaises(HTTPError):
            self.client.guild_member(TEST_GUILD_ID, TEST_USER_ID)        
        

class TestGuildGetName(TestCase):

    @patch(MODULE_PATH + '.DiscordClient.guild_infos')    
    def test_returns_from_cache_if_found(self, mock_guild_get_infos):
        guild_name = 'Omega'
        my_mock_redis = MagicMock(**{'get.return_value': guild_name.encode('utf8')})
        mock_guild_get_infos.side_effect = RuntimeError
        client = DiscordClient2(TEST_BOT_TOKEN, my_mock_redis)
        result = client.guild_name(TEST_GUILD_ID)
        self.assertEqual(result, guild_name)

    @patch(MODULE_PATH + '.DiscordClient.guild_infos')    
    def test_fetches_from_server_if_not_found_in_cache_and_stores_in_cache(
        self, mock_guild_get_infos
    ):
        guild_name = 'Omega'
        my_mock_redis = MagicMock(**{'get.return_value': False})
        mock_guild_get_infos.return_value = {'id': TEST_GUILD_ID, 'name': guild_name}
        client = DiscordClient2(TEST_BOT_TOKEN, my_mock_redis)
        result = client.guild_name(TEST_GUILD_ID)
        self.assertEqual(result, guild_name)
        self.assertTrue(my_mock_redis.set.called)

    @patch(MODULE_PATH + '.DiscordClient.guild_infos')    
    def test_return_empty_if_not_found_in_cache_and_not_returned_from_server(
        self, mock_guild_get_infos
    ):
        my_mock_redis = MagicMock(**{'get.return_value': False})
        mock_guild_get_infos.return_value = {}
        client = DiscordClient2(TEST_BOT_TOKEN, my_mock_redis)
        result = client.guild_name(TEST_GUILD_ID)
        self.assertEqual(result, '')
        self.assertFalse(my_mock_redis.set.called)


@requests_mock.Mocker()
class TestGuildDeleteRole(TestCase):

    def setUp(self):
        self.access_token = 'accesstoken'        
        self.headers = DEFAULT_REQUEST_HEADERS
        self.request_url = \
            f'{API_BASE_URL}guilds/{TEST_GUILD_ID}/roles/{TEST_ROLE_ID}'
        self.client = DiscordClient2(TEST_BOT_TOKEN, mock_redis)

    def test_guild_delete_role_success(self, requests_mocker):
        requests_mocker.delete(            
            self.request_url,
            request_headers=self.headers,
            status_code=204
        )
        result = self.client.delete_guild_role(
            guild_id=TEST_GUILD_ID, role_id=TEST_ROLE_ID
        )
        self.assertTrue(result)

    def test_guild_delete_role_failed(self, requests_mocker):
        requests_mocker.delete(            
            self.request_url,
            request_headers=self.headers,
            status_code=200
        )
        result = self.client.delete_guild_role(
            guild_id=TEST_GUILD_ID, role_id=TEST_ROLE_ID
        )
        self.assertFalse(result)


@requests_mock.Mocker()
class TestGuildAddMember(TestCase):
    
    def setUp(self):
        self.access_token = 'accesstoken'        
        self.headers = DEFAULT_REQUEST_HEADERS
        self.request_url = \
            f'{API_BASE_URL}guilds/{TEST_GUILD_ID}/members/{TEST_USER_ID}'
        self.client = DiscordClient2(TEST_BOT_TOKEN, mock_redis)

    def test_create_new_without_params(self, requests_mocker):

        def data_matcher(request):            
            expected = {'access_token': self.access_token}
            return (json.loads(request.text) == expected)
             
        requests_mocker.register_uri(
            'PUT',
            self.request_url,
            request_headers=self.headers,
            additional_matcher=data_matcher,
            status_code=201,            
        )        
        result = self.client.add_guild_member(
            guild_id=TEST_GUILD_ID, 
            user_id=TEST_USER_ID,
            access_token=self.access_token
        )
        self.assertTrue(result)

    def test_create_existing_without_params(self, requests_mocker):
        
        def data_matcher(request):            
            expected = {'access_token': self.access_token}
            return (json.loads(request.text) == expected)
          
        requests_mocker.register_uri(
            'PUT',
            self.request_url,
            request_headers=self.headers,
            additional_matcher=data_matcher,
            status_code=204,            
        )        
        result = self.client.add_guild_member(
            guild_id=TEST_GUILD_ID, 
            user_id=TEST_USER_ID,
            access_token=self.access_token
        )
        self.assertIsNone(result)

    def test_create_failed_without_params(self, requests_mocker):
        
        def data_matcher(request):            
            expected = {'access_token': self.access_token}
            return (json.loads(request.text) == expected)
         
        requests_mocker.register_uri(
            'PUT',
            self.request_url,
            request_headers=self.headers,
            additional_matcher=data_matcher,
            status_code=200,            
        )        
        result = self.client.add_guild_member(
            guild_id=TEST_GUILD_ID, 
            user_id=TEST_USER_ID,
            access_token=self.access_token
        )
        self.assertFalse(result)

    def test_create_new_with_roles(self, requests_mocker):

        role_ids = [1, 2]

        def data_matcher(request):
            expected = {
                'access_token': self.access_token,
                'roles': role_ids
            }
            return (json.loads(request.text) == expected)
             
        requests_mocker.register_uri(
            'PUT',
            self.request_url,
            request_headers=self.headers,
            additional_matcher=data_matcher,
            status_code=201,            
        )        
        result = self.client.add_guild_member(
            guild_id=TEST_GUILD_ID, 
            user_id=TEST_USER_ID,
            access_token=self.access_token,
            role_ids=role_ids
        )
        self.assertTrue(result)

    def test_raise_exception_on_invalid_roles(self, requests_mocker):
        with self.assertRaises(ValueError):
            self.client.add_guild_member(
                guild_id=TEST_GUILD_ID, 
                user_id=TEST_USER_ID,
                access_token=self.access_token,
                role_ids=['abc', 'def']
            )

    def test_create_new_with_nick(self, requests_mocker):

        nick_input = 'x' * 50
        nick_used = 'x' * 32

        def data_matcher(request):
            expected = {
                'access_token': self.access_token,
                'nick': nick_used
            }
            return (json.loads(request.text) == expected)
             
        requests_mocker.register_uri(
            'PUT',
            self.request_url,
            request_headers=self.headers,
            additional_matcher=data_matcher,
            status_code=201,            
        )        
        result = self.client.add_guild_member(
            guild_id=TEST_GUILD_ID, 
            user_id=TEST_USER_ID,
            access_token=self.access_token,
            nick=nick_input
        )
        self.assertTrue(result)


@requests_mock.Mocker()
class TestGuildModifyMember(TestCase):
    
    def setUp(self):
        self.access_token = 'accesstoken'        
        self.headers = DEFAULT_REQUEST_HEADERS.copy()
        self.headers['content-type'] = 'application/json'
        self.request_url = \
            f'{API_BASE_URL}guilds/{TEST_GUILD_ID}/members/{TEST_USER_ID}'
        self.client = DiscordClient2(TEST_BOT_TOKEN, mock_redis)

    def test_can_update_roles(self, requests_mocker):
        role_ids = [1, 2]
            
        def data_matcher(request):            
            expected = {'roles': role_ids}
            return (json.loads(request.text) == expected)
             
        requests_mocker.register_uri(
            'patch',
            self.request_url,
            request_headers=self.headers,
            additional_matcher=data_matcher,
            status_code=204,            
        )        
        result = self.client.modify_guild_member(
            guild_id=TEST_GUILD_ID, 
            user_id=TEST_USER_ID,
            role_ids=role_ids
        )
        self.assertTrue(result)

    def test_can_update_nick(self, requests_mocker):
        nick_input = 'x' * 50
        nick_used = 'x' * 32
            
        def data_matcher(request):            
            expected = {'nick': nick_used}
            return (json.loads(request.text) == expected)
             
        requests_mocker.register_uri(
            'patch',
            self.request_url,
            request_headers=self.headers,
            additional_matcher=data_matcher,
            status_code=204,            
        )        
        result = self.client.modify_guild_member(
            guild_id=TEST_GUILD_ID, 
            user_id=TEST_USER_ID,
            nick=nick_input
        )
        self.assertTrue(result)

    def test_can_update_roles_and_nick(self, requests_mocker):
        role_ids = [1, 2]
            
        def data_matcher(request):            
            expected = {
                'roles': role_ids,
                'nick': TEST_USER_NAME
            }
            return (json.loads(request.text) == expected)
             
        requests_mocker.register_uri(
            'patch',
            self.request_url,
            request_headers=self.headers,
            additional_matcher=data_matcher,
            status_code=204,            
        )        
        result = self.client.modify_guild_member(
            guild_id=TEST_GUILD_ID, 
            user_id=TEST_USER_ID,
            role_ids=role_ids,
            nick=TEST_USER_NAME,
        )
        self.assertTrue(result)

    def test_returns_none_if_member_is_unknown(self, requests_mocker):

        def data_matcher(request):            
            expected = {'nick': TEST_USER_NAME}
            return (json.loads(request.text) == expected)
             
        requests_mocker.register_uri(
            'patch',
            self.request_url,
            request_headers=self.headers,
            additional_matcher=data_matcher,
            status_code=404,            
            json={'code': 10007}
        )        
        result = self.client.modify_guild_member(
            guild_id=TEST_GUILD_ID, 
            user_id=TEST_USER_ID,
            nick=TEST_USER_NAME
        )
        self.assertIsNone(result)

    def test_returns_false_if_unsuccessful(self, requests_mocker):

        def data_matcher(request):            
            expected = {'nick': TEST_USER_NAME}
            return (json.loads(request.text) == expected)
             
        requests_mocker.register_uri(
            'patch',
            self.request_url,
            request_headers=self.headers,
            additional_matcher=data_matcher,
            status_code=200,            
        )        
        result = self.client.modify_guild_member(
            guild_id=TEST_GUILD_ID, 
            user_id=TEST_USER_ID,
            nick=TEST_USER_NAME
        )
        self.assertFalse(result)

    def test_raise_exception_on_invalid_roles(self, requests_mocker):
        with self.assertRaises(ValueError):
            self.client.modify_guild_member(
                guild_id=TEST_GUILD_ID, 
                user_id=TEST_USER_ID,                
                role_ids=['abc', 'def']
            )

    def test_raise_exception_if_role_ids_not_list_like(self, requests_mocker):
        with self.assertRaises(TypeError):
            self.client.modify_guild_member(
                guild_id=TEST_GUILD_ID, 
                user_id=TEST_USER_ID,                
                role_ids='I am not a list'
            )

    def test_raise_exception_on_missing_params(
        self, requests_mocker
    ):
        with self.assertRaises(ValueError):
            self.client.modify_guild_member(
                guild_id=TEST_GUILD_ID, 
                user_id=TEST_USER_ID
            )


class TestGuildRemoveMember(TestCase):

    def setUp(self):        
        self.headers = DEFAULT_REQUEST_HEADERS
        self.request_url = \
            f'{API_BASE_URL}guilds/{TEST_GUILD_ID}/members/{TEST_USER_ID}'
        self.client = DiscordClient2(TEST_BOT_TOKEN, mock_redis)
    
    @requests_mock.Mocker()
    def test_returns_true_on_success(self, requests_mocker):
        requests_mocker.register_uri(
            'DELETE',
            self.request_url,
            request_headers=self.headers,
            status_code=204
        )        
        result = self.client.remove_guild_member(
            guild_id=TEST_GUILD_ID, user_id=TEST_USER_ID
        )
        self.assertTrue(result)
    
    @requests_mock.Mocker()
    def test_returns_none_if_member_unknown(self, requests_mocker):
        requests_mocker.register_uri(
            'DELETE',
            self.request_url,
            request_headers=self.headers,
            status_code=404,
            json={'code': 10007}
        )        
        result = self.client.remove_guild_member(
            guild_id=TEST_GUILD_ID, user_id=TEST_USER_ID
        )
        self.assertIsNone(result)

    @requests_mock.Mocker()
    def test_raise_exception_on_404_if_member_known(self, requests_mocker):
        requests_mocker.register_uri(
            'DELETE',
            self.request_url,
            request_headers=self.headers,
            status_code=404,
            json={}
        )        
        with self.assertRaises(HTTPError):
            self.client.remove_guild_member(
                guild_id=TEST_GUILD_ID, user_id=TEST_USER_ID
            )

    @requests_mock.Mocker()
    def test_raise_exception_on_404_if_no_api_response(self, requests_mocker):
        requests_mocker.register_uri(
            'DELETE',
            self.request_url,
            request_headers=self.headers,
            status_code=404
        )        
        with self.assertRaises(HTTPError):
            self.client.remove_guild_member(
                guild_id=TEST_GUILD_ID, user_id=TEST_USER_ID
            )

    @requests_mock.Mocker()
    def test_returns_false_when_not_successful(self, requests_mocker):
        requests_mocker.register_uri(
            'DELETE',
            self.request_url,
            request_headers=self.headers,
            status_code=200
        )        
        result = self.client.remove_guild_member(
            guild_id=TEST_GUILD_ID, user_id=TEST_USER_ID
        )
        self.assertFalse(result)


class TestGuildMemberAddRole(TestCase):
    
    def setUp(self):        
        self.headers = DEFAULT_REQUEST_HEADERS
        self.request_url = (
            f'{API_BASE_URL}guilds/{TEST_GUILD_ID}/members/{TEST_USER_ID}'
            f'/roles/{TEST_ROLE_ID}'
        )
        self.client = DiscordClient2(TEST_BOT_TOKEN, mock_redis)
    
    @requests_mock.Mocker()
    def test_returns_true_on_success(self, requests_mocker):
        requests_mocker.register_uri(
            'PUT',
            self.request_url,
            request_headers=self.headers,
            status_code=204
        )        
        result = self.client.add_guild_member_role(
            guild_id=TEST_GUILD_ID, user_id=TEST_USER_ID, role_id=TEST_ROLE_ID
        )
        self.assertTrue(result)

    @requests_mock.Mocker()
    def test_return_none_if_member_not_known(self, requests_mocker):
        requests_mocker.register_uri(
            'PUT',
            self.request_url,
            request_headers=self.headers,
            status_code=404,        
            json={'code': 10007}
        )        
        result = self.client.add_guild_member_role(
            guild_id=TEST_GUILD_ID, user_id=TEST_USER_ID, role_id=TEST_ROLE_ID
        )
        self.assertIsNone(result)
    
    @requests_mock.Mocker()
    def test_returns_false_when_not_successful(self, requests_mocker):
        requests_mocker.register_uri(
            'PUT',
            self.request_url,
            request_headers=self.headers,
            status_code=200
        )        
        result = self.client.add_guild_member_role(
            guild_id=TEST_GUILD_ID, user_id=TEST_USER_ID, role_id=TEST_ROLE_ID
        )
        self.assertFalse(result)


class TestGuildMemberRemoveRole(TestCase):
    
    def setUp(self):
        self.headers = DEFAULT_REQUEST_HEADERS
        self.request_url = (
            f'{API_BASE_URL}guilds/{TEST_GUILD_ID}/members/{TEST_USER_ID}'
            f'/roles/{TEST_ROLE_ID}'
        )
        self.client = DiscordClient2(TEST_BOT_TOKEN, mock_redis)
    
    @requests_mock.Mocker()
    def test_returns_true_on_success(self, requests_mocker):
        requests_mocker.register_uri(
            'DELETE',
            self.request_url,
            request_headers=self.headers,
            status_code=204
        )        
        result = self.client.remove_guild_member_role(
            guild_id=TEST_GUILD_ID, user_id=TEST_USER_ID, role_id=TEST_ROLE_ID
        )
        self.assertTrue(result)

    @requests_mock.Mocker()
    def test_return_none_if_member_not_known(self, requests_mocker):
        requests_mocker.register_uri(
            'DELETE',
            self.request_url,
            request_headers=self.headers,
            status_code=404,        
            json={'code': 10007}
        )        
        result = self.client.remove_guild_member_role(
            guild_id=TEST_GUILD_ID, user_id=TEST_USER_ID, role_id=TEST_ROLE_ID
        )
        self.assertIsNone(result)

    @requests_mock.Mocker()
    def test_returns_false_when_not_successful(self, requests_mocker):
        requests_mocker.register_uri(
            'DELETE',
            self.request_url,
            request_headers=self.headers,
            status_code=200
        )        
        result = self.client.remove_guild_member_role(
            guild_id=TEST_GUILD_ID, user_id=TEST_USER_ID, role_id=TEST_ROLE_ID
        )
        self.assertFalse(result)


@patch(MODULE_PATH + '.DiscordClient.create_guild_role')
@patch(MODULE_PATH + '.DiscordClient.guild_roles')
class TestGuildGetOrCreateRoles(TestCase):
            
    def test_return_id_if_role_in_cache(
        self, mock_guild_get_roles, mock_guild_create_role,
    ):        
        role_name = 'alpha'
        my_mock_redis = MagicMock(**{'get.return_value': b'1'})
        client = DiscordClient2(TEST_BOT_TOKEN, my_mock_redis)
        mock_guild_get_roles.side_effect = RuntimeError
        mock_guild_create_role.side_effect = RuntimeError

        expected = ({'id': 1, 'name': 'alpha'}, False)
        result = client.match_guild_role_to_name(TEST_GUILD_ID, role_name)
        self.assertEqual(result, expected)

    def test_return_id_for_role_known_by_api(
        self, mock_guild_get_roles, mock_guild_create_role,
    ):                
        my_mock_redis = MagicMock(**{'get.return_value': None})
        client = DiscordClient2(TEST_BOT_TOKEN, my_mock_redis)
        mock_guild_get_roles.return_value = [
            {'id': 1, 'name': 'alpha'},
            {'id': 2, 'name': 'bravo'}
        ]
        mock_guild_create_role.side_effect = RuntimeError
        
        expected = ({'id': 1, 'name': 'alpha'}, False)
        result = client.match_guild_role_to_name(TEST_GUILD_ID, 'alpha')
        self.assertEqual(result, expected)

        expected = ({'id': 2, 'name': 'bravo'}, False)
        result = client.match_guild_role_to_name(TEST_GUILD_ID, 'bravo')
        self.assertEqual(result, expected)
    
    @patch(MODULE_PATH + '.DISCORD_DISABLE_ROLE_CREATION', False)
    def test_create_role_for_role_not_known_by_api(
        self, mock_guild_get_roles, mock_guild_create_role,
    ):
        my_mock_redis = MagicMock(**{'get.return_value': None})
        client = DiscordClient2(TEST_BOT_TOKEN, my_mock_redis)
        mock_guild_get_roles.return_value = [
            {'id': 1, 'name': 'alpha'},
            {'id': 2, 'name': 'bravo'}
        ]
        mock_guild_create_role.return_value = {'id': 3, 'name': 'charlie'}
        
        expected = ({'id': 3, 'name': 'charlie'}, True)
        result = client.match_guild_role_to_name(TEST_GUILD_ID, 'charlie')
        self.assertEqual(result, expected)

    @patch(MODULE_PATH + '.DISCORD_DISABLE_ROLE_CREATION', True)
    def test_return_none_if_role_creation_is_disabled(
        self, mock_guild_get_roles, mock_guild_create_role,
    ):
        my_mock_redis = MagicMock(**{'get.return_value': None})
        client = DiscordClient2(TEST_BOT_TOKEN, my_mock_redis)
        mock_guild_get_roles.return_value = [
            {'id': 1, 'name': 'alpha'},
            {'id': 2, 'name': 'bravo'}
        ]
        mock_guild_create_role.return_value = {'id': 3, 'name': 'charlie'}
                
        result = client.match_guild_role_to_name(TEST_GUILD_ID, 'charlie')
        self.assertIsNone(result[0])
        self.assertFalse(result[1])

    def test_return_ids_if_role_in_cache(
        self, mock_guild_get_roles, mock_guild_create_role,   
    ):
        def my_cache_get(name):
            map = {
                DiscordClient._role_cache_key(TEST_GUILD_ID, 'alpha'): b'1',
                DiscordClient._role_cache_key(TEST_GUILD_ID, 'bravo'): b'2',
                DiscordClient._role_cache_key(TEST_GUILD_ID, 'charlie'): b'3'
            }
            if name in map:
                return map[name]
            else:
                return None
        
        my_mock_redis = MagicMock(**{'get.side_effect': my_cache_get})
        client = DiscordClient2(TEST_BOT_TOKEN, my_mock_redis)
        mock_guild_get_roles.side_effect = RuntimeError
        mock_guild_create_role.side_effect = RuntimeError
        
        expected = [
            ({'id': 1, 'name': 'alpha'}, False), ({'id': 3, 'name': 'charlie'}, False)
        ]
        result = client.match_guild_roles_to_names(TEST_GUILD_ID, ['alpha', 'charlie'])
        self.assertEqual(result, expected)

    @patch(MODULE_PATH + '.DiscordClient.match_guild_role_to_name')
    def test_ignore_none_roles_in_guild_get_or_create_roles(
        self, 
        mock_guild_get_or_create_role, 
        mock_guild_get_roles, 
        mock_guild_create_role,
    ):
        def my_guild_get_or_create_role(guild_id, role_name):
            if role_name == 'alpha':
                return {'id': 1, 'name': 'alpha'}, False
            elif role_name == 'charlie':
                return None, False
            else:
                raise ValueError('Unknown role')
        
        mock_guild_get_or_create_role.side_effect = my_guild_get_or_create_role

        client = DiscordClient2(TEST_BOT_TOKEN, mock_redis)
        result = client.match_guild_roles_to_names(TEST_GUILD_ID, ['alpha', 'charlie'])
        expected = [
            ({'id': 1, 'name': 'alpha'}, False),         
        ]
        self.assertEqual(result, expected)
        

class TestUpdateRoleCache(TestCase):
    
    def test_can_update_cache(self):
        my_mock_redis = MagicMock()
        client = DiscordClient(TEST_BOT_TOKEN, my_mock_redis)
        role = {'id': 1, 'name': 'alpha'}
        client._update_role_cache(TEST_GUILD_ID, role)
        self.assertTrue(my_mock_redis.set.called)

    def test_raises_exception_if_wrong_role_type(self):
        my_mock_redis = MagicMock()
        client = DiscordClient(TEST_BOT_TOKEN, my_mock_redis)
        role = 'abc'
        with self.assertRaises(TypeError):
            client._update_role_cache(TEST_GUILD_ID, role)

        self.assertFalse(my_mock_redis.set.called)
        

class TestApiRequestBasics(TestCase):

    def setUp(self):
        self.client = DiscordClient(TEST_BOT_TOKEN, mock_redis)
    
    @patch(MODULE_PATH + '.requests', spec=requests)
    def test_raises_exception_on_invalid_method(self, mock_requests):
        with self.assertRaises(ValueError):
            self.client._api_request('xxx', 'users/@me')


@patch(MODULE_PATH + '.DiscordClient._redis_decr_or_set')
@requests_mock.Mocker()
class TestRateLimitMechanic(TestCase):
    
    my_role = {'id': 1, 'name': 'alpha'}
    
    @staticmethod
    def my_redis_pttl(name: str):
        if name == DiscordClient._KEY_GLOBAL_BACKOFF_UNTIL:
            return -1
        else:
            return TEST_RETRY_AFTER
    
    def test_proceed_if_requests_remaining(
        self, mock_redis_decr_or_set, requests_mocker
    ):               
        requests_mocker.post(
            f'{API_BASE_URL}guilds/{TEST_GUILD_ID}/roles', json=self.my_role
        )        
        my_mock_redis = MagicMock(**{'pttl.side_effect': self.my_redis_pttl})
        mock_redis_decr_or_set.return_value = 5
        client = DiscordClient(TEST_BOT_TOKEN, my_mock_redis)        
        result = client.create_guild_role(
            guild_id=TEST_GUILD_ID, role_name=self.my_role['name']
        )
        self.assertDictEqual(result, self.my_role)

    @patch(MODULE_PATH + '.sleep')
    def test_wait_if_reset_happens_soon(
        self, requests_mocker, mock_sleep, mock_redis_decr_or_set
    ):        
        counter = 0
        
        def my_redis_pttl_2(name: str):
            if name == DiscordClient._KEY_GLOBAL_BACKOFF_UNTIL:
                return -1
            else:
                return 100
        
        def my_redis_decr_or_set(**kwargs):
            nonlocal counter
            counter += 1

            if counter < 2:
                return -1
            else:
                return 5

        requests_mocker.post(
            f'{API_BASE_URL}guilds/{TEST_GUILD_ID}/roles', json=self.my_role
        )        
        my_mock_redis = MagicMock(**{'pttl.side_effect': my_redis_pttl_2})
        mock_redis_decr_or_set.side_effect = my_redis_decr_or_set
        client = DiscordClient(TEST_BOT_TOKEN, my_mock_redis)
        
        result = client.create_guild_role(
            guild_id=TEST_GUILD_ID, role_name=self.my_role['name']
        )
        self.assertDictEqual(result, self.my_role)
        self.assertTrue(mock_sleep.called)
    
    def test_throw_exception_if_rate_limit_reached(
        self, mock_redis_decr_or_set, requests_mocker
    ):        
        requests_mocker.post(
            f'{API_BASE_URL}guilds/{TEST_GUILD_ID}/roles', json=self.my_role
        )        
        my_mock_redis = MagicMock(**{'pttl.side_effect': self.my_redis_pttl})
        mock_redis_decr_or_set.return_value = -1
        client = DiscordClient(TEST_BOT_TOKEN, my_mock_redis)
        try:
            client.create_guild_role(
                guild_id=TEST_GUILD_ID, role_name=self.my_role['name']
            )
        except Exception as ex:
            self.assertIsInstance(ex, DiscordRateLimitExhausted)
            self.assertEqual(ex.retry_after, TEST_RETRY_AFTER)

    @patch(MODULE_PATH + '.RATE_LIMIT_RETRIES', 1)
    @patch(MODULE_PATH + '.sleep')
    def test_throw_exception_if_retries_are_exhausted(
        self, requests_mocker, mock_sleep, mock_redis_decr_or_set
    ):        
        def my_redis_pttl_2(name: str):
            if name == DiscordClient._KEY_GLOBAL_BACKOFF_UNTIL:
                return -1
            else:
                return 100
        
        requests_mocker.post(
            f'{API_BASE_URL}guilds/{TEST_GUILD_ID}/roles', json=self.my_role
        )        
        my_mock_redis = MagicMock(**{'pttl.side_effect': my_redis_pttl_2})
        mock_redis_decr_or_set.return_value = -1
        client = DiscordClient(TEST_BOT_TOKEN, my_mock_redis)
        
        with self.assertRaises(RuntimeError):
            client.create_guild_role(
                guild_id=TEST_GUILD_ID, role_name=self.my_role['name']
            )
        
    def test_report_api_rate_limits(
        self, mock_redis_decr_or_set, requests_mocker
    ):               
        headers = {
            'x-ratelimit-limit': '10',
            'x-ratelimit-remaining': '9',
            'x-ratelimit-reset-after': '10.000',
        }
        requests_mocker.post(
            f'{API_BASE_URL}guilds/{TEST_GUILD_ID}/roles', 
            json=self.my_role,
            headers=headers
        )        
        my_mock_redis = MagicMock(**{'pttl.side_effect': self.my_redis_pttl})
        mock_redis_decr_or_set.return_value = 5
        client = DiscordClient(TEST_BOT_TOKEN, my_mock_redis)        
        result = client.create_guild_role(
            guild_id=TEST_GUILD_ID, role_name=self.my_role['name']
        )
        self.assertDictEqual(result, self.my_role)

    def test_dont_report_api_rate_limits(
        self, mock_redis_decr_or_set, requests_mocker
    ):               
        headers = {
            'x-ratelimit-limit': '10',
            'x-ratelimit-remaining': '5',
            'x-ratelimit-reset-after': '10.000',
        }
        requests_mocker.post(
            f'{API_BASE_URL}guilds/{TEST_GUILD_ID}/roles', 
            json=self.my_role,
            headers=headers
        )        
        my_mock_redis = MagicMock(**{'pttl.side_effect': self.my_redis_pttl})
        mock_redis_decr_or_set.return_value = 5
        client = DiscordClient(TEST_BOT_TOKEN, my_mock_redis)        
        result = client.create_guild_role(
            guild_id=TEST_GUILD_ID, role_name=self.my_role['name']
        )
        self.assertDictEqual(result, self.my_role)

    def test_ignore_errors_in_api_rate_limits(
        self, mock_redis_decr_or_set, requests_mocker
    ):               
        headers = {
            'x-ratelimit-limit': '10',
            'x-ratelimit-remaining': '0',
            'x-ratelimit-reset-after': 'invalid',
        }
        requests_mocker.post(
            f'{API_BASE_URL}guilds/{TEST_GUILD_ID}/roles', 
            json=self.my_role,
            headers=headers
        )        
        my_mock_redis = MagicMock(**{'pttl.side_effect': self.my_redis_pttl})
        mock_redis_decr_or_set.return_value = 5
        client = DiscordClient(TEST_BOT_TOKEN, my_mock_redis)        
        result = client.create_guild_role(
            guild_id=TEST_GUILD_ID, role_name=self.my_role['name']
        )
        self.assertDictEqual(result, self.my_role)

    @patch(MODULE_PATH + '.DiscordClient._ensure_rate_limed_not_exhausted')
    def test_can_turn_off_rate_limiting(
        self, 
        requests_mocker, 
        mock_ensure_rate_limed_not_exhausted, 
        mock_redis_decr_or_set
    ):        
        requests_mocker.post(
            f'{API_BASE_URL}guilds/{TEST_GUILD_ID}/roles', json=self.my_role
        )                
        client = DiscordClient(TEST_BOT_TOKEN, mock_redis, is_rate_limited=False)
        result = client.create_guild_role(
            guild_id=TEST_GUILD_ID, role_name=self.my_role['name']
        )
        self.assertDictEqual(result, self.my_role)
        self.assertFalse(mock_ensure_rate_limed_not_exhausted.called)


@patch(MODULE_PATH + '.DiscordClient._redis_decr_or_set')
@requests_mock.Mocker()
class TestBackoffHandling(TestCase):
    
    my_role = {'id': 1, 'name': 'alpha'}

    def test_dont_raise_exception_when_no_global_backoff(
        self, mock_redis_decr_or_set, requests_mocker
    ):
        requests_mocker.post(
            f'{API_BASE_URL}guilds/{TEST_GUILD_ID}/roles', json=self.my_role
        )
        my_mock_redis = MagicMock(**{'pttl.return_value': -1})
        mock_redis_decr_or_set.return_value = 5
        client = DiscordClient(TEST_BOT_TOKEN, my_mock_redis)        
        result = client.create_guild_role(guild_id=TEST_GUILD_ID, role_name='dummy')
        self.assertDictEqual(result, self.my_role)
    
    def test_raise_exception_when_global_backoff_in_effect(
        self, mock_redis_decr_or_set, requests_mocker
    ):
        requests_mocker.post(
            f'{API_BASE_URL}guilds/{TEST_GUILD_ID}/roles', json=self.my_role
        )
        retry_after = 1000        
        my_mock_redis = MagicMock(**{'pttl.return_value': retry_after})
        mock_redis_decr_or_set.return_value = 5
        client = DiscordClient(TEST_BOT_TOKEN, my_mock_redis)
        try:
            client.create_guild_role(
                guild_id=TEST_GUILD_ID, role_name='dummy'
            )
        except Exception as ex:
            self.assertIsInstance(ex, DiscordTooManyRequestsError)
            self.assertEqual(ex.retry_after, retry_after)

    @patch(MODULE_PATH + '.sleep')
    def test_just_wait_if_global_backoff_ends_soon(
        self, requests_mocker, mock_sleep, mock_redis_decr_or_set, 
    ):
        requests_mocker.post(
            f'{API_BASE_URL}guilds/{TEST_GUILD_ID}/roles', json=self.my_role
        )
        retry_after = 50        
        my_mock_redis = MagicMock(**{'pttl.return_value': retry_after})
        mock_redis_decr_or_set.return_value = 5
        client = DiscordClient(TEST_BOT_TOKEN, my_mock_redis)
        client.create_guild_role(
            guild_id=TEST_GUILD_ID, role_name='dummy'
        )
        result = client.create_guild_role(guild_id=TEST_GUILD_ID, role_name='dummy')
        self.assertDictEqual(result, self.my_role)
        self.assertTrue(mock_sleep.called)
    
    @patch(MODULE_PATH + '.DiscordClient._redis_set_if_longer')
    def test_raise_exception_if_api_returns_429(
        self, requests_mocker, mock_redis_set_if_longer, mock_redis_decr_or_set,
    ):
        retry_after = 5000
        requests_mocker.post(            
            f'{API_BASE_URL}guilds/{TEST_GUILD_ID}/roles',
            status_code=429,
            json={'retry_after': retry_after}
        )        
        my_mock_redis = MagicMock(
            **{'pttl.side_effect': TestRateLimitMechanic.my_redis_pttl}
        )
        mock_redis_decr_or_set.return_value = 5
        
        client = DiscordClient(TEST_BOT_TOKEN, my_mock_redis)
        try:
            client.create_guild_role(
                guild_id=TEST_GUILD_ID, role_name='dummy'
            )
        except Exception as ex:
            self.assertIsInstance(ex, DiscordTooManyRequestsError)
            self.assertEqual(ex.retry_after, retry_after + DURATION_CONTINGENCY)
            self.assertTrue(mock_redis_set_if_longer.called)
            args, kwargs = mock_redis_set_if_longer.call_args
            self.assertEqual(kwargs['px'], retry_after + DURATION_CONTINGENCY)

    @patch(MODULE_PATH + '.DiscordClient._redis_set_if_longer')
    def test_raise_exception_if_api_returns_429_no_retry_info(
        self, requests_mocker, mock_redis_set_if_longer, mock_redis_decr_or_set,
    ):
        requests_mocker.post(            
            f'{API_BASE_URL}guilds/{TEST_GUILD_ID}/roles',
            status_code=429,
            json={}
        )        
        my_mock_redis = MagicMock(
            **{'pttl.side_effect': TestRateLimitMechanic.my_redis_pttl}
        )
        mock_redis_decr_or_set.return_value = 5
        
        client = DiscordClient(TEST_BOT_TOKEN, my_mock_redis)
        try:
            client.create_guild_role(
                guild_id=TEST_GUILD_ID, role_name='dummy'
            )
        except Exception as ex:
            self.assertIsInstance(ex, DiscordTooManyRequestsError)
            self.assertEqual(ex.retry_after, DEFAULT_BACKOFF_DELAY)
            self.assertTrue(mock_redis_set_if_longer.called)
            args, kwargs = mock_redis_set_if_longer.call_args
            self.assertEqual(kwargs['px'], DEFAULT_BACKOFF_DELAY)

    @patch(MODULE_PATH + '.DiscordClient._redis_set_if_longer')
    def test_raise_exception_if_api_returns_429_ignore_value_error(
        self, requests_mocker, mock_redis_set_if_longer, mock_redis_decr_or_set,
    ):
        requests_mocker.post(            
            f'{API_BASE_URL}guilds/{TEST_GUILD_ID}/roles',
            status_code=429,
            json={'retry_after': "invalid"}
        )        
        my_mock_redis = MagicMock(
            **{'pttl.side_effect': TestRateLimitMechanic.my_redis_pttl}
        )
        mock_redis_decr_or_set.return_value = 5
        
        client = DiscordClient(TEST_BOT_TOKEN, my_mock_redis)
        try:
            client.create_guild_role(
                guild_id=TEST_GUILD_ID, role_name='dummy'
            )
        except Exception as ex:
            self.assertIsInstance(ex, DiscordTooManyRequestsError)
            self.assertEqual(ex.retry_after, DEFAULT_BACKOFF_DELAY)
            self.assertTrue(mock_redis_set_if_longer.called)
            args, kwargs = mock_redis_set_if_longer.call_args
            self.assertEqual(kwargs['px'], DEFAULT_BACKOFF_DELAY)


class TestRedisDecode(TestCase):

    def test_decode_string(self):
        self.assertEqual(
            DiscordClient._redis_decode('MyTest123'.encode('utf8')), 'MyTest123'
        )

    def test_decode_bool(self):
        self.assertTrue(DiscordClient._redis_decode(True))
        self.assertFalse(DiscordClient._redis_decode(False))

    def test_decode_none(self):
        self.assertIsNone(DiscordClient._redis_decode(None))


class TestTouchLuaScripts(TestCase):
    
    def test__redis_script_decr_or_set(self):
        client = DiscordClient(TEST_BOT_TOKEN, mock_redis)
        client._redis_decr_or_set(name='dummy', value=5, px=1000)

    def test_redis_set_if_longer(self):
        client = DiscordClient(TEST_BOT_TOKEN, mock_redis)
        client._redis_set_if_longer(name='dummy', value=5, px=1000)
