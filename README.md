# stonks
random stuff about stocks and fun with numbers


## Running
In order to run clone the repository and set up a python virtual environment (3.7 or higher). 
Use pip to install the requirements. Then `python index.py` to launch the app.

## Apps
### Rotation Graphs
Inspired by [this reddit post](https://www.reddit.com/r/thetagang/comments/mfn4zy/anticipating_the_rotation_march_29_2021/) and others by the same author.
This is a small dash app. It is not yet interactive, but you can adjust the script (dates and ticker list) and then restart the app to visualize the rotations.
I am not 100% confident on the calcualtions yet but they seem to make sense and are headed in the right direction. 

Once the app is launched it will be availabe at http://127.0.0.1:8050/apps/rotation by default.
Use the form to enter a benchmark and several tickers, all comma separated and pick two dates. 
Note that you need to include more than you think for dates because a lot of smoothing happens and 
I have not yet implemented the code to go get dates to go get extra historical data to use in smoothing.
