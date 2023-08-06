import math,random,time

from roboball2d import factory


def run(rendering=True):

    """
    Runs the balls demo, in which the robot moves according to random
    torques as 10 balls bounces around.
    You may run the executable roboball2d_balls_demo after install.

    Parameters
    ----------

    rendering : 
        renders the environment if True
    
    """


    # default physics and rendering, with 10 balls.
    # The first ball will be pink.
    r2d = factory.get_default(nb_balls=10,
                              ball_colors={0:(1,0.08,0.57)},
                              render=rendering)
    

    # we add a fixed goal
    # starting at x=3 and finishing at x=4
    goal = (2,4)
    goal_color = (0,0.7,0) # usual color
    goal_activated_color = (0,1,0) # when hit by a ball

    # running 10 episodes, max 3 seconds per episode
    n_episodes = 0

    for episode in range(10):

        # tracking the number of times the ball bounced
        n_bounced = 0

        # reset before a new episode
        r2d.world.reset(r2d.robot_reinit,
                        r2d.ball_guns)
        
        while True:

            # random torques
            torques = [random.uniform(-1.0,1.0) for _ in range(3)]

            # returns a snapshot of all the data computed
            # and updated by the physics engine at this
            # iteration 
            world_state = r2d.world.step(torques,relative_torques=True)

            # episode ends 
            # if the number of bounces is 2 or above
            # for the first ball ...
            if world_state.ball_hits_floor :
                n_bounced += 1
                if n_bounced >= 2:
                    break

            # ... or if 3 seconds passed
            if world_state.t > 3:
                break

            # display the goal with a lighter color
            # if hit by a ball at this iteration
            color = goal_color
            for p in world_state.balls_hits_floor:
                p = world_state.ball_hits_floor
                if p is not None and p>goal[0] and p<goal[1]:
                    # goal hit, using activated color
                    color = goal_activated_color
                    break

            # the renderer can take in an array of goals
            # to display. Here specifying only 1 goal
            # (start_x,end_x,color)
            goals = [(goal[0],goal[1],color)]

            # render based on the information provided by
            # the physics engine
            if rendering:
                r2d.renderer.render(world_state,goals,
                                    time_step=1.0/60.0)


