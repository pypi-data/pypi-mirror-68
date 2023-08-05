import requests

class Server:
    def __init__(self, address, port):
        self.address = 'http://' + str(address)
        self.port = str(port)
        self.address.strip()
        self.port.strip()


class Project:
    def __init__(self, name, token, server, clean=False):
        self.name = name
        self.token = token
        self.address = server.address
        self.port = server.port
        self.clean = clean
        self.register()

    def register(self):
        # add publisher
        r = requests.post(self.address + ':' + self.port + '/publisher/add',
                          data={'name': self.name, 'pwd': self.token,
                                'clean': self.clean})

        if r.status_code != 200 or r.json().get('code') != 200:
            raise Exception("Token 错误！！！")

    def add_task(self, name, msg):
        # add task
        r = requests.post(self.address + ':' + self.port + '/publisher/task/add',
                          data={'pname': self.name, 'ppwd': self.token,
                                'name': name, 'msg': msg})
        if r.status_code != 200 or r.json().get('code') != 200:
            raise Exception("Task 创建失败！！！")
        else:
            return Task(self, name, msg)

    def update_task(self, name, state):
        # update task state
        result = True
        try:
            r = requests.post(self.address + ':' + self.port + '/publisher/task/update',
                              data={'pname': self.project.name, 'ppwd': self.project.token,
                                    'name': name, 'state': state})
            if r.status_code != 200 or r.json().get('code') != 200:
                print("更新任务{" + name + "}到{" + state + "}状态失败")
                result = False
        finally:
            return result

    def finish_task(self, name):
        # finish task
        result = True
        try:
            r = requests.post(str(self.address) + ':' + str(self.port) + '/publisher/task/finish',
                              data={'pname': str(self.name), 'ppwd': str(self.token),
                                    'name': str(name)})
            if r.status_code != 200 or r.json().get('code') != 200:
                print("更新任务{" + str(name) + "}到{Finished}状态失败")
                result = False
        finally:
            return result

    def remove_task(self, name):
        # remove task
        result = True
        try:
            r = requests.delete(self.address + ':' + self.port + '/publisher/task/remove',
                                data={'pname': self.name, 'ppwd': self.token,
                                      'name': name})
            if r.status_code != 200 or r.json().get('code') != 200:
                print("移除任务{" + name + "}失败")
                result = False
        finally:
            return result

    def unregister(self):
        # unregister publisher
        result = True
        try:
            r = requests.delete(self.address + ':' + self.port + '/publisher/remove',
                                data={'name': self.name, 'pwd': self.token})
            if r.status_code != 200 or r.json().get('code') != 200:
                print("移除项目{" + name + "}失败")
                result = False
        finally:
            return result


class Task:
    def __init__(self, project, name, onfinished_msg):
        self.project = project
        self.name = str(name).strip()
        self.onfinished_msg = str(onfinished_msg).strip()

    def update_state(self, newstate):
        newstate = str(newstate).strip()
        return self.project.update_task(self.name, newstate)

    def finish(self):
        return self.project.finish_task(self.name)

    def remove(self):
        return self.project.remove_task(self.name)

if __name__ == "__main__":
	pass

