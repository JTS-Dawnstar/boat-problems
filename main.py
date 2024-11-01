# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 10:27:50 2024

@author: dawns

 - speed in still water (sy)
 - speed of current (sx)
 
 - width of river (dy)
 - distance of downstream travel (dx)
 
 - time (t)
 
 
 - resultant angle (ra)    # Relative to vertical. 
 - resultant speed (rs)

"""

import random as rand

import numpy as np
np.seterr(all = 'raise') # This is so we can catch bad radicals. 



def main(): 
    print("This is a Physics 11 problem-set generator! To be precise, it generates"
          " 'boat crossing river'-style problems. To be vague, it's 0 accel kinematics. "
          "To be frank, it took forever to make the solution-generator. To be or, not to be. \n\n\n")
    input("Press enter to load the first problem. ")
    print('\n')
    
    while True: 
        # We have to put this all in the mainloop since we have to reset the 
        # cardinal directions every time they ask for a new problem. 
        
        # Choosing directions. 
        vert = rand.choice(['North', 'East', 'South', 'West'])
        if vert in ['North', 'South']: 
            horiz = rand.choice(['East', 'West'])
        else: 
            horiz = rand.choice(['North', 'South'])

        y = ['sy', 'dy', 't']
        x = ['sx', 'dx', 't']
        alls = ['sy', 'sx', 'dy', 'dx', 't', 'ra', 'rs']

        ques = {'sy': "How fast would the boat travel in still water? (km/h)", 
                'sx': f"There is a current moving {horiz}. How fast is it going? (km/h)", 
                'dy': "How wide is the river? (km)", 
                'dx': f"How far will the boat have drifted {horiz} by the time it finishes "
                "crossing? (km)", 
                't': "How long will it take the boat to finish crossing? (hours)", 
                'ra': f"At what angle {horiz} of {vert} is the boat heading, due to the "
                "current? (degrees)", 
                'rs': "What resultant speed is the boat travelling at, including the "
                "current? (km/h)"}

        def randbound(bound = 100): 
            return rand.random() * bound

        def random_boat(): 
            d_knowns = rand.choice([y, x])
            knowns = rand.sample(d_knowns, 2)
            other = rand.choice([i for i in alls if i not in d_knowns])
            all_knowns = knowns + [other]
            out = {prop: round(randbound(), ndigits = 2) for prop in all_knowns}
            if 'ra' in out.keys(): # Override angle. 
                out['ra'] = randbound(bound = 80)
            return out

        def solve_boat(system, log = False): 
            logs = []
            while set(system.keys()) != set(alls): # Neat little hack. 
                keys = system.keys()
                if 't' in keys and 'sy' in keys and 'dy' not in keys: 
                    system['dy'] = system['t'] * system['sy']
                    logs.append(("We can find the width of the river by multiplying the"
                                " boat's speed in still water by the time it takes to "
                                f"cross. d = tv = {round(system['t'], ndigits = 2)} x "
                                f"{round(system['sy'], ndigits = 2)} = "
                                f"{round(system['dy'], ndigits = 2)} km. ", ('t', 'sy'), 'dy'))
                if 't' in keys and 'dy' in keys and 'sy' not in keys: 
                    system['sy'] = system['dy'] / system['t']
                    logs.append(("The boat's speed in still water can be calculated by "
                                "taking the width of the river and dividing it by the "
                                "time it take to cross. v = d/t = "
                                f"{round(system['dy'], ndigits = 2)} / "
                                f"{round(system['t'], ndigits = 2)} = "
                                f"{round(system['sy'], ndigits = 2)} km/h. ", ('dy', 't'), 'sy'))
                if 'sy' in keys and 'dy' in keys and 't' not in keys: 
                    system['t'] = system['dy'] / system['sy']
                    logs.append(("We can find the time it takes the boat to cross via "
                                "dividing the width of the river by the speed of the "
                                "boat in still water. t = d/v = "
                                f"{round(system['dy'], ndigits = 2)} / "
                                f"{round(system['sy'], ndigits = 2)} = "
                                f"{round(system['t'], ndigits = 2)} hours. ", ('dy', 'sy'), 't'))
                if 't' in keys and 'sx' in keys and 'dx' not in keys: 
                    system['dx'] = system['t'] * system['sx']
                    logs.append((f"The distance the boat will drift {horiz} by the time it"
                                " finishes crossing can be found by multiplying the "
                                "time it takes to cross the river by the speed of the "
                                f"current. d = tv = {round(system['t'], ndigits = 2)} x"
                                f" {round(system['sx'], ndigits = 2)} = "
                                f"{round(system['dx'], ndigits = 2)} km. ", ('t', 'sx'), 'dx'))
                if 't' in keys and 'dx' in keys and 'sx' not in keys: 
                    system['sx'] = system['dx'] / system['t']
                    logs.append(("The speed of the current is equal to the distance the"
                                f" boat will have drifted {horiz} divided by the time it "
                                "will take the boat to get to the other side. v = d/t ="
                                f" {round(system['dx'], ndigits = 2)} / "
                                f"{round(system['t'], ndigits = 2)} = "
                                f"{round(system['sx'], ndigits = 2)} km/h. ", ('dx', 't'), 'sx'))
                if 'sx' in keys and 'dx' in keys and 't' not in keys: 
                    system['t'] = system['dx'] / system['sx']
                    logs.append(("We can solve for the time the boat will take to cross"
                                " the river by taking the distance the boat will drift"
                                f" {horiz} over the entire trip, divided by the speed of "
                                f"the {horiz}-bound current. t = d/v = "
                                f"{round(system['dx'], ndigits = 2)} / "
                                f"{round(system['sx'], ndigits = 2)} = "
                                f"{round(system['t'], ndigits = 2)} hours. ", ('dx', 'sx'), 't'))
                
                if 'ra' in keys: 
                    if 'sy' in keys and 'sx' not in keys: 
                        system['sx'] = system['sy'] * np.tan(system['ra'] * np.pi / 180)
                        logs.append(("To find the speed of the current, we can take the "
                                    "speed of the boat in still water, and multiply it by "
                                    "the tangent of the angle the boat is moving at, "
                                    f"relative to {vert}. v_current = v_boat x "
                                    f"tan(angle) = {round(system['sy'], ndigits = 2)} "
                                    f"x {round(np.tan(system['ra'] * np.pi / 180), ndigits = 2)}"
                                    f" = {round(system['sx'], ndigits = 2)} km/h. ", ('sy', 'ra'), 'sx'))
                    elif 'sx' in keys and 'sy' not in keys: 
                        system['sy'] = system['sx'] / np.tan(system['ra'] * np.pi / 180)
                        logs.append(("To find the speed of the boat in still water, we can "
                                    "take the speed of the current, and divide it by "
                                    "the tangent of the angle the boat is moving at, "
                                    f"relative to {vert}. v_boat = v_current / "
                                    f"tan(angle) = {round(system['sx'], ndigits = 2)} "
                                    f"/ {round(np.tan(system['ra'] * np.pi / 180), ndigits = 2)}"
                                    f" = {round(system['sy'], ndigits = 2)} km/h. ", ('sx', 'ra'), 'sy'))
                
                if 'rs' in keys: 
                    if 'sy' in keys and 'sx' not in keys: 
                        system['sx'] = np.sqrt((system['rs'] ** 2) - (system['sy'] ** 2))
                        logs.append(("The Pythagorean Theorem can be used to find the speed"
                                    " of the current from the speed of the boat in still "
                                    "water and the resultant velocity of the boat "
                                    "including the current. v_current = sqrt(v_resultant"
                                    f"^2 - v_boat^2) = sqrt({round(system['rs'] ** 2, ndigits = 2)}"
                                    f" - {round(system['sy'] ** 2, ndigits = 2)}) = "
                                    f"{round(system['sx'], ndigits = 2)} km/h. ", ('rs', 'sy'), 'sx'))
                    elif 'sx' in keys and 'sy' not in keys: 
                        system['sy'] = np.sqrt((system['rs'] ** 2) - (system['sx'] ** 2))
                        logs.append(("We can find the boat's speed in still water by using "
                                    "the Pythagorean Theorem on the speed of the current "
                                    "and the resultant velocity of the boat including the "
                                    "current. v_boat = sqrt(v_resultant"
                                    f"^2 - v_current^2) = sqrt({round(system['rs'] ** 2, ndigits = 2)}"
                                    f" - {round(system['sx'] ** 2, ndigits = 2)}) = "
                                    f"{round(system['sy'], ndigits = 2)} km/h. ", ('rs', 'sx'), 'sy'))
                
                if 'ra' not in keys: 
                    if 'sy' in keys and 'sx' in keys and 'ra' not in keys: 
                        system['ra'] = np.arctan(system['sx'] / system['sy']) * 180 / np.pi
                        logs.append(("To solve for the angle the boat's moving at relative "
                                    f"to {vert}, we can calculate the inverse tangent of the"
                                    " speed of the current divided by the speed of the "
                                    "boat in still water. angle = arctan(v_current / v_boat)"
                                    f" = arctan({round(system['sx'], ndigits = 2)} / "
                                    f"{round(system['sy'], ndigits = 2)}) = "
                                    f"{round(system['ra'], ndigits = 2)} degrees East of North. ", ('sx', 'sy'), 'ra'))
                if 'rs' not in keys: 
                    if 'sy' in keys and 'sx' in keys and 'rs' not in keys: 
                        system['rs'] = np.sqrt((system['sx'] ** 2) + (system['sy'] ** 2))
                        logs.append(("To solve for the resultant speed of the boat, "
                                    "including the current, we can use the Pythagorean "
                                    "Theorem on the speed of the current and the speed of "
                                    "the boat in still water. v_resultant = sqrt(v_current"
                                    f"^2 - v_boat^2) = sqrt({round(system['sx'] ** 2, ndigits = 2)}"
                                    f" + {round(system['sy'] ** 2, ndigits = 2)}) = "
                                    f"{round(system['rs'], ndigits = 2)} km/h. ", ('sx', 'sy'), 'rs'))
            
            if log: 
                return (system, logs)
            else: 
                return system


        def eng_prob(sys, solvefor): 
            keys = sys.keys()
            system = {key: str(round(value, ndigits = 2)) for (key, value) in 
                      sys.items()}
            string = f"A boat is crossing a river. It's travelling {vert}. "
            if 'sy' in keys: 
                string += f"Its speed in still water is {system['sy']} km/h. "
            if 'sx' in keys: 
                string += f"The current is going {horiz} at {system['sx']} km/h. "
            else: 
                string += f"There is a current heading {horiz}. "
            if 'dy' in keys: 
                string += f"The river is {system['dy']} km wide. "
            if 'dx' in keys: 
                string += (f"Once it finishes crossing, the boat will have drifted"
                              f" {system['dx']} km {horiz}, due to the current. ")
            if 't' in keys: 
                string += (f"It will take the boat {system['t']} hours to finish "
                              f"crossing. ")
            if 'ra' in keys: 
                string += (f"Because of the current, the boat is heading "
                              f"{system['ra']} degrees {horiz} of {vert}. ")
            if 'rs' in keys: 
                string += f"The boat's resultant velocity, including the current, is {system['rs']} km/h. "
            
            string += '\n\n'
            string += ques[solvefor]
            return string


        def rand_eng_prob(): 
            sys = random_boat()
            unknowns = [i for i in alls if i not in sys.keys()]
            solve = rand.choice(unknowns)
            
            print(eng_prob(sys, solvefor = solve) + '\n\n')
            return (sys, solve)
        
        sys, solve = rand_eng_prob()
        while True: 
            try: 
                solved_sys, logs = solve_boat(sys, log = True)
            except: # Bad radicals. 
                continue
            else: 
                break
        # print(solved_sys)
        ans = solved_sys[solve]
        
        # print(logs)
        
        #---- Worked Solutions ----#
        
        counter = 0
        while counter < len(logs): 
            if logs[counter][2] == solve: 
                break # Stop when counter is correct. 
            counter += 1
        
        logsupto = logs[:counter + 1]
        logsneeded = logsupto.copy()
        for log in logsupto: # Removes unneeded steps. Basically if we calculated
                             # something that we never use, we can delete the log. 
            if (log[2] not in sum([[i for i in j[1]] for j in logsupto[logsupto.index(log):]], 
                                  start = [])) and logsupto.index(log) != len(logsupto) - 1: 
                logsneeded.remove(log)
        
        # print([i[0] for i in logsneeded])
        
        # Adding the 'then' for better wording in solutions. 
        stringlogs = [i[0] for i in logsneeded]
        if len(stringlogs) >= 2: 
            stringlogs[1] = 'Then, ' + stringlogs[1][0].lower() + stringlogs[1][1:]
        
        # Putting a nice summary on to the solution. 
        # Also we do some variable prep so I can reuse the code from eng_prob. 
        keys = [solve]
        system = {key: round(value, ndigits = 2) for (key, value) in solved_sys.items()}
        string = ''
        if 'sy' in keys: 
            string += f"Its speed in still water is {system['sy']} km/h. "
        if 'sx' in keys: 
            string += f"The current is going {horiz} at {system['sx']} km/h. "
        if 'dy' in keys: 
            string += f"The river is {system['dy']} km wide. "
        if 'dx' in keys: 
            string += (f"Once it finishes crossing, the boat will have drifted"
                          f" {system['dx']} km {horiz}, due to the current. ")
        if 't' in keys: 
            string += (f"It will take the boat {system['t']} hours to finish "
                          f"crossing. ")
        if 'ra' in keys: 
            string += (f"Because of the current, the boat is heading "
                          f"{system['ra']} degrees {horiz} of {vert}. ")
        if 'rs' in keys: 
            string += f"The boat's resultant velocity is {system['rs']} km/h. "
        string = 'Therefore, ' + string[0].lower() + string[1:] + '\u2610' # Nice Q.E.D. box. 
        stringlogs.append(string)
        
        # print('\n\n'.join(stringlogs))
        
        try: 
            user_input = float(input(" >>> "))
        except ValueError: 
            print(f"That ain't a number. The answer is {round(ans, ndigits = 2)}\n\n")
        else: 
            if 0.01 < abs(ans - user_input) < 1: 
                print(f"Correct! To be precise, it's {round(ans, ndigits = 2)}. \n\n")
            elif abs(ans - user_input) < 0.01: 
                print("Correct! Zero error too. ")
            else: 
                print(f"Not quite! It's actually {round(ans, ndigits = 2)}. \n\n")
        
        choice = input("Would you like to see a full solution? (y / n) \n >>> ")
        if 'y' in choice: 
            print("Awesome! Here it is: \n")
            print('\n\n'.join(stringlogs) + '\n')
        else: 
            print("Okay, but make sure to check out the full solutions at "
                  "some point. They're pretty cool and took FOREVER to make. \n")
        
        input("Press enter to load the next problem. ")
        print('\n')

main()
