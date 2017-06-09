import numpy as np
import math


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
            # Set the navigation angle towards the rock if found, else set it to navigable terrain
            if(not math.isnan(np.mean(Rover.rock_dists))):
                nav_avg_angle = np.clip(np.mean(Rover.rock_angles * 180/np.pi), -15, 15)
            else:
                nav_avg_angle = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -15, 15)
            # Check if rover is near sample and if it is not picking up, then pick up the sample
            if Rover.near_sample and not Rover.picking_up:
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
            # See if the rover is stuck by checking roll or pitch.
            elif ((Rover.roll > 3) & (Rover.pitch > 3)):
                Rover.throttle = 0
                Rover.brake = 0
                Rover.mode = 'stop'
            # Check the extent of navigable terrain
            elif len(Rover.nav_angles) >= Rover.stop_forward:  
                # If mode is forward, navigable terrain looks good 
                # and velocity is below max, then throttle 
                if Rover.vel < Rover.max_vel:
                    # Set throttle value to throttle setting
                    Rover.throttle = Rover.throttle_set
                else: # Else coast
                    Rover.throttle = 0
                # Set steering to average angle clipped to the range +/- 15           
                #Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -15, 15)
                #Rover.steer = nav_avg_angle
                #obs_avg_angle = np.clip(np.mean(Rover.obst_angles * 180/np.pi), -15, 15)
                #Rover.avg_angle = np.mean([nav_avg_angle, obs_avg_angle])
                #Rover.steer = Rover.avg_angle
                if nav_avg_angle > 11.45:
                    Rover.steer = -5
                elif nav_avg_angle < 0:
                    Rover.steer = 5
                else:
                    Rover.steer = 0
                Rover.steer = nav_avg_angle
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
                    Rover.throttle = 0
                    # Release the brake
                    Rover.brake = 0
                    # Set steer to mean angle
                    Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -15, 15)
                    Rover.mode = 'forward'
    # Just to make the rover do something 
    # even if no modifications have been made to the code
    else:
        Rover.throttle = Rover.throttle_set
        Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -15, 15)
        Rover.brake = 0
        Rover.mode = 'forward'
    
    # If in a state where want to pickup a rock send pickup command
    #if Rover.near_sample and Rover.vel == 0 and not Rover.picking_up:
        #Rover.send_pickup = True
    
    return Rover

