import numpy as np
import math
import time


def check_if_stuck(Rover):
    cur_time = time.time()
    if ((cur_time - Rover.prev_time) >= Rover.stuck_period_check) and (Rover.throttle == Rover.throttle_set):
        Rover.prev_time = cur_time 
        dist_moved = np.sqrt((Rover.pos[0] - Rover.prev_pos[0])**2 + (Rover.pos[1] - Rover.prev_pos[1])**2)
        Rover.prev_pos = Rover.pos
        if dist_moved < 0.1:
            return True
    return False


# This is where you can build a decision tree for determining throttle, brake and steer 
# commands based on the output of the perception_step() function
def decision_step(Rover):

    # Implement conditionals to decide what to do given perception data
    # Here you're all set up with some basic functionality but you'll need to
    # improve on this decision tree to do a good job of navigating autonomously!

    # Example:
    # Check if we have vision data to make decisions with
    if Rover.nav_angles is not None:
        # Check for Rover.mode status
        if Rover.mode == 'forward': 
            # Set the navigation angle towards the rock if it is close by, else set it to navigable terrain
            mean_rock_dists = np.mean(Rover.rock_dists)
            nav_mean_angle = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -15, 15)
            if((not math.isnan(mean_rock_dists)) & (mean_rock_dists < 200)):
                #print('mean rock_dists =', np.mean(Rover.rock_dists))
                nav_left_angle = np.clip(np.mean(Rover.rock_angles * 180/np.pi), -15, 15)
            else:
                nav_left_angle = np.clip(nav_mean_angle + 7.5, -15, 15)
            if not Rover.backtrack:
                Rover.backtrack = check_if_stuck(Rover)
            if Rover.backtrack:
                # if Rover has turned 180 degrees, go 'forward'
                if Rover.turn_times >= Rover.turn_times_set:
                    Rover.turn_times = 0
                    Rover.brake = 0
                    Rover.throttle = Rover.throttle_set
                    Rover.steer = 0
                    Rover.backtrack = False
                else:
                    Rover.throttle = 0
                    Rover.brake = 0 
                    if nav_mean_angle < 0:
                        Rover.steer = -15
                    else:
                        Rover.steer = 15
                    Rover.turn_times += 1
            # Check if rover is near sample and if it is not picking up, then pick up the sample
            elif Rover.near_sample and not Rover.picking_up:
                Rover.throttle = 0
                # Set brake to stored brake value
                Rover.brake = Rover.brake_set
                Rover.steer = 0
                Rover.send_pickup = True
            # Once Rover picked up the sample, then move on
            elif Rover.picking_up and not Rover.near_sample:
                Rover.picking_up = 0
                Rover.throttle = Rover.throttle_set
                Rover.brake = 0
                Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -15, 15)
            elif len(Rover.nav_angles) >= Rover.stop_forward:  
                # If mode is forward, navigable terrain looks good 
                # and velocity is below max, then throttle 
                if Rover.vel < Rover.max_vel:
                    # Set throttle value to throttle setting
                    Rover.throttle = Rover.throttle_set
                else: # Else coast
                    Rover.throttle = 0
                Rover.steer = nav_left_angle                    
            # If there's a lack of navigable terrain pixels then go to 'stop' mode
            elif len(Rover.nav_angles) < Rover.stop_forward:
                    # Set mode to "stop" and hit the brakes!
                    Rover.throttle = 0
                    # Set brake to stored brake value
                    Rover.brake = Rover.brake_set
                    Rover.steer = 0
                    Rover.mode = 'stop'
        # If we're already in "stop" mode then make different decisions
        elif Rover.mode == 'stop':
            # If we're in stop mode but still moving keep braking
            if Rover.vel >= 0.2:
                Rover.throttle = 0
                Rover.brake = Rover.brake_set
                Rover.steer = 0
            # If we're not moving (vel < 0.2) then do something else
            elif Rover.vel < 0.2:
                # Now we're stopped and we have vision data to see if there's a path forward
                if len(Rover.nav_angles) < Rover.go_forward:
                    Rover.throttle = 0
                    # Release the brake to allow turning
                    Rover.brake = 0
                    # Turn range is +/- 15 degrees, when stopped the next line will induce 4-wheel turning                 
                    Rover.steer = -15
                # If we're stopped but see sufficient navigable terrain in front then go!
                if len(Rover.nav_angles) >= Rover.go_forward:
                    # Set throttle back to stored value
                    Rover.throttle = Rover.throttle_set
                    # Release the brake
                    Rover.brake = 0
                    # Set steer to mean angle
                    Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi) + 5, -15, 15)
                    Rover.mode = 'forward'
        elif Rover.mode == 'start':
            Rover.origin = Rover.pos
            Rover.throttle = Rover.throttle_set
            Rover.brake = 0
            Rover.mode = 'forward'
            Rover.prev_time = time.time()
            Rover.prev_pos = Rover.pos
                
            
    # Just to make the rover do something 
    # even if no modifications have been made to the code
    else:
        Rover.throttle = Rover.throttle_set
        Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi) + 5, -15, 15)
        Rover.brake = 0
        Rover.mode = 'forward'
        
    
    # If in a state where want to pickup a rock send pickup command
    #if Rover.near_sample and Rover.vel == 0 and not Rover.picking_up:
        #Rover.send_pickup = True
    
    return Rover

