## Project: Search and Sample Return
---

**The goals / steps of this project are the following:**  

* The main goal of this project is to guide the Rover to navigate & map a terrain by providing it the necessary instructions to "perceive" and interpret its field of vision (i.e. path & surroundings) and "decide" on how to navigate the terrain.
* The Rover also should detect and pickup "rock" samples that it comes across its way.

**Training / Calibration**  

* The training video is located at https://github.com/Frame02/RoboND-Rover-Project/blob/my_proj_branch/output/test_mapping.mp4

**Autonomous Navigation / Mapping**
 
* I filled the perception_step(...) and decision_step(...) in `perception.py` and  `decision.py` with appropriate steps for image processing and decision making.
* I iterated the perception and decision steps multiple times to come up with reasonable metrics for Rover navigation and mapping.

[//]: # (Image References)


[Training image 1]: https://github.com/Frame02/RoboND-Rover-Project/blob/my_proj_branch/IMG/robocam_2017_06_04_22_38_11_937.jpg
[Training image 2]: https://github.com/Frame02/RoboND-Rover-Project/blob/my_proj_branch/IMG/robocam_2017_06_04_22_38_19_873.jpg 

## [Rubric](https://review.udacity.com/#!/rubrics/916/view) Points
### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---

### Notebook Analysis
#### 1. Run the functions provided in the notebook on test images (first with the test data provided, next on data you have recorded). Add/modify functions to allow for color selection of obstacles and rock samples.
Here is an example of how to include an image in your writeup.

![alt text][image1]

#### 1. Populate the `process_image()` function with the appropriate analysis steps to map pixels identifying navigable terrain, obstacles and rock samples into a worldmap.  Run `process_image()` on your test data using the `moviepy` functions provided to create video output of your result. 
And another! 

![alt text][image2]
### Autonomous Navigation and Mapping

#### 1. Fill in the `perception_step()` (at the bottom of the `perception.py` script) and `decision_step()` (in `decision.py`) functions in the autonomous mapping scripts and an explanation is provided in the writeup of how and why these functions were modified as they were.


#### 2. Launching in autonomous mode your rover can navigate and map autonomously.  Explain your results and how you might improve them in your writeup.  

**Note: running the simulator with different choices of resolution and graphics quality may produce different results, particularly on different machines!  Make a note of your simulator settings (resolution and graphics quality set on launch) and frames per second (FPS output to terminal by `drive_rover.py`) in your writeup when you submit the project so your reviewer can reproduce your results.**

I tried to implement wall-following algorithm to guide the Rover to navigate its terrain. I also implemented the functionality to guide the Rover whenever it sees the rock sample and pick up the same. However, the fidelity of the produced map is low despite of updating the map only when Rover's roll and pitch angles are low.


![alt text][image3]


