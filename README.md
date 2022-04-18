# IoT Analytics Dashboard
This is a Flask application meant to calculate and display data from user uploaded files that were generated from their attempts at programming a cobot.

## Contacts
* Danielle Stacy

## Solution Components
* Python 3.9
* Flask
* Chart.js

## Installation/Configuration
Clone this repository with `https://github.com/gve-sw/gve_devnet_iot_analytics_dashboard`

#### Run on Docker container (Recommended)
1. The instructions for how to build the Docker image are contaied in the `Dockerfile`. Build the image with the following command:
```
$ docker build -t [give docker image a name] .
```
2. To create a container from the image you built in the previous step, use the following command:
```
$ docker run -d -p 5000:5000 [name given to docker image in previous step]
```
The -d tag is optional, but it allows the container to run in detached mode.

#### Run on local machine (Not recommended)
1. Set up Python virtual environment. Make sure Python 3 is installed in your environment, and if not, you may download Python [here](https://www.python.org/downloads/). Once Python 3 is installed in your environment, you can activate the virtual environment with the instructions found [here](https://docs.python.org/3/tutorial/venv.html).
2. Install the requirements with pip3 install -r requirements.txt
3. Set the environmental settings with the following commands:
```
$ export FLASK_APP=src
$ export FLASK_ENV=development
```
4. To initialize the database (this is only needed on the first use), use the command:
```
$ flask init-db
```
5. To start the application, use the command:
```
$ flask run
```


## Usage
#### Access dashboard
You may access the dashboard by opening the browser of your choice and entering the address 127.0.0.1:5000

#### Home page
From here, a user can view the statistics of the users who have previously uploaded data to the portal. The data in the portal is divided into 6 different tabs: Engagement Scores, Programming Times, Decision Times, Command Times, Cycle Times, Performance Scatterplot, and Decision vs Cycle Time Scatterplot. The first 5 tabs will display a table of the different scores calculated for each user from the data they uploaded. The remaining 2 tabs display scatter charts of data pulled from the users' scores. The Performance Scatterplot displays the data from the Engagement Scores of the users with the x axis representing the average front scores and the y axis representing the average back scores. The Decision Time vs Cycle Time Scatterplot displays the data from the Decision Times and Cycle Times of the users with the x axis representing the decision time and the y axis representing the cycle time. Hovering over the data point will show the time that the user associated with that data point uploaded the data to receive that score.

#### Log In/Register User
To log in or register a user, click on the Login or Register button on the sidebar. To register a new user, enter a unique username and password. Then the user may sign in with those credentials on the Login page.

#### Home page after login
The home page will contain the same information as the home page did before the user logged in, but now the datapoints that correspond to the logged in user are colored red while the rest are blue.

#### Personal stats
The sidebar now contains another button that the user can click to view the logged in user's personal stats. This data is divided into 5 different tabs: Engagement Scores, Programming Times, Decision Times, Command Times, and Cycle Times. Each tab contains a table that shows the logged in user's calculated scores for each of those tabs as well as the date and time they uploaded the data that returned those scores. The Decision Times tab and the Cycle Times tab also display a line graph indicated the variation in performance within those two scores among the user's uploaded data. The x axis represents the time that the user uploaded the data, and the y axis represents the score that the user received for that metric from the data uploaded at the time.

#### Upload data
This is another button generated on the sidebar once the user logs in. To generate a score to display on the dashboard, upload the programming csv file, pos_programming csv file, back csv file, front csv file, and text file into the appropriate file fields. The application expects all files to be added at once and each file should be put in the appropriate field so that it is formatted the way the application expects. Once the files have been selected, click the upload button and the application will save the data from the files into the database and calculate the scores to display on the portal.

#### Upload data through script (optional)
A script has been written to automate the uploading of data. The script depends on the users associated with the data files to already have been added to the portal. To add users to the portal, view the steps listed above for registering a new user. Additionally, the script expects the data files to be in a directory named `Data` that is in the `gve_devnet_iot_analytics_dashboard` at the same level as the `src` directory. The `Data` directory should contain directories named after the users. Within those directories, there should be the 5 files that are generated from the Cobot (programming, pos_programming, front, back, and a text file). Note that if one user has multiple results that they would like to upload using this script, the script will have to be run multiple times, each time replacing the previous data files with the new data files. To run the script, use the command `flask upload-files`. This script was not written to be used with the Docker container and would require additions to the Dockerfile to work.


# Screenshots

![/IMAGES/0image.png](/IMAGES/0image.png)

Home page:
![/IMAGES/home.png](/IMAGES/home.png)

Register page:
![/IMAGES/register.png](/IMAGES/register.png)

Login page:
![/IMAGES/login.png](/IMAGES/login.png)

Engagement scores tab from home page:
![/IMAGES/home_engagement.png](/IMAGES/home_engagement.png)

Programming times tab from home page:
![/IMAGES/home_programming.png](/IMAGES/home_programming.png)

Decision times tab from home page:
![/IMAGES/home_decision.png](/IMAGES/home_decision.png)

Command times tab from home page:
![/IMAGES/home_command.png](/IMAGES/home_command.png)

Cycle times tab from home page:
![/IMAGES/home_cycle.png](/IMAGES/home_cycle.png)

Performance scatterplot tab from home page:
![/IMAGES/performance_plot.png](/IMAGES/performance_plot.png)

Decision times vs Cycle times scatterplot tab from home page:
![/IMAGES/decision_vs_cycle.png](/IMAGES/decision_vs_cycle.png)

Engagement scores tab from personal stats page:
![/IMAGES/personal_engagement.png](/IMAGES/personal_engagement.png)

Programming times tab from personal stats page:
![/IMAGES/personal_programming.png](/IMAGES/personal_programming.png)

Decision times tab from personal stats page:
![/IMAGES/personal_decision.png](/IMAGES/personal_decision.png)

Command times tab from personal stats page:
![/IMAGES/personal_command.png](/IMAGES/personal_command.png)

Cycle times tab from personal stats page:
![/IMAGES/personal_cycle.png](/IMAGES/personal_cycle.png)

Upload page:
![/IMAGES/upload.png](/IMAGES/upload.png)

Directory structure to use flask upload-files command (optional):
![/IMAGES/file_structure.png](/IMAGES/file_structure.png)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.
