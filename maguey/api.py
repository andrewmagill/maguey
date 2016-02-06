import os, requests, json

AGAVE_TENANT_BASEURL = os.environ.get('AGAVE_TENANT_BASEURL', 'https://agave.iplantc.org/')

class Files(object):
    pass

class Notifications(object):
    pass

class Meta(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            try:
                assert(k not in dir(self))
                setattr(self, k, v)
            except:
                raise Exception('key conflict: {}'.format(k))

    @staticmethod
    def list(token, query=None, **kwargs):
        """Returns list of metadata objects.

        Parameters:
            token   (required)  -   bearer token
            query   (optional)  -   must be valid mongodb query

            Example query:
                query = '{"name":"idsvc.project"}'

        Returns:
            List of metadata objects with the following fields:

            associationIds - IDs of associated metadata objects
            created - metadata object creation date
            internalUsername - system specific username
            lastUpdated - metadata object last updated
            name - often used to refer to the type of object the metadata describes
            owner - most likely the user who created the metadata
            schemaId - metadata schemata id
            uuid - unique identifier for metadata object
            value - usually contains a JSON object
        """
        if not token or token == '':
            raise ValueError("token is a required parameter")

        method_path = "meta/v2/data"
        parameters = None
        uuid = None

        if query:
            if type(query) == 'dict':
                query = json.dumps(query)
            parameters = {'q': query}

        if 'uuid' in kwargs.keys():
            uuid = kwargs['uuid']

        url = "{base}/{method}/{uuid}".format(
            base = AGAVE_TENANT_BASEURL,
            method = method_path,
            uuid = uuid if uuid else ''
        )

        headers = {'Authorization': 'Bearer {}'.format(token)}

        response = requests.get(url, headers=headers, params=parameters)

        try:
            if response.status_code == 400:
                raise Exception('Invalid JSON query')
            if response.status_code == 401:
                raise Exception('User is not authorized')
            if response.status_code == 402:
                raise Exception('Failed to authenticate user')
            if response.status_code == 403:
                raise Exception('The specified metadata cannot be found')
            if response.status_code == 404:
                raise Exception('The service was unable to query the metadata database')
        except Exception as e:
            raise Exception('invalid object from server')

        try:
            response = response.json()
            if response['status'] == 'error':
                raise Exception(response['message'])
        except Exception as e:
            raise Exception('invalid object from server')

        result = response['result']

        if type(result) == 'list':
            result_list = []
            for item in result:
                result_list.append(Meta(**item))
            return result_list
        else:
            return Meta(**result)

    @staticmethod
    def get(token, uuid):
        """Returns a metadata object.

        Parameters:
            token   (required)  -   bearer token
            uuid    (required)  -   get metadata by uuid

        Returns:
            A metadata object with the following fields:

            associationIds - IDs of associated metadata objects
            created - metadata object creation date
            internalUsername - system specific username
            lastUpdated - metadata object last updated
            name - often used to refer to the type of object the metadata describes
            owner - most likely the user who created the metadata
            schemaId - metadata schemata id
            uuid - unique identifier for metadata object
            value - usually contains a JSON object
        """
        if not token or token == '':
            raise ValueError("token is a required parameter")

        if not uuid or uuid == '':
            raise ValueError("uuid is a required parameter")

        return Meta.list(token, uuid=uuid)

    @staticmethod
    def _add_update(token, body, uuid=None):
        """Internal: Adds or updates a metadata object.

        Parameters:
            token   (required)  -   bearer token
            body    (required)  -   must be valid json with 'name' and 'value' fields
            uuid    (optional)  -   metadata object to update

        Returns:
            JSON message with the following fields:

            status - success or error
            message - error message
            result - newly created metadata object
        """
        if not token or token == '':
            raise ValueError("token is a required parameter")

        if not body or body == '':
            raise ValueError("body is a required parameter")

        method_path = "meta/v2/data"

        url = "{base}/{method}/{uuid}".format(
            base = AGAVE_TENANT_BASEURL,
            method = method_path,
            uuid = uuid if uuid else ''
        )

        headers = {'Authorization': 'Bearer {}'.format(token),
                   'content-type': 'application/json'}

        result = requests.post(url, headers=headers, data=body)
        return result.json()

    @staticmethod
    def add(token, body):
        """Creates a metadata object.

        Parameters:
            token   (required)  -   bearer token
            body    (required)  -   must be valid json with 'name' and 'value' fields

        Returns:
            JSON message with the following fields:

            status - success or error
            message - error message
            result - newly created metadata object
        """
        if not token or token == '':
            raise ValueError("token is a required parameter")

        if not body or body == '':
            raise ValueError("body is a required parameter")

        return Meta._add_update(token, body)

    @staticmethod
    def update(token, uuid, body):
        """Updates a metadata object.

        Parameters:
            token   (required)  -   bearer token
            uuid    (required)  -   metadata object to update
            body    (required)  -   must be valid json with 'name' and 'value' fields

        Returns:
            JSON message with the following fields:

            status - success or error
            message - error message
            result - newly created metadata object
        """
        if not token or token == '':
            raise ValueError("token is a required parameter")

        if not uuid or uuid == '':
            raise ValueError("uuid is a required parameter")

        if not body or body == '':
            raise ValueError("body is a required parameter")

        return Meta._add_update(token, body, uuid)

    @staticmethod
    def delete(token, uuid):
        """Deletes a metadata object.

        Parameters:
            token   (required)  -   bearer token
            uuid    (required)  -   metadata object to update

        Returns:
            JSON message with the following fields:

            status - success or error
            message - error message
        """
        if not token or token == '':
            raise ValueError("token is a required parameter")

        if not uuid or uuid == '':
            raise ValueError("uuid is a required parameter")

        method_path = "meta/v2/data"

        url = "{base}/{method}/{uuid}".format(
            base = AGAVE_TENANT_BASEURL,
            method = method_path,
            uuid = uuid
        )

        headers = {'Authorization': 'Bearer {}'.format(token)}

        result = requests.delete(url, headers=headers)
        return result.json()

class Postits(object):
    pass

class Profiles(object):
    pass

class Systems(object):
    pass
