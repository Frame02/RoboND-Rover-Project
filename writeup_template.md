## Project: Search and Sample Return
---

**The goals / steps of this project are the following:**  

* The primary goal of this project is to guide the Rover to navigate & map a terrain by providing it the necessary instructions to "perceive" and interpret its field of vision (i.e. path & surroundings) and "decide" on how to navigate the terrain.
* The Rover also should detect and pick up "rock" samples that it comes across its way.

**Training / Calibration**  

* The training video is present at ./output/test_mapping.mp4

**Autonomous Navigation / Mapping**
 
* I filled in the perception_step(...) and decision_step(...) in `perception.py` and  `decision.py` with appropriate steps for image processing and decision making.
* I iterated the perception and decision steps multiple times to come up with reasonable metrics for Rover navigation and mapping.

[//]: # (Image References)

[Training image 1]: ./IMG/robocam_2017_06_04_22_38_11_937.jpg
[Training image 2]: ./IMG/robocam_2017_06_04_22_38_19_873.jpg 

### Autonomous Navigation and Mapping

* I ran most of the simulations at 800 X 600 resolution.
* I tried to implement wall-following algorithm to guide the Rover to navigate its terrain. I also implemented the functionality to guide the Rover whenever it sees the rock sample and pick up the same.
* However, the fidelity of the produced map is low despite updating the map only when Rover's roll and pitch angles are small (0.5). And, I couldn't completely resolve the problem of Rover getting under the rock and unable to navigate back. Further, I want to improve steering angle of the Rover and make it navigate close to the wall.
