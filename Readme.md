# Google Cloud Billing Dashboard

## Introduction
This application collects and displays charts of Google Cloud Billing exports to facilitate analysis of overall cloud spend.

The app is built using Flask for api calls , AngularJS for front end , D3.js for data visualization, SQL DB to store the data and a scheduler(python) to read the JSON file created by Google and update the DB.    

The default setup assumes you're running within GCP itself, rather than locally, to take advantage of (Application Default Credentials)[https://developers.google.com/identity/protocols/application-default-credentials]

### Quick Start
The easiest way to try out the system is to use [Docker](https://docs.docker.com/) 1.9 and [Docker Compose](https://docs.docker.com/compose/) 1.6.
The following commands will install, link and run the components.

  $ docker-compose build  
  $ docker-compose up  

Once running you'll be able to access the app on port 80 of your docker host IP.

On a mac simply run:

  $ open "http://$(docker-machine ip default)/"


## Additional Configurations

###  Google Storage Bucket Details
1. Enable Billing Export
  - Google provides the ability to [export your billing](https://support.google.com/cloud/answer/6293835?rd=1) information to a storage bucket as **JSON** as the data processing feature expects a JSON file to process the data. The process runs nightly so you'll need to wait until it runs after you enable the feature.
2. Permissions on the Main and Archive buckets to read and write as we have to update the metadata on the file, move it to archive  and also delete once data has been processed.

### Database Settings
1. Modify the **common.env** with the corresponding values  
  * MYSQL_ROOT_PASSWORD=password
  * MYSQL_DATABASE=db_name
  * MYSQL_USER=db_user
  * MYSQL_PASSWORD=db_password    
 
### Bucket Settings
1. Modify the **common.env** with the corresponding values  
  * BUCKET_NAME=bucket-name
  * ARCHIVE_BUCKET_NAME=archive-bucket-name

### Scheduler Settings
1. Modify the **common.env** with the corresponding values  
  * SCHEDULER_HOUR=0-23
  * SCHEDULER_MIN=0-59

### View Quota link Setting
1. Modify the **common.env** with the corresponding values
  * QUOTA_VIEW=True or False  
When set to **True** it will have the link to view the Metrics Usage for all projects else it is hidden in the navbar. In order to have the data from other projects, the current project in which the code is deployed should have access to read all the projects and this is possible by adding the service account of this project into the other projects(https://cloud.google.com/docs/permissions-overview).

### For local developlement 
  If running locally add the path to the JSON file for the service account in apps_config.py -- 'GOOGLE_APPLICATION_CREDENTIALS' and place the file under web/billing-app/.  


### Load Data into DB
By default the scheduler is set to process the data everyday at the time set using the env variables SCHEDULER_HOUR and SCHEDULER_MIN. To run the procss immediatley use **/billing/loadData** and to change the scheduler timming use **/billing/loadData?hour=0-23&min=0-59**, this will reset the scheduler.  


### Technologies

* Python > 2.0
* [Flask] -- Render the main page and API calls that make DB calls
* SQLAlchemy -- Used so that any DB SQLITE or MYSQL can be used as backend
* [AngularJS] -- Front End routing, templating,etc.
* [Twitter Bootstrap] -- For RWD
* [node.js] --  For Build Process
* [Grunt] -- Minify and Concat all the assets
* [jQuery] -- For some Js features
* [D3.js] -- Data visualization
* [NVD3.js] -- Data visualization library based on D3.js


## URLS 
Landing page  :   
  **/**   
   Billing Cost per cost center :   
   **/billing**   
   Overall cost for all cost centers UI :  
   **/billing/cost_center/#?span=year&span_value=2015&&view_by=month&cost_center=all&project=all&resource=all**  
   Overall cost for all cost centers API :  
   **/billing/usage/2016?span=year&span_value=2015&&view_by=month&cost_center=all&project=all&resource=all**  
   By changing the parameters in the url you can get the corresponding data.   
   Change the scheduler time with the hour and min specified in the url :  
   **/billing/loadData?hour=0-23&min=0-59**   
   To run the data loading process immediatley :   
   **/billing/loadData**  
   Once logged in to update projects :   
   **/billing/projects**  
   There is a login button that will control who can add project into info into the 'Project' table. By default only 'test' user  and password. You can update the users logic in login/views.py.  
   To see the CPU and other metrics across all projects and cost centers use :  
   **/quota/**   
   To use the API call for a given project:  
   **/quota/<project-name>**  
   To see Director Level billing:  
   **/billing/director**  
   Api to get the support cost:  
   **/billing/usage/support_cost**
   
   

## License
Open source under Apache License v2.0 (http://www.apache.org/licenses/LICENSE-2.0)

   [Billing App Flask Repo]: <https://github.com/homedepot/GoogleBillingDashboard>
   [node.js]: <http://nodejs.org>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [jQuery]: <http://jquery.com>
   [AngularJS]: <http://angularjs.org>
   [Grunt]: <http://gruntjs.com>
   [D3.js]: <http://d3js.org>
   [NVD3.js]:  <http://nvd3.org/>
   [Flask]: <flask.pocoo.org>
   [reporting.db]: <https://github.com/homedepot/GoogleBillingDashboard/blob/master/web/billing-app/reporting.db>
