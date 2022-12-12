from django.contrib.auth import get_user_model
from django.test import TestCase

from buildin.accounts.models import ParticipantRole, Profile
from buildin.projects.models import BuildInProject, ProjectPhases
from buildin.tasks.models import ProjectTask

UserModel = get_user_model()


class BaseTestCase(TestCase):
    email_credentials = 'user@it.com'
    password_credentials = '12345'

    profile_first_name = 'Marina'
    profile_last_name = 'Petrova'
    participant_role = ParticipantRole.choices()[3][0]

    project_identifier = 'BG100'
    project_name = 'Hotel'
    project_phase = ProjectPhases.choices()[2][0]
    client_name = 'Arch Studio'
    deadline_date = '2023-05-06'

    task_id = 'FP101'
    task_name = 'Plan at storey 3th'

    def create_and_login_user(self):
        credentials = {
            'email': self.email_credentials,
            'password': self.password_credentials
        }
        user = UserModel.objects.create_user(**credentials)
        self.client.login(**credentials)
        return user

    def create_login_and_make_profile_of_user(self):
        credentials = {
            'email': self.email_credentials,
            'password': self.password_credentials
        }
        profile_info = {
            'first_name': self.profile_first_name,
            'last_name': self.profile_last_name,
            'participant_role': self.participant_role
        }

        user = UserModel.objects.create_user(**credentials)
        self.client.login(**credentials)
        profile = Profile.objects.create(**profile_info, user=user)
        return user, profile

    def create_and_login_user_by_credentials(self, **credentials):
        user = UserModel.objects.create_user(**credentials)
        self.client.login(**credentials)
        return user

    def create_user_by_credentials(self, **credentials):
        return UserModel.objects.create_user(**credentials)

    def create_profile_by_user_and_info(self, user, **profile_info):
        return Profile.objects.create(**profile_info, user=user)

    def create_and_save_multiple_projects_of_user(self, user):
        projects = []
        for i in range(1, 10):
            project = BuildInProject(
                project_identifier=100 + i,
                project_name=f'Residential Building on {i}th street',
                owner=user,
            )
            project.full_clean()
            project.save()
            projects.append(project)
        return projects

    def create_and_save_multiple_tasks_by_user_and_project(self, user, project):
        tasks = []
        for i in range(1, 3):
            task = ProjectTask(
                task_id=f'FP{100 + i}',
                task_name=f'Plan for storey {i}',
                time_estimation=i,
                designer=user,
                project=project,
            )
            task.full_clean()
            task.save()
            tasks.append(task)

        return tasks

    def create_and_save_project_of_user(self, user):
        project_info = {
            'project_identifier': self.project_identifier,
            'project_name': self.project_name,
            'project_phase': self.project_phase,
            'client_name': self.client_name,
            'deadline_date': self.deadline_date,
            'owner': user,
        }

        project = BuildInProject(**project_info)
        project.full_clean()
        project.save()

        return project

    def create_and_save_task_of_project(self, project):
        task_info = {
            'task_id': self.task_id,
            'task_name': self.task_name,
            'project': project,
        }
        task = ProjectTask(**task_info)
        task.full_clean()
        task.save()
        return task
