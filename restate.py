from typing import List
import logging
import pprint


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class State:
    def __init__(self, name: str, on_entry=None, on_exit=None):
        self.name = name
        self._on_entry = on_entry
        self._on_exit = on_exit
    
    @property
    def on_entry(self):
        logger.debug(f'Entering state {self.name}')
        
        return self._on_entry
    
    @on_entry.setter
    def on_entry(self, func):
        self._on_entry = func
        
    @property
    def on_exit(self):
        logger.debug(f'Leaving state {self.name}')
        
        return self._on_exit
    
    @on_exit.setter
    def on_exit(self, func):
        self._on_exit = func
        
        
class Transition:
    def __init__(self, name, _machine, start=None, target=None):
        self.name = name
        self.start = start
        self.target = target
        
        if isinstance(_machine, Machine):
            self.machine = _machine
        else:
            raise Exception('Machine can be only of type `Machine`')
        
    def __str__(self):
        return f' Active state-> {self.machine.active_state} Transition-> ({self.start}, {self.target})'
    
    def do_transition(self):
        if transition:= self.machine.transitions.get(self.name, None):
            ok = (
                    transition.start == self.machine.active_state and 
                    transition.target == self.target
                )
            if not ok:
                raise Exception(f'Cannot change state to {self.name} from {self.machine.active_state}')
            
            
            # execute on_exit for current state , if any.
            current_state = self.machine.states[self.machine.active_state]
            next_state = self.machine.states[self.target]
            
            try:
                current_state.on_exit()
            except (AttributeError, TypeError):
                pass 
            
            self.machine.active_state = self.target

            try:
                next_state.on_entry()
            except (AttributeError, TypeError):
                pass
            

class Machine(object):
    
    def __init__(self, initial_sate, states: List[str]):
        self.initial_state = initial_sate
        self.states = {}
        self.add_states(states)
        self.transitions = {}
        self.active_state = initial_sate

    @property
    def state(self):
        return self.active_state
    
    @property
    def state_names(self):
        return self.states.keys()
    
    def add_states(self, states):
        for state in states:
            if isinstance(state, State):
                self.states[state.name] = state
            else:
                self.states[state] = State(name=state)
                
    def __getattr__(self, transition):
        transition_obj = self.transitions[transition]
        return transition_obj.do_transition

    def add_transition(self, name:str, start: str, target:str):
        state_names = self.state_names
        
        if start not in state_names or target not in state_names:
            raise Exception(f'transition cannot be added , one of state {start} , {target} is invalid')
        
        if not isinstance(name , Transition):
                transition = Transition(name=name, _machine=self, start=start, target=target)
        self.transitions[transition.name] = transition 
        
        
if __name__ == "__main__":
    unlocked_state = State(name='unlocked', on_entry=lambda: print('entring unlocked state..') , on_exit=lambda:print('exiting unlocked state..'))
    turnstile = Machine('locked', states=['locked', unlocked_state])
    turnstile.add_transition(name='lock', start='unlocked', target='locked')
    turnstile.add_transition(name='unlock', start='locked', target='unlocked')
    
    print(turnstile.state)
    turnstile.unlock()
    print(turnstile.state)
    turnstile.lock()
    print(turnstile.state)
