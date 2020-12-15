# hasbro-pulse
## Installation
Required Libraries : Requests, lxml, BeautifulSoup4

```shell
$ git clone https://github.com/ronpichardo/pulse.git
$ cd pulse
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```
1. Next, open up the config.example.json file and fill out the fields with the relevant information.(Address for checkout not yet implemented, keyword is required to find the product)
ex. if product title is "Star Wars The Black Series Bo-Katan Kryze"

![image](https://user-images.githubusercontent.com/63974878/102283625-c4d86d00-3f00-11eb-89bf-3732168dc943.png)

2. File, Save as 'config.json' or save and run the following from terminal
> $ cp config.example.json config.json


## Usage
Using the script after the installation is complete, and the config.json file is completed
```shell
$ python3 pulse.py
```
Output:
![image](https://user-images.githubusercontent.com/63974878/102284619-74620f00-3f02-11eb-8e9c-025518b5ff6f.png)

prints out the checkout link for a product that you are looking to purchase from hasbropulse.com

