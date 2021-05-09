# restate
A state machine library

```
           ▄████████    ▄████████    ▄████████     ███        ▄████████     ███        ▄████████ 
          ███    ███   ███    ███   ███    ███ ▀█████████▄   ███    ███ ▀█████████▄   ███    ███ 
          ███    ███   ███    █▀    ███    █▀     ▀███▀▀██   ███    ███    ▀███▀▀██   ███    █▀  
         ▄███▄▄▄▄██▀  ▄███▄▄▄       ███            ███   ▀   ███    ███     ███   ▀  ▄███▄▄▄     
        ▀▀███▀▀▀▀▀   ▀▀███▀▀▀     ▀███████████     ███     ▀███████████     ███     ▀▀███▀▀▀     
        ▀███████████   ███    █▄           ███     ███       ███    ███     ███       ███    █▄  
          ███    ███   ███    ███    ▄█    ███     ███       ███    ███     ███       ███    ███ 
          ███    ███   ██████████  ▄████████▀     ▄████▀     ███    █▀     ▄████▀     ██████████ 
          ███    ███                                                                             
  ```


example:
```python
    # Create a state object
    unlocked_state = State(name='unlocked', 
                        on_entry=lambda: print('entring unlocked state..') ,
                        on_exit=lambda:print('exiting unlocked state..')
                     )
                     
    # Define a FSM Machine, intial state & possible states,
    # State can be a simple string object or an instance os `State`
    turnstile = Machine('locked', states=['locked', unlocked_state])
    
    # Define transitions
    turnstile.add_transition(name='lock', start='unlocked', target='locked')
    turnstile.add_transition(name='unlock', start='locked', target='unlocked')
    
    
    print(turnstile.state)
    turnstile.unlock()
    print(turnstile.state)
    turnstile.lock()
    print(turnstile.state)
```
