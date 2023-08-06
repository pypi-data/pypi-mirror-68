
from terminal import Logger, prompt, password, green, yellow

from ..util import config, client,util, ecs_client, it_config

log = Logger()


def login(region, accessKeyId=None, accessKeySecret=None):
    opt = config.getConfigs(config.COMMON)

    opt['region'] = region

    if region and accessKeyId and accessKeySecret:

        opt['accesskeyid'] = accessKeyId
        opt['accesskeysecret'] = accessKeySecret

    else:
        opt['accesskeyid'] = prompt('input accessKeyId')
        opt['accesskeysecret'] = password('and accessKeySecret')

    try:
        util.check_intranet_region(opt = opt)

        client.check_client(opt)

        # generate_ecs_instance_type_map(opt)

        generate_bcs_instance_type_map(opt)

        config.setConfigs(config.COMMON, opt)

        util.check_default_osspath(opt)

        util.set_default_type_n_image()

        util.check_default_vpc_cidr_block()

        print(green('login success' ))

    except Exception as e:
        e = '%s' % e
        if 'nodename nor servname provided' in e:
            raise Exception('Invalid region %s' % region)
        else:
            raise Exception(e)

def logout():
    config.removeConfig(config.COMMON)

def generate_bcs_instance_type_map(opt):
    result = client.describeInstances(opt)
    m = {}
    for n in result:
        m[n['InstanceType']]={
            'name': n['InstanceType'],
            'cpu': n['CpuCore'],
            'memory': n['MemorySize'],
        }
    it_config.save(m)


# generate ecs instanse type map
def generate_ecs_instance_type_map(opt):
    result = ecs_client.describeInstances(opt)
    m = {}
    for n in result:
        m[n['InstanceTypeId']]={
            'name': n['InstanceTypeId'],
            'cpu': n['CpuCoreCount'],
            'memory': n['MemorySize'],
        }
    it_config.save(m)