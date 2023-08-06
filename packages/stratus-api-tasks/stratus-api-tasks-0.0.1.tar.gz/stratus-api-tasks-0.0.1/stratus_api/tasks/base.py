def create_celery_app(project_folder):
    """Creates a celery app based on the celery setting pulled from environment variables.
        DO NOT DELETE the `import tasks`

        :return: celery app
        """
    from stratus_api.core.settings import get_settings
    from celery import Celery
    from celery.signals import import_modules
    celery_settings = get_settings(settings_type='celery')

    celery_settings['imports'] = collect_app_tasks(project_folder=project_folder) + collect_framework_tasks()
    print(celery_settings['imports'])
    celery_app = Celery(__name__)
    celery_app.config_from_object(celery_settings, force=True)
    return celery_app


def collect_app_tasks(project_folder):
    import os
    tasks = set()
    for i in os.walk(os.path.join(project_folder, 'tasks')):
        base = i[0].replace(project_folder, '').replace('/', '.')
        tasks.add(base)
        for f in [f.replace('.py', '') for f in i[-1] if f.endswith('.py') and f not in {'__init__.py','__pycache__.py'}]:
            tasks.add(base + '.' + f)
    return list(tasks)


def collect_framework_tasks():
    import os
    framework_dir = os.path.abspath(__file__).replace('/tasks/base.py', '')
    print(framework_dir)
    tasks = set()
    for root, folders, files in os.walk(framework_dir):
        if ('tasks' in root and 'stratus_api/tasks' not in root) or 'stratus_api/tasks/tasks' in root:
            base = root.replace(framework_dir, 'stratus_api').replace('/', '.')
            tasks.add(base)
            for f in [f.replace('.py', '') for f in root[-1] if f.endswith('.py') and f not in {'__init__.py','__pycache__.py'}]:
                tasks.add(base + '.' + f)
    print(tasks)
    return list(tasks)
