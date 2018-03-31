#!/usr/bin/env python3

# Copyright (c) 2017 Anki, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License in the file LICENSE.txt or at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''This Program creates two custom wall objects and cozmo will  on recognizing those custom objects
will move as programmed"
.
You can adjust the markers, marker sizes, and object sizes to fit whatever
object you have and the exact size of the markers that you print out.
'''

import time
import cozmo
from cozmo.objects import CustomObject, CustomObjectMarkers, CustomObjectTypes
from cozmo.util import degrees, distance_mm, speed_mmps, distance_inches
from cozmo.behavior import BehaviorTypes

isLeft = [ False ]# these variables are set unset when the objects appear /dissapear
isRight = [ False ]

#will set the default position cozmo's head upon start
def default_position_upon_start(robot: cozmo.robot.Robot):
    robot.set_head_angle(degrees(0)).wait_for_completed()
    robot.set_lift_height(height=0).wait_for_completed()

def handle_object_appeared(evt, **kw):
    # This will be called whenever an EvtObjectAppeared is dispatched -
    # whenever an Object comes into view.
    if isinstance(evt.obj, CustomObject):
        #if the object is a diamond 2
        if(evt.obj.object_type == CustomObjectTypes.CustomType00):
            isRight[0] = True
        #if the object is hexagon 5
        elif(evt.obj.object_type == CustomObjectTypes.CustomType01):
            isLeft[0] = True
        #if the object is hexagon 4
        elif(evt.obj.object_type == CustomObjectTypes.CustomType02):
            isLeft[0] = True



def handle_object_disappeared(evt, **kw):
    # This will be called whenever an EvtObjectDisappeared is dispatched -
    # whenever an Object goes out of view.
    #if the object is a diamond 2
    if(evt.obj.object_type == CustomObjectTypes.CustomType00):
        isRight[0] = False
    #if the object is hexagon 5
    elif(evt.obj.object_type == CustomObjectTypes.CustomType01):
        isLeft[0] = False
    #if the object is hexagon 4
    elif(evt.obj.object_type == CustomObjectTypes.CustomType02):
        isLeft[0] = False


def action_on_seeing_object(robot: cozmo.robot.Robot):


    '''This block uses a full size hexagon 5 printout to initiate the demo.  Cozmo will drive straight for 20.5 inches,
    in which times he will hit the wall.  It'll then do some actions, then turn.  Once cozmo has turned, it should see
    the diamond 2 QR, and begin those actions upon the trigger'''


    if isLeft[0] and CustomObjectTypes.CustomType00:
        robot.drive_straight(distance_inches(20.5), speed_mmps(70)).wait_for_completed()
        robot.say_text("What the????").wait_for_completed()
        robot.drive_straight(distance_inches(-3), speed_mmps(70)).wait_for_completed()
        robot.drive_straight(distance_inches(3), speed_mmps(35)).wait_for_completed()
        robot.say_text("Careful Cozmo....").wait_for_completed()
        robot.turn_in_place(degrees(90)).wait_for_completed()

    '''Once cozmo notices the diamond 2 image, it will begin the actions stated below.  It will eventually do a full
    180 degree turn, and head towards the hexagon 4 image.  This will trigger cozmo's final set of instructions.'''

    if isRight[0] and CustomObjectTypes.CustomType00:
        robot.drive_straight(distance_inches(12), speed_mmps(70)).wait_for_completed()
        robot.play_anim_trigger(cozmo.anim.Triggers.CubePounceLoseSession, ignore_body_track=True).wait_for_completed()
        robot.say_text("Ugh.").wait_for_completed()
        robot.drive_straight(distance_inches(2), speed_mmps(90)).wait_for_completed()
        robot.say_text("You gotta be kidding me!").wait_for_completed()
        robot.drive_straight(distance_inches(-2), speed_mmps(65)).wait_for_completed()
        robot.turn_in_place(degrees(180)).wait_for_completed()

    '''Here cozmo will notice the hexagon 4 image, and should find his way out of the "maze".  To signal that cozmo
    has made it out, the event 'CubePounceWinSession is triggered.'''

    if isLeft[0] and CustomObjectTypes.CustomType02:
        robot.drive_straight(distance_inches(21), speed_mmps(70)).wait_for_completed()
        robot.turn_in_place(degrees(-90)).wait_for_completed()
        robot.say_text("How do I get out of here!?").wait_for_completed()
        robot.drive_straight(distance_inches(2), speed_mmps(25)).wait_for_completed()
        robot.turn_in_place(degrees(-180)).wait_for_completed()
        robot.say_text("It's gotta be around here somewhere").wait_for_completed()
        robot.drive_straight(distance_inches(8), speed_mmps(35)).wait_for_completed()
        robot.play_anim_trigger(cozmo.anim.Triggers.CubePounceWinSession, ignore_body_track=True).wait_for_completed()

def custom_objects(robot: cozmo.robot.Robot):
    # Add event handlers for whenever Cozmo sees a new object
    robot.add_event_handler(cozmo.objects.EvtObjectAppeared, handle_object_appeared)
    robot.add_event_handler(cozmo.objects.EvtObjectDisappeared, handle_object_disappeared)

    default_position_upon_start(robot)



    # define a unique wall (150mm x 120mm (x10mm thick for all walls)
    # with a 50mm x 30mm Circles2 image on front and back
    wall_obj1 = robot.world.define_custom_wall(CustomObjectTypes.CustomType01,
                                              CustomObjectMarkers.Hexagons5,
                                              150, 120,
                                              50, 30, True)
    wall_obj2 = robot.world.define_custom_wall(CustomObjectTypes.CustomType00,
                                                CustomObjectMarkers.Diamonds2,
                                                150, 120,
                                                50, 30, True)
    wall_obj3 = robot.world.define_custom_wall(CustomObjectTypes.CustomType02,
                                               CustomObjectMarkers.Hexagons4,
                                               150, 120,
                                               50, 30, True)

    if ((wall_obj1 is not None) and (wall_obj2 is not None)) and (wall_obj3 is not None):
        print("All objects defined successfully!")
    else:
        print("One or more object definitions failed!")

    print("Press CTRL-C to quit")
    while True:
        #time.sleep(0.1)
        action_on_seeing_object(robot)

cozmo.run_program(custom_objects, use_3d_viewer=False, use_viewer=True)
