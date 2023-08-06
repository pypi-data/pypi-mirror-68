#!/usr/bin/python
class exoJSON:
    def __init__(self):
        pass

    @staticmethod
    def JSONParser(jsonVar, param=''):
        _tempJson = jsonVar
        if param == '':
            return jsonVar
        if jsonVar == {}:
            raise Warning("Empty JSON")
        else:
            paramList = param.split('/')
            for p in paramList:
                if p not in list(_tempJson.keys()):
                    raise Exception(
                        "invalid json parameter: {}. Available parameters: {}".format(
                            p, _tempJson.keys()))
                _tempJson = _tempJson[p]
        return _tempJson

    @staticmethod
    def JSONStructure(jsonVar, KEY=''):
        '''
         KEY == '' returns entire structure
         KEY == '__ROOT__' returns only root keys
         if KEY == key, returns the sub-keys under a particular key
        '''
        stack = list(jsonVar.keys())
        result = list(jsonVar.keys())
        if KEY == '__ROOT__':
            return result
        elif KEY != '':
            stack = [KEY]
            result = [KEY]
        _json = jsonVar
        while stack:
            top_element = stack.pop()
            _json = _json[top_element]
            try:
                list_of_keys = list(_json.keys())
                # print(list_of_keys)
                for key in list_of_keys:
                    # print(top_element, end = "-->")
                    # print(key)
                    stack.append(key)
                    result.append(top_element + '/' + key)
            except BaseException:
                return result
