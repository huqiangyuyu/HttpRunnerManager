import os

from django.core.exceptions import ObjectDoesNotExist
from httprunner import exceptions, logger
from ApiManager.models import TestCaseInfo, ApiInfo, ModuleInfo, ProjectInfo, DebugTalk, TestSuite
from ApiManager.utils.testcase import dump_python_file, dump_yaml_file


def run_by_single(index, base_url, path):
    """
    加载单个case用例信息
    :param index: int or str：用例索引
    :param base_url: str：环境地址
    :return: dict
    """
    # obj = TestSuite.objects.get(id=index)
	#
    # include = eval(obj.include)
    # suite_dict = {'config':
    #                   {'name': 'testsuite'}}
    # list_data = []
    # try:
    #     for val in include:
    #         suite_dir_path, test_suite, suite_data = run_by_single_suite(val[0],
    #                                                                      base_url,
    #                                                                      path)
    #         list_data.append(suite_data)
    #     suite_dict['testcases'] = list_data
    #
    # except:
    #     print('数据格式错误')

    config = {
        'config': {
            'name': '',
            'request': {
                'base_url': base_url
            }
        }
    }
    testcase_list = []
    api_dict = {}
    # suite_list = []
    testcase_dict = {}

    # testcase_list.append(config)

    try:
        obj = TestCaseInfo.objects.get(id=index)
    except ObjectDoesNotExist:
        return testcase_list

    include = eval(obj.include)
    request = eval(obj.request)
    name = obj.name
    project = obj.belong_project
    module = obj.belong_module.module_alias

    config['config']['name'] = name

    testcase_dir_path = os.path.join(path, project)

    if not os.path.exists(testcase_dir_path):
        os.makedirs(testcase_dir_path)

        try:
            debugtalk = DebugTalk.objects.get(
                belong_project__project_name=project).debugtalk
        except ObjectDoesNotExist:
            debugtalk = ''

        dump_python_file(os.path.join(testcase_dir_path, 'debugtalk.py'),
                         debugtalk)

    api_dir_path = os.path.join(testcase_dir_path, 'api')
    case_dir_path = os.path.join(testcase_dir_path, 'testcases')
    if not os.path.exists(api_dir_path):
        os.mkdir(api_dir_path)
    if not os.path.exists(case_dir_path):
        os.mkdir(case_dir_path)
    for test_info in include:
        try:
            if isinstance(test_info, dict):
                config_id = test_info.pop('config')[0]
                config_request = eval(
                    TestCaseInfo.objects.get(id=config_id).request)
                # config_request.get('config').get('request').setdefault('base_url', base_url)
                config_request['config'].pop('request')
                config_request['config']['name'] = name
                testcase_dict['config'] = config_request['config']

            else:
                id = test_info[0]
                api_name = test_info[1]
                pre_request = eval(ApiInfo.objects.get(id=id).request)
                api_dict['request'] = pre_request['teststeps']['request']
                api_dict['name'] = api_name
                api_dict['base_url'] = 'http://' + base_url
                dump_yaml_file(os.path.join(api_dir_path, api_name + '.yml'),
                               api_dict)
                pre_request['teststeps'].pop('request')
                pre_request['teststeps'][
                    'api'] = 'api/'  + api_name + '.yml'

                testcase_list.append(pre_request['teststeps'])
                testcase_dict['teststeps'] = testcase_list

        except ObjectDoesNotExist:
            return testcase_list

    if request['test']['request']['url'] != '':
        testcase_list.append(request)
    # suite_dict['testcases'] = suite_list
    path = os.path.join(case_dir_path, name + '.yml')
    dump_yaml_file(path, testcase_dict)
    return case_dir_path
    # config = {
    #     'config': {
    #         'name': '',
    #         'request': {
    #             'base_url': base_url
    #         }
    #     }
    # }
    # testcase_list = []
	#
    # testcase_list.append(config)
	#
    # try:
    #     obj = TestCaseInfo.objects.get(id=index)
    # except ObjectDoesNotExist:
    #     return testcase_list
	#
    # include = eval(obj.include)
    # request = eval(obj.request)
    # name = obj.name
    # project = obj.belong_project
    # module = obj.belong_module.module_name
	#
    # config['config']['name'] = name
	#
    # testcase_dir_path = os.path.join(path, project)
	#
    # if not os.path.exists(testcase_dir_path):
    #     os.makedirs(testcase_dir_path)
	#
    #     try:
    #         debugtalk = DebugTalk.objects.get(belong_project__project_name=project).debugtalk
    #     except ObjectDoesNotExist:
    #         debugtalk = ''
	#
    #     dump_python_file(os.path.join(testcase_dir_path, 'debugtalk.py'), debugtalk)
    # testcase_dir_path = os.path.join(testcase_dir_path, module)
	#
    # if not os.path.exists(testcase_dir_path):
    #     os.mkdir(testcase_dir_path)
	#
    # for test_info in include:
    #     try:
    #         if isinstance(test_info, dict):
    #             config_id = test_info.pop('config')[0]
    #             config_request = eval(TestCaseInfo.objects.get(id=config_id).request)
    #             config_request.get('config').get('request').setdefault('base_url', base_url)
    #             config_request['config']['name'] = name
    #             testcase_list[0] = config_request
    #         else:
    #             id = test_info[0]
    #             pre_request = eval(ApiInfo.objects.get(id=id).request)
    #             testcase_list.append(pre_request)
	#
    #     except ObjectDoesNotExist:
    #         return testcase_list
	#
    # if request['test']['request']['url'] != '':
    #     testcase_list.append(request)
	#
    # dump_yaml_file(os.path.join(testcase_dir_path, name + '.yml'), testcase_list)


