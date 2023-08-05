################################################################################
#
# Licensed Materials - Property of IBM
# (C) Copyright IBM Corp. 2017
# US Government Users Restricted Rights - Use, duplication disclosure restricted
# by GSA ADP Schedule Contract with IBM Corp.
#
################################################################################

import requests
from watson_machine_learning_client.wml_client_error import MissingValue, WMLClientError, NoWMLCredentialsProvided, ApiRequestFailure, UnexpectedType, MissingMetaProp
from watson_machine_learning_client.href_definitions import HrefDefinitions
from watson_machine_learning_client.utils.log_util import get_logger
from watson_machine_learning_client.utils import get_type_of_details, STR_TYPE, str_type_conv
import urllib.parse
import os

class WMLResource:
    def __init__(self, name, client):
        self._logger = get_logger(name)
        self._name = name
        self._WSD = None
        WMLResource._validate_type(client, u'client', object, True)
        if client.wml_credentials is None:
            raise NoWMLCredentialsProvided
        WMLResource._validate_type(client.wml_credentials, u'wml_credentials', dict, True)
        if not client.WSD and not client.ICP:
            wml_token = str_type_conv(client.wml_token)
            WMLResource._validate_type(wml_token, u'wml_token', STR_TYPE, True)
        self._client = client
        self._ICP = client.ICP
        self._WSD = client.WSD

        # ToDO why this is differnt , check in 2.5 cluster and cloud whether it is working
        if client.ICP or client.WSD:
            self._wml_credentials = client.wml_credentials
            self._href_definitions = HrefDefinitions(client.wml_credentials)
        else:
            self._wml_credentials = client.service_instance._wml_credentials
            self._href_definitions = HrefDefinitions(client.service_instance._wml_credentials)

    def _handle_response(self, expected_status_code, operationName, response, json_response=True):
        if "dele" in operationName:
            if response.status_code == expected_status_code:
                return "SUCCESS"
            else:
                print(response.text)
                return "FAILED"
        if response.status_code == expected_status_code:

            self._logger.info(u'Successfully finished {} for url: \'{}\''.format(operationName, response.url))
            self._logger.debug(u'Response({} {}): {}'.format(response.request.method, response.url, response.text))
            if json_response:
                try:
                    return response.json()
                except Exception as e:
                    raise WMLClientError(u'Failure during parsing json response: \'{}\''.format(response.text), e)
            else:
                return response.text
        else:
            raise ApiRequestFailure(u'Failure during {}.'.format(operationName), response)

    @staticmethod
    def _get_required_element_from_dict(el, root_path, path):
        WMLResource._validate_type(el, root_path, dict)
        WMLResource._validate_type(root_path, u'root_path', STR_TYPE)
        WMLResource._validate_type(path, u'path', list)

        if path.__len__() < 1:
            raise WMLClientError(u'Unexpected path length: {}'.format(path.__len__))

        try:
            new_el = el[path[0]]
            new_path = path[1:]
        except Exception as e:
            raise MissingValue(root_path + '.' + str(path[0]), e)

        if path.__len__() > 1:
            return WMLResource._get_required_element_from_dict(new_el, root_path + u'.' + path[0], new_path)
        else:
            if new_el is None:
                raise MissingValue(root_path + u'.' + str(path[0]))

            return new_el

    @staticmethod
    def _validate_type(el, el_name, expected_type, mandatory=True):
        if el_name is None:
            raise MissingValue(u'el_name')

        el_name = str_type_conv(el_name)
        if type(el_name) is not STR_TYPE:
            raise UnexpectedType(u'el_name', STR_TYPE, type(el_name))

        if expected_type is None:
            raise MissingValue(u'expected_type')

        if type(expected_type) is not type and type(expected_type) is not list:
            raise UnexpectedType('expected_type', 'type or list', type(expected_type))

        if type(mandatory) is not bool:
            raise UnexpectedType(u'mandatory', bool, type(mandatory))

        if mandatory and el is None:
            raise MissingValue(el_name)
        elif el is None:
            return

        if type(expected_type) is list:
            try:
                next((x for x in expected_type if isinstance(el, x)))
                return True
            except StopIteration:
                return False
        else:
            if not isinstance(el, expected_type):
                raise UnexpectedType(el_name, expected_type, type(el))

    @staticmethod
    def _validate_meta_prop(meta_props, name, expected_type, mandatory=True):
        if name in meta_props:
            WMLResource._validate_type(meta_props[name], u'meta_props.' + name, expected_type, mandatory)
        else:
            if mandatory:
                raise MissingMetaProp(name)

    @staticmethod
    def _validate_type_of_details(details, expected_type):
        actual_type = get_type_of_details(details)

        if type(expected_type) is list:
            expected_types = expected_type
        else:
            expected_types = [expected_type]

        if not any([actual_type == exp_type for exp_type in expected_types]):
            logger = get_logger(u'_validate_type_of_details')
            logger.debug(u'Unexpected type of \'{}\', expected: \'{}\', actual: \'{}\', occured for details: {}'.format(
                u'details', expected_type, actual_type, details))
            raise UnexpectedType(u'details', expected_type, actual_type)

    def _check_if_lib_or_def(self, lib_uid):

        verify = False
        lib_details = requests.get(self._href_definitions.get_custom_library_href(lib_uid),
                                   headers=self._client._get_headers(), verify=verify)
        if lib_details.status_code == 200:
            return lib_details.json()["metadata"]["href"]
        def_details = requests.get(self._href_definitions.get_model_definition_assets_href() + u'/' + lib_uid,
                                   params=self._client._params(), headers=self._client._get_headers(), verify=verify)
        if def_details.status_code == 200:
            return def_details.json()["href"]
        else:
            raise WMLClientError("The LIB_UID provided is not a valid model_definition/library")

    def _get_artifact_details(self, base_url, uid, limit, resource_name, summary=None,pre_defined=None):
        op_name = 'getting {} details'.format(resource_name)

        if uid is None:
            return self._get_with_or_without_limit(url=base_url, limit=limit, op_name=resource_name,summary=summary,pre_defined=pre_defined)
        else:
            # if not is_uid(uid):
            #     raise WMLClientError(u'Failure during {}, invalid uid: \'{}\''.format(op_name, uid)) # TODO
            params = self._client._params()

            url = base_url + u'/' + uid

            if not self._ICP and not self._client.WSD:
                response_get = requests.get(
                    url,
                    params,
                    headers=self._client._get_headers()
                )
            else:
                response_get = requests.get(
                    url,
                    params,
                    headers=self._client._get_headers(),
                    verify=False
                )

            return self._handle_response(200, op_name, response_get)

    def _get_with_or_without_limit(self, url, limit, op_name,summary,pre_defined, revision=None):
        params = self._client._params()
        if summary == "False":
            params.update({u'summary': u'false'})
        if pre_defined == "True":
            params.update({u'system_runtimes': u'true'})
        if limit is not None:
            if limit < 1:
                raise WMLClientError('Limit cannot be lower than 1.')
            elif limit > 1000:
                raise WMLClientError('Limit cannot be larger than 1000.')
            params.update({u'limit': limit})
        if revision is not None:
            params.update({u'rev': revision})
        if len (params) > 0:
            if not self._ICP:
                response_get = requests.get(
                    url,
                    headers=self._client._get_headers(),
                    params=params
                )
            else:
                response_get = requests.get(
                    url,
                    headers=self._client._get_headers(),
                    params=params,
                    verify=False
                )
            return self._handle_response(200, op_name, response_get)
        else:

            resources = []

            while True:
                if not self._ICP:
                    response_get = requests.get(
                        url,
                        headers=self._client._get_headers()

                    )
                else:
                    response_get = requests.get(
                        url,
                        headers=self._client._get_headers(),
                        verify=False
                    )

                result = self._handle_response(200, op_name, response_get)
                resources.extend(result['resources'])

                if 'next' not in result:
                    break
                else:

                    url = self._wml_credentials["url"]+result['next']['href']
                    if('start=invalid' in url):
                        break


            return {
                "resources": resources
            }

    def _get_no_space_artifact_details(self, base_url, uid, limit, resource_name, summary=None,pre_defined=None):
        op_name = 'getting {} details'.format(resource_name)

        if uid is None:
            return self._get_no_space_with_or_without_limit(url=base_url, limit=limit, op_name=resource_name,summary=summary,pre_defined=pre_defined)
        else:
            # if not is_uid(uid):
            #     raise WMLClientError(u'Failure during {}, invalid uid: \'{}\''.format(op_name, uid)) # TODO

            url = base_url + u'/' + uid

            if not self._ICP:
                response_get = requests.get(
                    url,
                    headers=self._client._get_headers()
                )
            else:
                response_get = requests.get(
                    url,
                    headers=self._client._get_headers(),
                    verify=False
                )

            return self._handle_response(200, op_name, response_get)

    def _get_no_space_with_or_without_limit(self, url, limit, op_name,summary,pre_defined):
        params = {}
        if summary == "False":
            params.update({u'summary': u'false'})
        if pre_defined == "True":
            params.update({u'system_runtimes': u'true'})
        if limit is not None:
            if limit < 1:
                raise WMLClientError('Limit cannot be lower than 1.')
            elif limit > 1000:
                raise WMLClientError('Limit cannot be larger than 1000.')
            params.update({u'limit': limit})
        if len (params) > 0:
            if not self._ICP:
                response_get = requests.get(
                    url,
                    headers=self._client._get_headers(),
                    params=params
                )
            else:
                response_get = requests.get(
                    url,
                    headers=self._client._get_headers(),
                    params=params,
                    verify=False
                )

            return self._handle_response(200, op_name, response_get)
        else:

            resources = []

            while True:
                if not self._ICP:
                    response_get = requests.get(
                        url,
                        headers=self._client._get_headers(),

                    )
                else:
                    response_get = requests.get(
                        url,
                        headers=self._client._get_headers(),
                        verify=False
                    )

                result = self._handle_response(200, op_name, response_get)
                resources.extend(result['resources'])

                if 'next' not in result:
                    break
                else:

                    url = self._wml_credentials["url"]+result['next']['href']
                    if('start=invalid' in url):
                        break
            return {
                "resources": resources
            }

    def _if_deployment_exist_for_asset(self, asset_id):

        deployment_href = self._href_definitions.get_deployments_href() + "?asset_id=" + asset_id
        response_deployment = requests.get(deployment_href, params=self._client._params(),
                                           headers=self._client._get_headers(), verify=False)
        deployment_json = self._handle_response(200, "Get deployment details", response_deployment)
        resources = deployment_json["resources"]
        if resources:
            return 1
        else:
            return 0

    def _list(self, values, header, limit, default_limit, sort_by='CREATED'):
        if sort_by is not None and sort_by in header:
            column_no = header.index(sort_by)
            values = sorted(values, key=lambda x: x[column_no], reverse=True)

        from tabulate import tabulate

        if limit is None:
            table = tabulate([header] + values[:default_limit])
            print(table)
            if default_limit is not None and len(values) > default_limit:
                print('Note: Only first {} records were displayed. To display more use \'limit\' parameter.'.format(default_limit))
        else:
            table = tabulate([header] + values)
            print(table)

    def _wsd_list_assets(self, asset_type, limit=None):
        _DEFAULT_LIST_LENGTH = 50
        ##For CP4D, check if either spce or project ID is set
        href = self._href_definitions.get_wsd_asset_search_href(asset_type)
        if limit is None:
            data = {
                "query": "*:*"
            }
        else:
            self._validate_type(limit, u'limit', int, False)
            data = {
                "query": "*:*",
                "limit": limit
            }

        response = requests.post(href, params=self._client._params(), headers=self._client._get_headers(),
                                     json=data, verify=False)
        self._handle_response(200, u'list ', response)
        asset_details = self._handle_response(200, u'model list', response)["results"]
        model_def_values = [
            (m[u'metadata'][u'name'], m[u'metadata'][u'asset_type'], m[u'metadata'][u'asset_id']) for
            m in asset_details]

        self._list(model_def_values, [u'NAME', u'ASSET_TYPE', u'GUID'], limit, _DEFAULT_LIST_LENGTH)

    def _create_wsd_payload(self, asset_type, payload_input, meta_props):
        # TODO: Get the country code from locale
        origin_country = "US"
        payload_metadata = {
            "name": meta_props['name'],
            "asset_type": asset_type,
            "origin_country": origin_country,
            "assetCategory": "USERS"
        }
        if 'description' in meta_props and meta_props['description'] is not None:
            payload_metadata.update({'description': meta_props['description']})

        if asset_type == 'wml_model':
            payload_input.update({'content_status': {
                "state": "persisted"}})
            if 'trainingDataSchema' in meta_props and meta_props['trainingDataSchema'] is not None:
                training_schema_field = meta_props['trainingDataSchema']['fields']
                training_data_reference=[
                    {'location': {'bucket': 'not_applicable'},
                     'type': 'fs',
                     'connection': {'access_key_id': 'not_applicable',
                                    'secret_access_key': 'not_applicable',
                                    'endpoint_url': 'not_applicable'},
                     'schema': {
                         'id': '1',
                         'type': 'struct',
                         'fields': training_schema_field
                     }}]
                payload_input.pop('trainingDataSchema')
                payload_input.update({'training_data_references': training_data_reference})
        cams_payload = {
            "metadata": payload_metadata,
            "entity": {
                asset_type: payload_input
            }
        }
        return cams_payload

    def _wsd_create_asset(self, asset_type, input_payload, meta_props, path_to_archive, user_archive_file=False):
        import json
        import copy
        def is_xml(model_filepath):
            return os.path.splitext(os.path.basename(model_filepath))[-1] == '.xml'

        params = self._client._params()
        headers = self._client._get_headers()
        url = self._href_definitions.get_wsd_model_href()

        if asset_type != 'wml_model_definition':
            cams_entity = copy.deepcopy(input_payload)
            #cams_entity.pop('name')
            if cams_entity.get('description') is not None:
                cams_entity.pop('description')
            cams_payload = self._create_wsd_payload(asset_type, cams_entity, meta_props)
        else:
            cams_payload = copy.deepcopy(input_payload)
        try:
            atype_body = {
                "name": asset_type
            }
            atype_payload = json.dumps(atype_body, separators=(',', ':'))
            atype_url = self._href_definitions.get_wsd_asset_type_href()
            aheaders = {
                'Content-Type': "application/json"
            }
            asset_type_response = requests.post(
                atype_url,
                params=params,
                data=atype_payload,
                headers=aheaders,
                verify=False
            )

            if asset_type_response.status_code != 200 and \
                    asset_type_response.status_code != 201 and asset_type_response.status_code != 409:
                raise WMLClientError("Failed to create asset type. Try again.")

            create_response = requests.post(
                url,
                params=params,
                json=cams_payload,
                headers=headers,
                verify=False
            )
            asset_res_text = 'creating new ' + asset_type[4:]
            asset_details = self._handle_response(201, asset_res_text, create_response)
            # Upload model content to desktop project using polyfill
            if create_response.status_code == 201:
                asset_uid = create_response.json()["metadata"]["asset_id"]

                if type(path_to_archive) is STR_TYPE:
                    file_name_to_attach = path_to_archive.rsplit("/")[-1]
                else:
                    file_name_to_attach = 'function_attachment'
                if asset_type == 'data_asset':
                    content_upload_url = self._href_definitions.get_wsd_model_attachment_href() + \
                                         urllib.parse.quote(asset_type + "/" + input_payload['name'],safe='')
                else:
                    content_upload_url = self._href_definitions.get_wsd_model_attachment_href() + \
                                     urllib.parse.quote(asset_type + "/" + asset_uid + "/" + file_name_to_attach, safe='')
                attach_url = self._href_definitions.get_model_definition_assets_href() + "/" + \
                             urllib.parse.quote(asset_uid + "/attachments")
                if type(path_to_archive) is STR_TYPE:
                    with open(path_to_archive, 'rb') as f:
                        fdata = f.read()
                else:
                    fdata = path_to_archive

                if is_xml(path_to_archive):
                    response = requests.put(
                        content_upload_url,
                        files={'file': ('native', fdata, 'application/xml', {'Expires': '0'})},
                        params=params,
                        verify=False
                    )
                else:
                    response = requests.put(
                        content_upload_url,
                        files={'file': ('native', fdata, 'application/gzip', {'Expires': '0'})},
                        params=params,
                        verify=False
                    )

                if response.status_code == 201:
                    # update the attachement url with details :
                    if asset_type == 'data_asset':
                        asset_body = {
                            "asset_type": asset_type,
                            "name": input_payload['name'],
                            "mime": input_payload['mime_type'],
                            "object_key": input_payload['name'],
                            "object_key_is_read_only": True
                        }
                    else:
                        asset_body = {
                            "asset_type": asset_type,
                            "name": "native",
                            "object_key": asset_uid + "/" + file_name_to_attach,
                            "object_key_is_read_only": True
                        }
                    attach_payload = json.dumps(asset_body, separators=(',', ':'))

                    attach_response = requests.post(attach_url,
                                                    data=attach_payload,
                                                    params=params,
                                                    headers=headers,
                                                    verify=False)
                    if attach_response.status_code == 201:
                        # remove the tmp file create for content upload
                        if asset_type != 'data_asset':
                            if type(path_to_archive) is STR_TYPE and os.path.isfile(path_to_archive) \
                                    and user_archive_file is False:
                                os.remove(path_to_archive)
                            return self._wsd_get_required_element_from_response(asset_details)
                        else:
                            return asset_details
                    else:
                        self._wsd_delete_asset(asset_uid)
                        raise WMLClientError("Failed while creating a model. Try again.")
                else:
                    self._wsd_delete_asset(asset_uid)
                    raise WMLClientError("Failed while creating a model. Try again.")
            else:
                raise WMLClientError("Failed while creating a model. Try again.")
        except Exception as e:
            raise e

    def _wsd_delete_asset(self, asset_type, asset_id):
        asset_uid = str_type_conv(asset_id)
        delete_endpoint = self._href_definitions.get_model_definition_assets_href() + "/" + asset_uid
        self._logger.debug(u'Deletion artifact {} endpoint: {}'.format(asset_type, delete_endpoint))
        response_delete = requests.delete(delete_endpoint, params=self._client._params(),
                                              headers=self._client._get_headers(), verify=False)
        return response_delete

    def _wsd_get_asset_details(self, asset_type, asset_id, limit=None):
        url = self._href_definitions.get_model_definition_assets_href()
        return self._get_artifact_details(url, asset_id, limit, asset_type)

    def _wsd_get_required_element_from_response(self, response_data):
        WMLResource._validate_type(response_data, u'model response', dict)
        try:
            if self._client.default_project_id is not None and self._client.WSD:
                href = "/v2/assets/" + response_data['metadata']['asset_type'] + "/" +response_data['metadata']['asset_id'] + "?" + "project_id=" + response_data['metadata']['project_id']
                metadata_val = {'project_id': response_data['metadata']['project_id'],
                                       'asset_id': response_data['metadata']['asset_id'],
                                       'href': href,
                                       'name': response_data['metadata']['name'],
                                       'asset_type': response_data['metadata']['asset_type'],
                                       'created_at': response_data['metadata']['created_at'],
                                       'last_updated_at': response_data['metadata']['usage']['last_updated_at']
                                       }
                if 'description' in response_data['metadata'] and response_data['metadata']['description'] is not None:
                    metadata_val.update({u'description': response_data['metadata']['description']})

                new_el = {'metadata': metadata_val,
                          'entity': response_data['entity']
                          }

                return new_el
            else:
                return response_data
        except Exception as e:
            raise WMLClientError("Failed to read Response from down-stream service: " + response_data)

    def _create_revision_artifact(self, base_url, uid, resource_name):
        op_name = 'Creation revision for {}'.format(resource_name)
        if self._client.default_project_id is not None:
           input_json = {
                "project_id": self._client.default_project_id
            }
        else:
            input_json = {
                "space_id": self._client.default_space_id
            }

        url = base_url + u'/' + uid + "/revisions"
        if not self._ICP and not self._client.WSD:
            response = requests.post(url, headers=self._client._get_headers(),
                                     json=input_json)
        else:
            response = requests.post(url, headers=self._client._get_headers(),
                                     json=input_json, verify=False)
        return self._handle_response(201, op_name, response)

