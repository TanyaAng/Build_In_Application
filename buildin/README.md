## BUILDIN

### WEB APPICATION FOR PROJECT MANAGEMENT FOR DESIGN ENGINEERS

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">API endpoints</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

### About The Project

BuildIn - Django web application for project management in field of structural engineeering.
This app targets small to large design companies and allows their teams to manage their projects in real time with a lot
of features.

- User model is implemented by extending Django user - there are two separate models: User model and Profile model with
  one-to-one relationship;
- personalized dashboard to any user - every user can see only the projects, which the same user created (<b>owner</b>)
  and projects, in which other user involved in as a <b>participant</b>;
- profile information - provides information about profile and list display of all user tasks, in which the current user
  is involved;
- <b>CRUD</b> operations of a <b>project</b> are allowed only for <b>owner of the project</b> and <b>superuser</b>;
- create <b>tasks</b> to different projects - every user, who can access a concrete project, has all CRUD operations to
  tasks of this project; every task has two additional model relations to user - one for designer of the task and
  another one for engineer, who have to check the quality of the task;
- <b>comment section</b> of every task - every user who can access a project, can create a comment to a task of this
  project, user can edit or delete own comments, superuser can only delete other user's comment;
- LogActivity views - only superusers and admin users can access this view - it is readonly view - the models save
  information about all activities on creation or deleting of any other django models;

<p align="right"><a href="#top">back to top</a></p>

#### Build With

* [Python](https://www.python.org/)
* [Django](https://www.django-rest-framework.org/)
* [Docker](https://www.docker.com/)

### Getting Started

#### Installation

1. Clone the repo
   ```sh
   https://github.com/TanyaAng/Build_In_Application.git
   ```
2. Install all Python libraries
   ```sh
   pip install -r requirements.txt
   ```

<p align="right"><a href="#top">back to top</a></p>

### Usage
LIVE LINK: https://buildin.tk

1. Home View - public access
![home_page](https://user-images.githubusercontent.com/18015470/207098928-704a5cb1-eeb6-408c-8815-a89e6737994f.PNG)

2. Dashboard - when user is logged in
![dashboard](https://user-images.githubusercontent.com/18015470/207099019-827a878a-4853-4ff4-9cb2-5830b7cfe585.PNG)


3. Add New Project
![add_project](https://user-images.githubusercontent.com/18015470/207099046-58403283-c371-4f03-8143-ba969c081455.PNG)


4. Edit Project
![edit-project](https://user-images.githubusercontent.com/18015470/207099072-c485c9b4-758b-4f57-96fd-3f8d299f6a6b.PNG)

5. Delete Project
![delete-project](https://user-images.githubusercontent.com/18015470/207099091-7fdfcb92-265d-4f4d-b386-c3677e816f7e.PNG)

6. Project Details:
![project_details](https://user-images.githubusercontent.com/18015470/207099131-af7e4309-800a-4340-8ba8-c96fd05f5c83.PNG)

7. Project Contacts:
![project-contacts](https://user-images.githubusercontent.com/18015470/207099156-336ff02f-4dcc-4885-a379-38db70d65ce6.PNG)

8. Task Comment section:
![comment-section](https://user-images.githubusercontent.com/18015470/207099186-a3147f78-9281-4461-aa90-14e51bdaf8ca.PNG)

9. Profile Details: 
![profile_details](https://user-images.githubusercontent.com/18015470/207099218-df55faad-bb88-47dc-8b98-a9a0fc6012eb.PNG)

10. Log Activity:
![log-activity](https://user-images.githubusercontent.com/18015470/207099251-7998f79a-cb4e-4a82-8e27-16855746b7b7.PNG)


    
<p align="right"><a href="#top">back to top</a></p>

### License

MIT License

<p align="right"><a href="#top">back to top</a></p>

### Contact

Tanya Angelova - [LinkedIn](https://www.linkedin.com/in/tanya-angelova-44b03590/) - t.j.angelova@gmail.com

Project Link: [github link]

<p align="right"><a href="#top">back to top</a></p>

[LinkedIn]: https://www.linkedin.com/in/tanya-angelova-44b03590/

[github link]: https://github.com/TanyaAng/Build_In_Application.git