def run_by_single_suite(index, base_url, path):
    """
    加载单个case用例信息
    :param index: int or str：用例索引
    :param base_url: str：环境地址
    :return: dict
    """
    config = {
        'config': {
            'name': '',
            'request': {
                'base_url': base_url
            }
        }
    }
    testcase_list = []
    api_dict = {}
    # suite_list = []
    testcase_dict = {}

    # testcase_list.append(config)

    try:
        obj = TestCaseInfo.objects.get(id=index)
    except ObjectDoesNotExist:
        return testcase_list

    include = eval(obj.include)
    request = eval(obj.request)
    name = obj.name
    project = obj.belong_project
    module = obj.belong_module.module_alias

    config['config']['name'] = name

    testcase_dir_path = os.path.join(path, 'TFbank')

    if not os.path.exists(testcase_dir_path):
        os.makedirs(testcase_dir_path)

        try:
            debugtalk = DebugTalk.objects.get(belong_project__project_name=project).debugtalk
        except ObjectDoesNotExist:
            debugtalk = ''

        dump_python_file(os.path.join(testcase_dir_path, 'debugtalk.py'), debugtalk)

    api_dir_path = os.path.join(testcase_dir_path, 'api')
    case_dir_path = os.path.join(testcase_dir_path, 'testcases')
    suite_dir_path = os.path.join(testcase_dir_path, 'testsuites')
    if not os.path.exists(api_dir_path):
        os.mkdir(api_dir_path)
    if not os.path.exists(case_dir_path):
        os.mkdir(case_dir_path)
    if not os.path.exists(suite_dir_path):
        os.mkdir(suite_dir_path)
    api_dir_path = os.path.join(api_dir_path, module)
    case_dir_path = os.path.join(case_dir_path, module)
    if not os.path.exists(api_dir_path):
        os.mkdir(api_dir_path)
    if not os.path.exists(case_dir_path):
        os.mkdir(case_dir_path)
    for test_info in include:
        try:
            if isinstance(test_info, dict):
                config_id = test_info.pop('config')[0]
                config_request = eval(TestCaseInfo.objects.get(id=config_id).request)
                # config_request.get('config').get('request').setdefault('base_url', base_url)
                config_request['config'].pop('request')
                # parameters = config_request['config'].pop('parameters')
                # config_request['config']['name'] = name
                # testcase_dict['config'] = config_request['config']
                #获取套件用例
                pre_suite = 'testcases/' + module + '/' + name + '.yml'
                if 'data' in request['test']['request']:
                    suite_name = request['test']['request']['data']['name']
                else:
                    suite_name = name
                # if 'parameters' in config_request['config']:
                #     suite_data = {'name': suite_name, 'testcase': pre_suite,'parameters':config_request['config']['parameters']}
                #     config_request['config'].pop('parameters')
                if 'parameters' in request['test']:
                    suite_data = {'name': suite_name, 'testcase': pre_suite,'parameters':request['test']['parameters']}
                    request['test'].pop('parameters')
                else:
                    suite_data = {'name': suite_name, 'testcase': pre_suite}
                config_request['config']['name'] = name


                testcase_dict['config'] = config_request['config']
                # testcase_dict['config'].pop('setup_hooks')
                # testcase_dict['config'].pop('teardown_hooks')
                # # suite_list.append(suite_data)
            else:
                id = test_info[0]
                api_name = test_info[1]
                pre_request = eval(ApiInfo.objects.get(id=id).request)
                api_dict['request'] = pre_request['teststeps']['request']
                api_dict['name'] = api_name
                api_dict['base_url'] = 'http://'+ base_url
                dump_yaml_file(os.path.join(api_dir_path, api_name + '.yml'),
                               api_dict)
                pre_request['teststeps'].pop('request')
                pre_request['teststeps']['api'] = 'api/'+ module + '/'+ api_name + '.yml'

                testcase_list.append(pre_request['teststeps'])
                testcase_dict['teststeps'] = testcase_list

        except ObjectDoesNotExist:
            return testcase_list

    if request['test']['request']['url'] != '':
        testcase_list.append(request)
    # suite_dict['testcases'] = suite_list
    path = os.path.join(case_dir_path, name + '.yml')
    dump_yaml_file(path, testcase_dict)


    return suite_dir_path,suite_data



