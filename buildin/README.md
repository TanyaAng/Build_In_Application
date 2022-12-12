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
   ![](D:\SOFTUNI\BUILDIN_imgs_github\home_page.PNG)

2. Dashboard - when user is logged in
   ![](D:\SOFTUNI\BUILDIN_imgs_github\dashboard.PNG)

3. Add New Project
   ![](D:\SOFTUNI\BUILDIN_imgs_github\add_project.PNG)

4. Edit Project
   ![](D:\SOFTUNI\BUILDIN_imgs_github\edit-project.PNG)

5. Delete Project
   ![](D:\SOFTUNI\BUILDIN_imgs_github\delete-project.PNG)

6. Project Details:
   ![](D:\SOFTUNI\BUILDIN_imgs_github\project_details.PNG)

7. Project Contacts:
   ![](D:\SOFTUNI\BUILDIN_imgs_github\project-contacts.PNG)

8. Task Comment section:
   ![](D:\SOFTUNI\BUILDIN_imgs_github\comment-section.PNG)

9. Profile Details: 
![](D:\SOFTUNI\BUILDIN_imgs_github\profile_details.PNG)

10. Log Activity:
![](D:\SOFTUNI\BUILDIN_imgs_github\log-activity.PNG)

    
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