def run_by_suite(index, base_url, path):
    obj = TestSuite.objects.get(id=index)

    include = eval(obj.include)
    suite_dict = {'config':
                      {'name': 'testsuite'}}
    list_data = []
    suite_dir_path = ''
    try:
        for val in include:
            suite_dir_path,suite_data = run_by_single_suite(val[0], base_url, path)
            list_data.append(suite_data)
        suite_dict['testcases'] = list_data
        test_suite = 'TFbank_testsuite.yml'
        dump_yaml_file(os.path.join(suite_dir_path, test_suite), suite_dict)
    except:
        print('数据格式错误')
    return suite_dir_path


def run_by_batch(test_list, base_url, path, type=None, mode=False):
    """
    批量组装用例数据
    :param test_list:
    :param base_url: str: 环境地址
    :param type: str：用例级别
    :param mode: boolean：True 同步 False: 异步
    :return: list
    """

    if mode:
        for index in range(len(test_list) - 2):
            form_test = test_list[index].split('=')
            value = form_test[1]
            if type == 'project':
                run_by_project(value, base_url, path)
            elif type == 'module':
                run_by_module(value, base_url, path)
            elif type == 'suite':
                run_by_suite(value, base_url, path)
            else:
                run_by_single(value, base_url, path)

    else:
        if type == 'project':
            for value in test_list.values():
                run_by_project(value, base_url, path)

        elif type == 'module':
            for value in test_list.values():
                run_by_module(value, base_url, path)
        elif type == 'suite':
            for value in test_list.values():
                run_by_suite(value, base_url, path)

        else:
            for index in range(len(test_list) - 1):
                form_test = test_list[index].split('=')
                index = form_test[1]
                run_by_single(index, base_url, path)


def run_by_module(id, base_url, path):
    """
    组装模块用例
    :param id: int or str：模块索引
    :param base_url: str：环境地址
    :return: list
    """
    obj = ModuleInfo.objects.get(id=id)
    test_index_list = TestCaseInfo.objects.filter(belong_module=obj, type=1).values_list('id')
    for index in test_index_list:
        run_by_single(index[0], base_url, path)


def run_by_project(id, base_url, path):
    """
    组装项目用例
    :param id: int or str：项目索引
    :param base_url: 环境地址
    :return: list
    """
    obj = ProjectInfo.objects.get(id=id)
    module_index_list = ModuleInfo.objects.filter(belong_project=obj).values_list('id')
    for index in module_index_list:
        module_id = index[0]
        run_by_module(module_id, base_url, path)


def run_test_by_type(id, base_url, path, type):
    if type == 'project':
        run_by_project(id, base_url, path)
    elif type == 'module':
        run_by_module(id, base_url, path)
    elif type == 'suite':
        path = run_by_suite(id, base_url, path)
    else:
        path = run_by_single(id, base_url, path)
    return path

def run_test_by_env(path):
    #加载配置信息
    env_list = []
    env_request = eval(TestCaseInfo.objects.get(name='env配置').request)
    env_data = env_request['config']['request']['json']
    for key in env_data:
        data = key + '=' + env_data[key]
        env_list.append(data)
    demo_env_content = "\n".join(env_list)

    create_file(os.path.join(path, ".env"), demo_env_content)



def create_file(path, file_content=""):
        with open(path, 'w') as f:
            f.write(file_content)
        msg = "created file: {}".format(path)
        logger.color_print(msg, "BLUE")


def query_module(index):
    obj = TestSuite.objects.get(id=index)
    include = eval(obj.include)
    id = include[0][0]
    obj = TestCaseInfo.objects.get(id=id)
    module = obj.belong_module.module_alias
    return module

def query_case(index):
    obj = TestCaseInfo.objects.get(id=index)
    name = obj.name
    return name